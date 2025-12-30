"""
Schemas defining media-level metadata.

These schemas represent the canonical definition of
audio/video objects flowing through the system.
"""

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class MediaMetadata(BaseModel):
    media_id: str = Field(..., description="Unique identifier for the media")
    media_type: str = Field(..., description="audio | video")
    source: str = Field(..., description="upload | youtube")
    original_filename: Optional[str] = None
    source_url: Optional[str] = None

    duration_seconds: Optional[float] = None
    language: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)

    # File paths
    media_path: Optional[str] = None
    audio_path: Optional[str] = None

    # Processing state
    processed: bool = False
    processing_metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)
