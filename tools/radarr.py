"""Radarr API wrapper for Apollo Bot tool calls."""

import aiohttp
from config import Config

HEADERS = {
    "X-Api-Key": Config.RADARR_API_KEY,
    "Content-Type": "application/json",
}


async def _get(endpoint: str, params: dict | None = None) -> dict | list:
    url = f"{Config.RADARR_URL}/api/v3{endpoint}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=HEADERS, params=params) as resp:
            resp.raise_for_status()
            return await resp.json()


async def get_queue() -> str:
    """Get the current Radarr download queue."""
    data = await _get("/queue", params={"pageSize": 10, "sortKey": "progress", "sortDirection": "ascending"})
    records = data.get("records", [])

    if not records:
        return "The Radarr download queue is empty — nothing is currently downloading."

    lines = []
    for item in records:
        title = item.get("title", "Unknown")
        status = item.get("status", "unknown")
        progress = item.get("sizeleft", 0)
        size = item.get("size", 1)
        pct = round((1 - progress / size) * 100, 1) if size > 0 else 0
        time_left = item.get("timeleft", "unknown")
        lines.append(f"• **{title}** — {status} | {pct}% done | ETA: {time_left}")

    return "**Radarr Download Queue:**\n" + "\n".join(lines)


async def lookup_movie(title: str) -> str:
    """Look up a movie in Radarr's library."""
    movies = await _get("/movie/lookup", params={"term": title})

    if not movies:
        return f"No movie found matching '{title}' in Radarr."

    # Check top results
    lines = []
    for movie in movies[:3]:
        name = movie.get("title", "Unknown")
        year = movie.get("year", "?")
        monitored = movie.get("monitored", False)
        has_file = movie.get("hasFile", False)
        quality = movie.get("movieFile", {}).get("quality", {}).get("quality", {}).get("name", "N/A")

        if has_file:
            status = f"✅ Downloaded ({quality})"
        elif monitored:
            status = "⏳ Monitored (waiting for download)"
        else:
            status = "Not in library"

        lines.append(f"• **{name}** ({year}) — {status}")

    return "**Radarr Lookup:**\n" + "\n".join(lines)


async def get_system_status() -> str:
    """Get Radarr system health status."""
    status = await _get("/system/status")
    health = await _get("/health")

    version = status.get("version", "?")
    issues = [h.get("message", "") for h in health] if health else ["No issues"]

    return (
        f"**Radarr Status:** v{version}\n"
        f"**Health:** {'; '.join(issues)}"
    )
