"""RAG pipeline: ingest markdown docs into ChromaDB and retrieve relevant chunks."""

import os
import hashlib
from pathlib import Path

import chromadb
from chromadb.config import Settings

from config import Config


def get_chroma_client() -> chromadb.ClientAPI:
    """Create a persistent ChromaDB client."""
    return chromadb.PersistentClient(
        path=Config.CHROMA_PERSIST_DIR,
        settings=Settings(anonymized_telemetry=False),
    )


def get_collection(client: chromadb.ClientAPI) -> chromadb.Collection:
    """Get or create the docs collection.

    Uses ChromaDB's default embedding function (all-MiniLM-L6-v2)
    which runs locally — no external API calls needed for embeddings.
    """
    return client.get_or_create_collection(
        name=Config.CHROMA_COLLECTION,
        metadata={"hnsw:space": "cosine"},
    )


# ── Chunking ────────────────────────────────────────────────────────


def chunk_markdown(text: str, source: str, max_chars: int = 1000, overlap: int = 200) -> list[dict]:
    """Split a markdown document into overlapping chunks.

    Tries to split on headings (##) first, then falls back to paragraph
    boundaries. Each chunk includes metadata about its source file.
    """
    chunks: list[dict] = []

    # Split on markdown headings first
    sections = _split_on_headings(text)

    for section_title, section_body in sections:
        # If a section is small enough, keep it as one chunk
        if len(section_body) <= max_chars:
            chunks.append({
                "text": section_body.strip(),
                "source": source,
                "section": section_title,
            })
        else:
            # Split large sections into overlapping paragraph chunks
            paragraphs = section_body.split("\n\n")
            current_chunk = ""
            for para in paragraphs:
                if len(current_chunk) + len(para) > max_chars and current_chunk:
                    chunks.append({
                        "text": current_chunk.strip(),
                        "source": source,
                        "section": section_title,
                    })
                    # Keep overlap from end of previous chunk
                    current_chunk = current_chunk[-overlap:] + "\n\n" + para
                else:
                    current_chunk += "\n\n" + para if current_chunk else para

            if current_chunk.strip():
                chunks.append({
                    "text": current_chunk.strip(),
                    "source": source,
                    "section": section_title,
                })

    return chunks


def _split_on_headings(text: str) -> list[tuple[str, str]]:
    """Split markdown text on ## headings. Returns (heading, body) pairs."""
    lines = text.split("\n")
    sections: list[tuple[str, str]] = []
    current_heading = "Introduction"
    current_lines: list[str] = []

    for line in lines:
        if line.startswith("## "):
            if current_lines:
                sections.append((current_heading, "\n".join(current_lines)))
            current_heading = line.lstrip("# ").strip()
            current_lines = [line]
        else:
            current_lines.append(line)

    if current_lines:
        sections.append((current_heading, "\n".join(current_lines)))

    return sections


# ── Ingestion ───────────────────────────────────────────────────────


def ingest_docs(docs_dir: str = "./docs") -> int:
    """Ingest all markdown files from docs_dir into ChromaDB.

    Returns the number of chunks ingested.
    """
    client = get_chroma_client()
    collection = get_collection(client)

    docs_path = Path(docs_dir)
    if not docs_path.exists():
        print(f"❌ Docs directory not found: {docs_dir}")
        return 0

    md_files = list(docs_path.glob("**/*.md"))
    if not md_files:
        print(f"⚠️  No .md files found in {docs_dir}")
        return 0

    total_chunks = 0
    for md_file in md_files:
        text = md_file.read_text(encoding="utf-8")
        relative_path = str(md_file.relative_to(docs_path))
        chunks = chunk_markdown(text, source=relative_path)

        if not chunks:
            continue

        ids = []
        documents = []
        metadatas = []
        for i, chunk in enumerate(chunks):
            # Deterministic ID based on content so re-ingestion is idempotent
            chunk_id = hashlib.md5(
                f"{chunk['source']}:{i}:{chunk['text'][:100]}".encode()
            ).hexdigest()
            ids.append(chunk_id)
            documents.append(chunk["text"])
            metadatas.append({"source": chunk["source"], "section": chunk["section"]})

        collection.upsert(ids=ids, documents=documents, metadatas=metadatas)
        total_chunks += len(chunks)
        print(f"  ✅ {relative_path}: {len(chunks)} chunks")

    print(f"\n📚 Ingested {total_chunks} chunks from {len(md_files)} files.")
    return total_chunks


# ── Retrieval ───────────────────────────────────────────────────────


def retrieve(query: str, n_results: int = 5) -> list[dict]:
    """Retrieve the most relevant document chunks for a query.

    Returns a list of dicts with 'text', 'source', 'section', and 'distance'.
    """
    client = get_chroma_client()
    collection = get_collection(client)

    if collection.count() == 0:
        return []

    results = collection.query(query_texts=[query], n_results=n_results)

    retrieved = []
    for i in range(len(results["ids"][0])):
        retrieved.append({
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i].get("source", "unknown"),
            "section": results["metadatas"][0][i].get("section", ""),
            "distance": results["distances"][0][i] if results["distances"] else None,
        })

    return retrieved


# ── CLI entrypoint ──────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "query":
        query = " ".join(sys.argv[2:])
        results = retrieve(query)
        print(f"\n🔍 Results for: '{query}'\n")
        for r in results:
            print(f"  [{r['source']} > {r['section']}] (distance: {r['distance']:.3f})")
            print(f"  {r['text'][:200]}...\n")
    else:
        print("📥 Ingesting documentation...\n")
        ingest_docs()
