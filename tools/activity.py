"""Activity monitoring service API wrapper for Apollo Bot tool calls."""

import aiohttp
from config import Config


async def _get(cmd: str, params: dict | None = None) -> dict:
    """Make a GET request to the activity monitoring API."""
    url = f"{Config.ACTIVITY_SERVICE_URL}/api/v2"
    base_params = {"apikey": Config.ACTIVITY_SERVICE_API_KEY, "cmd": cmd}
    if params:
        base_params.update(params)
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=base_params) as resp:
            resp.raise_for_status()
            data = await resp.json()
            return data.get("response", {}).get("data", {})


async def get_activity() -> str:
    """Get current Plex streaming activity."""
    data = await _get("get_activity")
    sessions = data.get("sessions", [])
    stream_count = data.get("stream_count", 0)

    if not sessions:
        return "No one is currently streaming on Plex."

    lines = [f"**Currently Streaming ({stream_count} active):**"]
    for s in sessions:
        user = s.get("friendly_name", "Unknown")
        title = s.get("full_title", "Unknown")
        state = s.get("state", "unknown")
        quality = s.get("quality_profile", "?")
        transcode = "transcoding" if s.get("transcode_decision") == "transcode" else "direct play"
        lines.append(f"• **{user}**: {title} ({state}) — {quality}, {transcode}")

    return "\n".join(lines)


async def get_recently_added(count: int = 5) -> str:
    """Get recently added media to Plex."""
    data = await _get("get_recently_added", {"count": count})
    items = data.get("recently_added", [])

    if not items:
        return "No recently added media found."

    lines = ["**Recently Added to Plex:**"]
    for item in items:
        title = item.get("full_title") or item.get("title", "Unknown")
        media_type = item.get("media_type", "?")
        added = item.get("added_at", "?")
        lines.append(f"• **{title}** [{media_type}]")

    return "\n".join(lines)


async def get_server_info() -> str:
    """Get Plex server info."""
    data = await _get("get_server_info")
    name = data.get("pms_name", "Unknown")
    version = data.get("pms_version", "?")
    platform = data.get("pms_platform", "?")

    return (
        f"**Plex Server:** {name}\n"
        f"**Version:** {version}\n"
        f"**Platform:** {platform}"
    )
