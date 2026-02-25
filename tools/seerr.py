"""Seerr API wrapper for Apollo Bot tool calls."""

import aiohttp
from config import Config

HEADERS = {
    "X-Api-Key": Config.SEERR_API_KEY,
    "Content-Type": "application/json",
}


async def _get(endpoint: str, params: dict | None = None) -> dict | list:
    """Make a GET request to the Seerr API."""
    url = f"{Config.SEERR_URL}/api/v1{endpoint}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=HEADERS, params=params) as resp:
            resp.raise_for_status()
            return await resp.json()


async def search_media(query: str) -> str:
    """Search for movies and TV shows in Seerr."""
    data = await _get("/search", params={"query": query, "page": 1, "language": "en"})
    results = data.get("results", [])[:5]

    if not results:
        return f"No results found for '{query}'."

    lines = []
    for item in results:
        media_type = item.get("mediaType", "unknown")
        title = item.get("title") or item.get("name", "Unknown")
        year = (item.get("releaseDate") or item.get("firstAirDate") or "")[:4]
        status = _media_status(item.get("mediaInfo", {}))
        lines.append(f"• **{title}** ({year}) [{media_type}] — {status}")

    return "**Search Results:**\n" + "\n".join(lines)


async def get_requests(status: str = "all", count: int = 10) -> str:
    """Get recent media requests from Seerr.

    status: 'all', 'pending', 'approved', 'available', 'processing'
    """
    params = {"take": count, "skip": 0, "sort": "added"}
    if status != "all":
        filter_map = {
            "pending": "pendingapproval",
            "approved": "approved",
            "available": "available",
            "processing": "processing",
        }
        params["filter"] = filter_map.get(status, status)

    data = await _get("/request", params=params)
    results = data.get("results", [])

    if not results:
        return f"No {status} requests found."

    lines = []
    for req in results:
        media = req.get("media", {})
        media_type = req.get("type", "unknown")
        title = media.get("title") or media.get("name") or f"ID:{media.get('tmdbId', '?')}"
        req_status = _request_status(req.get("status", 0))
        requested_by = req.get("requestedBy", {}).get("displayName", "Unknown")
        lines.append(f"• **{title}** [{media_type}] — {req_status} (by {requested_by})")

    return f"**Recent Requests ({status}):**\n" + "\n".join(lines)


async def get_request_by_title(title: str) -> str:
    """Look up the status of a specific request by searching for it."""
    # First search for the media
    data = await _get("/search", params={"query": title, "page": 1, "language": "en"})
    results = data.get("results", [])

    for item in results:
        media_info = item.get("mediaInfo")
        if media_info:
            name = item.get("title") or item.get("name", "Unknown")
            status = _media_status(media_info)
            requests = media_info.get("requests", [])
            detail = ""
            if requests:
                req = requests[0]
                requested_by = req.get("requestedBy", {}).get("displayName", "Someone")
                detail = f" | Requested by: {requested_by}"
            return f"**{name}**: {status}{detail}"

    return f"Could not find any request matching '{title}'. It may not have been requested yet."


def _media_status(media_info: dict) -> str:
    """Convert Seerr media status codes to human-readable text."""
    if not media_info:
        return "Not requested"
    status = media_info.get("status", 0)
    status_map = {
        1: "🟡 Unknown",
        2: "🟠 Pending approval",
        3: "⏳ Processing (downloading/transcoding)",
        4: "🟢 Partially available",
        5: "✅ Available",
    }
    return status_map.get(status, f"Status code: {status}")


def _request_status(status_code: int) -> str:
    """Convert request status code to human-readable text."""
    status_map = {
        0: "🟡 Pending approval",
        1: "🟠 Approved",
        2: "✅ Available",
        3: "❌ Declined",
    }
    return status_map.get(status_code, f"Status: {status_code}")
