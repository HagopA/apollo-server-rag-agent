"""Apollo Bot — Discord entry point.

A RAG-powered support chatbot for a private Plex media server.
Listens in a designated channel and creates threads for conversations.
"""

import asyncio
import time
import logging
from collections import defaultdict

import discord
from discord.ext import commands

from config import Config
from llm import chat

# ── Logging ─────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
log = logging.getLogger("apollo-bot")

# ── Rate limiter ────────────────────────────────────────────────────


class RateLimiter:
    """Simple per-user rate limiter using a sliding window."""

    def __init__(self, max_requests: int, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window = window_seconds
        self._timestamps: dict[int, list[float]] = defaultdict(list)

    def is_allowed(self, user_id: int) -> bool:
        now = time.time()
        # Prune old timestamps
        self._timestamps[user_id] = [
            t for t in self._timestamps[user_id] if now - t < self.window
        ]
        if len(self._timestamps[user_id]) >= self.max_requests:
            return False
        self._timestamps[user_id].append(now)
        return True


rate_limiter = RateLimiter(max_requests=Config.RATE_LIMIT_PER_USER)

# ── Conversation history (per-thread) ──────────────────────────────

# Maps thread_id -> list of {"role": ..., "content": ...}
thread_history: dict[int, list[dict]] = {}

# ── Discord bot setup ───────────────────────────────────────────────

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    log.info(f"✅ {Config.BOT_NAME} is online as {bot.user}")
    log.info(f"   Listening in channel ID: {Config.DISCORD_CHANNEL_ID}")


@bot.event
async def on_message(message: discord.Message):
    # Ignore own messages
    if message.author == bot.user:
        return

    # ── Determine if we should respond ──────────────────────────

    should_respond = False
    is_thread = isinstance(message.channel, discord.Thread)

    # Case 1: Message in the designated channel (not in a thread)
    if (
        not is_thread
        and hasattr(message.channel, "id")
        and message.channel.id == Config.DISCORD_CHANNEL_ID
    ):
        should_respond = True

    # Case 2: Message in a thread that the bot created
    if is_thread and message.channel.owner_id == bot.user.id:
        should_respond = True

    # Case 3: Bot is mentioned anywhere
    if bot.user in message.mentions:
        should_respond = True

    if not should_respond:
        await bot.process_commands(message)
        return

    # ── Rate limit check ────────────────────────────────────────

    if not rate_limiter.is_allowed(message.author.id):
        await message.reply(
            "⏳ You're sending messages too quickly. Please wait a moment.",
            mention_author=False,
        )
        return

    # ── Get or create thread ────────────────────────────────────

    thread = None
    if is_thread:
        thread = message.channel
    elif message.channel.id == Config.DISCORD_CHANNEL_ID:
        # Create a new thread for this conversation
        thread_name = message.content[:80] + ("..." if len(message.content) > 80 else "")
        try:
            thread = await message.create_thread(
                name=thread_name,
                auto_archive_duration=60,  # Archive after 1 hour of inactivity
            )
        except discord.HTTPException:
            # Fall back to replying in channel if thread creation fails
            thread = None

    # ── Build conversation history ──────────────────────────────

    channel_id = thread.id if thread else message.channel.id
    if channel_id not in thread_history:
        thread_history[channel_id] = []

    history = thread_history[channel_id]

    # ── Typing indicator + call Claude ──────────────────────────

    target = thread or message.channel
    async with target.typing():
        try:
            user_text = message.content.replace(f"<@{bot.user.id}>", "").strip()
            response_text = await chat(
                user_message=user_text,
                conversation_history=history if history else None,
            )

            # Update history
            history.append({"role": "user", "content": user_text})
            history.append({"role": "assistant", "content": response_text})

            # Trim history to max length
            max_h = Config.MAX_CONVERSATION_HISTORY * 2  # pairs
            if len(history) > max_h:
                thread_history[channel_id] = history[-max_h:]

        except Exception as e:
            log.error(f"Error processing message: {e}", exc_info=True)
            response_text = (
                "Sorry, I ran into an error processing your request. "
                "Please try again in a moment."
            )

    # ── Send response (split if > 2000 chars for Discord limit) ─

    for chunk in _split_message(response_text):
        if thread:
            await thread.send(chunk)
        else:
            await message.reply(chunk, mention_author=False)


def _split_message(text: str, max_len: int = 1900) -> list[str]:
    """Split a message into chunks that fit within Discord's character limit."""
    if len(text) <= max_len:
        return [text]

    chunks = []
    while text:
        if len(text) <= max_len:
            chunks.append(text)
            break
        # Try to split at a newline
        split_at = text.rfind("\n", 0, max_len)
        if split_at == -1:
            split_at = max_len
        chunks.append(text[:split_at])
        text = text[split_at:].lstrip("\n")

    return chunks


# ── Slash command: /status ──────────────────────────────────────────


@bot.command(name="status")
async def status_command(ctx: commands.Context):
    """Quick check: is the bot alive?"""
    await ctx.send(f"✅ **{Config.BOT_NAME}** is online and ready to help!")


@bot.command(name="ingest")
@commands.has_permissions(administrator=True)
async def ingest_command(ctx: commands.Context):
    """Re-ingest documentation (admin only)."""
    from rag import ingest_docs

    await ctx.send("📥 Re-ingesting documentation...")
    count = ingest_docs()
    await ctx.send(f"✅ Done! Ingested **{count}** chunks.")


# ── Main ────────────────────────────────────────────────────────────


def main():
    if not Config.DISCORD_BOT_TOKEN:
        log.error("❌ DISCORD_BOT_TOKEN is not set. Check your .env file.")
        return
    if not Config.ANTHROPIC_API_KEY:
        log.error("❌ ANTHROPIC_API_KEY is not set. Check your .env file.")
        return

    log.info(f"🚀 Starting {Config.BOT_NAME}...")
    bot.run(Config.DISCORD_BOT_TOKEN)


if __name__ == "__main__":
    main()
