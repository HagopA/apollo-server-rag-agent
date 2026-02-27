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
    MEDIA_REQUESTS_URL: str = os.getenv("MEDIA_REQUESTS_URL", "http://localhost:5055")
    MEDIA_REQUESTS_API_KEY: str = os.getenv("MEDIA_REQUESTS_API_KEY", "")

    MOVIE_SERVICE_URL: str = os.getenv("MOVIE_SERVICE_URL", "http://localhost:7878")
    MOVIE_SERVICE_API_KEY: str = os.getenv("MOVIE_SERVICE_API_KEY", "")

    TV_SERVICE_URL: str = os.getenv("TV_SERVICE_URL", "http://localhost:8989")
    TV_SERVICE_API_KEY: str = os.getenv("TV_SERVICE_API_KEY", "")

    ACTIVITY_SERVICE_URL: str = os.getenv("ACTIVITY_SERVICE_URL", "http://localhost:8181")
    ACTIVITY_SERVICE_API_KEY: str = os.getenv("ACTIVITY_SERVICE_API_KEY", "")

    # ChromaDB
    CHROMA_PERSIST_DIR: str = os.getenv("CHROMA_PERSIST_DIR", "./data/chromadb")
    CHROMA_COLLECTION: str = "apollo_docs"

    # Bot behavior
    BOT_NAME: str = os.getenv("BOT_NAME", "Apollo Assistant")
    RATE_LIMIT_PER_USER: int = int(os.getenv("RATE_LIMIT_PER_USER", "10"))
    MAX_CONVERSATION_HISTORY: int = int(os.getenv("MAX_CONVERSATION_HISTORY", "10"))
