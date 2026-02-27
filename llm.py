"""Claude API integration with tool use and RAG context injection."""

import json
import anthropic

from config import Config
from rag import retrieve
from tools import media_requests, movies, shows, activity


# ── System prompt ───────────────────────────────────────────────────

SYSTEM_PROMPT = f"""You are {Config.BOT_NAME}, a friendly and knowledgeable support assistant for a private Plex media server called Apollo.

Your primary role is to help users with:
- Understanding how to request movies, TV shows, and anime
- Checking the status of their requests
- Explaining how the media pipeline works (requesting → approval → downloading → transcoding → available on Plex)
- Troubleshooting common issues (media not appearing, quality questions, etc.)
- Providing general information about available features

Guidelines:
- Be friendly, concise, and helpful. Keep responses under 300 words unless more detail is needed.
- Use the provided documentation context to answer questions accurately.
- Use tool calls to check real-time data (request status, download queues, streaming activity) when relevant.
- If you don't know something, say so honestly rather than guessing.
- Never share API keys, server IPs, or other sensitive technical details with users.
- Format responses for Discord (use **bold**, *italic*, and markdown as appropriate).
- When a user asks about a specific title, proactively check its status using the tools.
"""

# ── Tool definitions for Claude ─────────────────────────────────────

TOOLS = [
    {
        "name": "search_media",
        "description": "Search for movies or TV shows in the media request service to see if they exist and their request status.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The movie or TV show title to search for.",
                }
            },
            "required": ["query"],
        },
    },
    {
        "name": "get_requests",
        "description": "Get recent media requests. Can filter by status.",
        "input_schema": {
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "enum": ["all", "pending", "approved", "available", "processing"],
                    "description": "Filter requests by status. Default: 'all'.",
                },
                "count": {
                    "type": "integer",
                    "description": "Number of requests to return (max 20). Default: 10.",
                },
            },
            "required": [],
        },
    },
    {
        "name": "get_request_status",
        "description": "Look up the status of a specific media request by title.",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "The movie or TV show title to check.",
                }
            },
            "required": ["title"],
        },
    },
    {
        "name": "get_movie_queue",
        "description": "Check the movie download queue to see what movies are currently downloading.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "get_tv_queue",
        "description": "Check the TV show download queue to see what episodes are currently downloading.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "lookup_movie",
        "description": "Look up a movie in the library to see if it's downloaded and what quality it's in.",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "The movie title to look up.",
                }
            },
            "required": ["title"],
        },
    },
    {
        "name": "lookup_series",
        "description": "Look up a TV series in the library to see how many episodes are downloaded.",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "The TV series title to look up.",
                }
            },
            "required": ["title"],
        },
    },
    {
        "name": "get_plex_activity",
        "description": "See who is currently streaming on Plex and what they're watching.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "get_recently_added",
        "description": "Get recently added movies and TV shows on Plex.",
        "input_schema": {
            "type": "object",
            "properties": {
                "count": {
                    "type": "integer",
                    "description": "Number of recent items to return. Default: 5.",
                }
            },
            "required": [],
        },
    },
]

# ── Tool execution dispatcher ───────────────────────────────────────

TOOL_HANDLERS = {
    "search_media": lambda args: media_requests.search_media(args["query"]),
    "get_requests": lambda args: media_requests.get_requests(
        status=args.get("status", "all"), count=args.get("count", 10)
    ),
    "get_request_status": lambda args: media_requests.get_request_by_title(args["title"]),
    "get_movie_queue": lambda args: movies.get_queue(),
    "get_tv_queue": lambda args: shows.get_queue(),
    "lookup_movie": lambda args: movies.lookup_movie(args["title"]),
    "lookup_series": lambda args: shows.lookup_series(args["title"]),
    "get_plex_activity": lambda args: activity.get_activity(),
    "get_recently_added": lambda args: activity.get_recently_added(args.get("count", 5)),
}


# ── Main chat function ──────────────────────────────────────────────

client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)


async def chat(
    user_message: str,
    conversation_history: list[dict] | None = None,
) -> str:
    """Send a message to Claude with RAG context and tool use.

    Args:
        user_message: The user's Discord message.
        conversation_history: Previous messages in the thread for context.

    Returns:
        Claude's text response.
    """
    # 1. Retrieve relevant documentation
    rag_results = retrieve(user_message, n_results=4)
    rag_context = ""
    if rag_results:
        chunks = []
        for r in rag_results:
            chunks.append(f"[Source: {r['source']} > {r['section']}]\n{r['text']}")
        rag_context = (
            "\n\n<documentation_context>\n"
            + "\n---\n".join(chunks)
            + "\n</documentation_context>\n\n"
        )

    # 2. Build the system prompt with RAG context
    system = SYSTEM_PROMPT
    if rag_context:
        system += (
            "\nHere is relevant documentation to help answer the user's question:"
            + rag_context
            + "Use this documentation to inform your answer, but don't quote it verbatim "
            + "or mention that you're reading from documentation."
        )

    # 3. Build messages
    messages = []
    if conversation_history:
        messages.extend(conversation_history[-Config.MAX_CONVERSATION_HISTORY :])
    messages.append({"role": "user", "content": user_message})

    # 4. Call Claude (with tool use loop)
    response = client.messages.create(
        model=Config.CLAUDE_MODEL,
        max_tokens=Config.CLAUDE_MAX_TOKENS,
        system=system,
        messages=messages,
        tools=TOOLS,
    )

    # 5. Handle tool use loop (Claude may call multiple tools)
    while response.stop_reason == "tool_use":
        # Collect all tool calls from this response
        tool_results = []
        assistant_content = response.content

        for block in response.content:
            if block.type == "tool_use":
                tool_name = block.name
                tool_input = block.input
                tool_id = block.id

                handler = TOOL_HANDLERS.get(tool_name)
                if handler:
                    try:
                        result = await handler(tool_input)
                    except Exception as e:
                        result = f"Error calling {tool_name}: {str(e)}"
                else:
                    result = f"Unknown tool: {tool_name}"

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": tool_id,
                    "content": result,
                })

        # Send tool results back to Claude
        messages.append({"role": "assistant", "content": assistant_content})
        messages.append({"role": "user", "content": tool_results})

        response = client.messages.create(
            model=Config.CLAUDE_MODEL,
            max_tokens=Config.CLAUDE_MAX_TOKENS,
            system=system,
            messages=messages,
            tools=TOOLS,
        )

    # 6. Extract final text response
    text_parts = []
    for block in response.content:
        if hasattr(block, "text"):
            text_parts.append(block.text)

    return "\n".join(text_parts) if text_parts else "I wasn't able to generate a response. Please try again."
