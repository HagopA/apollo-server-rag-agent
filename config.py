"""Centralized configuration loaded from environment variables."""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Discord
    DISCORD_BOT_TOKEN: str = os.getenv("DISCORD_BOT_TOKEN", "")
    DISCORD_CHANNEL_ID: int = int(os.getenv("DISCORD_CHANNEL_ID", "0"))

    # Anthropic
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    CLAUDE_MODEL: str = "claude-sonnet-4-5-20250929"
    CLAUDE_MAX_TOKENS: int = 1024

    # Service URLs & Keys
    SEERR_URL: str = os.getenv("SEERR_URL", "http://localhost:5055")
    SEERR_API_KEY: str = os.getenv("SEERR_API_KEY", "")

    RADARR_URL: str = os.getenv("RADARR_URL", "http://localhost:7878")
    RADARR_API_KEY: str = os.getenv("RADARR_API_KEY", "")

    SONARR_URL: str = os.getenv("SONARR_URL", "http://localhost:8989")
    SONARR_API_KEY: str = os.getenv("SONARR_API_KEY", "")

    TAUTULLI_URL: str = os.getenv("TAUTULLI_URL", "http://localhost:8181")
    TAUTULLI_API_KEY: str = os.getenv("TAUTULLI_API_KEY", "")

    # ChromaDB
    CHROMA_PERSIST_DIR: str = os.getenv("CHROMA_PERSIST_DIR", "./data/chromadb")
    CHROMA_COLLECTION: str = "apollo_docs"

    # Bot behavior
    BOT_NAME: str = os.getenv("BOT_NAME", "Apollo Assistant")
    RATE_LIMIT_PER_USER: int = int(os.getenv("RATE_LIMIT_PER_USER", "10"))
    MAX_CONVERSATION_HISTORY: int = int(os.getenv("MAX_CONVERSATION_HISTORY", "10"))
