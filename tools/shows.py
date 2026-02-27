"""TV show service API wrapper for Apollo Bot tool calls."""

import aiohttp
from config import Config

HEADERS = {
    "X-Api-Key": Config.TV_SERVICE_API_KEY,
    "Content-Type": "application/json",
}


async def _get(endpoint: str, params: dict | None = None) -> dict | list:
    url = f"{Config.TV_SERVICE_URL}/api/v3{endpoint}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=HEADERS, params=params) as resp:
            resp.raise_for_status()
            return await resp.json()


async def get_queue() -> str:
    """Get the current TV Show download queue."""
    data = await _get("/queue", params={"pageSize": 10, "sortKey": "progress", "sortDirection": "ascending"})
    records = data.get("records", [])

    if not records:
        return "The TV Show download queue is empty — no episodes are currently downloading."

    lines = []
    for item in records:
        title = item.get("title", "Unknown")
        series = item.get("series", {}).get("title", "")
        episode = item.get("episode", {})
        ep_info = f"S{episode.get('seasonNumber', '?'):02d}E{episode.get('episodeNumber', '?'):02d}"
        status = item.get("status", "unknown")
        size = item.get("size", 1)
        sizeleft = item.get("sizeleft", 0)
        pct = round((1 - sizeleft / size) * 100, 1) if size > 0 else 0
        time_left = item.get("timeleft", "unknown")
        lines.append(f"• **{series}** {ep_info} — {status} | {pct}% done | ETA: {time_left}")

    return "**TV Show Download Queue:**\n" + "\n".join(lines)


async def lookup_series(title: str) -> str:
    """Look up a TV series in TV Show's library."""
    results = await _get("/series/lookup", params={"term": title})

    if not results:
        return f"No series found matching '{title}' in TV Show."

    lines = []
    for series in results[:3]:
        name = series.get("title", "Unknown")
        year = series.get("year", "?")
        monitored = series.get("monitored", False)
        stats = series.get("statistics", {})
        ep_count = stats.get("episodeFileCount", 0)
        total = stats.get("totalEpisodeCount", 0)

        if ep_count > 0:
            status = f"✅ {ep_count}/{total} episodes downloaded"
        elif monitored:
            status = "⏳ Monitored (waiting for episodes)"
        else:
            status = "Not in library"

        lines.append(f"• **{name}** ({year}) — {status}")

    return "**TV Show Lookup:**\n" + "\n".join(lines)


async def get_system_status() -> str:
    """Get TV Show system health status."""
    status = await _get("/system/status")
    health = await _get("/health")

    version = status.get("version", "?")
    issues = [h.get("message", "") for h in health] if health else ["No issues"]

    return (
        f"**TV Show Status:** v{version}\n"
        f"**Health:** {'; '.join(issues)}"
    )
