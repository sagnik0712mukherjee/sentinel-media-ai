"""
Global configuration for Sentinel Media AI.

This file centralizes:
- Model choices
- Chunking parameters
- Index names
- Paths
- Feature toggles

Nothing in here should contain business logic.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# -------------------------------------------------------------------
# Environment
# -------------------------------------------------------------------

load_dotenv()

PROJECT_NAME = "Sentinel Media AI"
ENVIRONMENT = os.getenv("ENVIRONMENT", "local")

# -------------------------------------------------------------------
# Base Paths
# -------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
MEDIA_DIR = DATA_DIR / "media"
TMP_DIR = DATA_DIR / "tmp"

MEDIA_DIR.mkdir(parents=True, exist_ok=True)
TMP_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------------------
# OpenAI / LLM Configuration
# -------------------------------------------------------------------

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Default models (can be swapped easily)
TEXT_MODEL = os.getenv("TEXT_MODEL", "gpt-5-mini")
REASONING_MODEL = os.getenv("REASONING_MODEL", "gpt-5-mini")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "medium")
# Vision model (used by VideoAgent / multimodal reasoning)
VISION_MODEL = os.getenv("VISION_MODEL", "gpt-5-mini")

# -------------------------------------------------------------------
# Chunking Configuration
# -------------------------------------------------------------------

# Audio chunking
AUDIO_CHUNK_SECONDS = int(os.getenv("AUDIO_CHUNK_SECONDS", 45))
AUDIO_CHUNK_OVERLAP = int(os.getenv("AUDIO_CHUNK_OVERLAP", 5))

# Video frame sampling
FRAME_SAMPLE_INTERVAL_SECONDS = int(
    os.getenv("FRAME_SAMPLE_INTERVAL_SECONDS", 5)
)

# -------------------------------------------------------------------
# Elasticsearch Configuration
# -------------------------------------------------------------------

ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL")
ELASTICSEARCH_USER = os.getenv("ELASTICSEARCH_USER")
ELASTICSEARCH_PASSWORD = os.getenv("ELASTICSEARCH_PASSWORD")

# Index names
MEDIA_TRANSCRIPTS_INDEX = "sentinel_media_transcripts"
MEDIA_SCENES_INDEX = "sentinel_media_scenes"
MEDIA_INSIGHTS_INDEX = "sentinel_media_insights"

# -------------------------------------------------------------------
# Agent Configuration
# -------------------------------------------------------------------

# Used for orchestration & logging
AGENT_TIMEOUT_SECONDS = int(os.getenv("AGENT_TIMEOUT_SECONDS", 120))

# Toggle agents on/off easily
ENABLE_VIDEO_AGENT = True
ENABLE_EMOTION_AGENT = True
ENABLE_RISK_AGENT = True

# -------------------------------------------------------------------
# RAG / Chat Configuration
# -------------------------------------------------------------------

RAG_TOP_K = int(os.getenv("RAG_TOP_K", 6))
MAX_CHAT_HISTORY = int(os.getenv("MAX_CHAT_HISTORY", 10))

# -------------------------------------------------------------------
# Logging
# -------------------------------------------------------------------

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

