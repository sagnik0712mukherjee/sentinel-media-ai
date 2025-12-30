"""
Database Models
---------------

Defines ORM-style models for session
and media metadata storage.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class MediaRecord(BaseModel):
    media_id: str
    title: Optional[str] = None
    source: str  # local | youtube
    created_at: datetime = datetime.utcnow()


class ChatSession(BaseModel):
    session_id: str
    media_id: str
    created_at: datetime = datetime.utcnow()

