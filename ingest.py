#!/usr/bin/env python3
"""Standalone script to ingest documentation into ChromaDB.

Usage:
    python ingest.py              # Ingest all docs
    python ingest.py query "how do I request a movie"  # Test retrieval
"""

import sys
from rag import ingest_docs, retrieve


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "query":
        query = " ".join(sys.argv[2:])
        if not query:
            print("Usage: python ingest.py query <your question>")
            return
        results = retrieve(query)
        print(f"\n🔍 Top results for: '{query}'\n")
        for i, r in enumerate(results, 1):
            print(f"  {i}. [{r['source']} > {r['section']}] (dist: {r['distance']:.3f})")
            print(f"     {r['text'][:200]}...\n")
    else:
        print("📥 Ingesting documentation from ./docs/\n")
        count = ingest_docs("./docs")
        if count > 0:
            print("\n✅ Ready! You can test with: python ingest.py query 'how do I request a movie'")
        else:
            print("\n⚠️  No documents ingested. Add .md files to the ./docs/ directory.")


if __name__ == "__main__":
    main()
