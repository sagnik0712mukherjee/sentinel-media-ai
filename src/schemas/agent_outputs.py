"""
Schemas defining structured outputs produced by agents.

All agent outputs MUST conform to one of these schemas.
This enables:
- Validation
- Debugging
- Safe indexing
- Predictable orchestration
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


# -------------------------------------------------------------------
# Base Agent Output
# -------------------------------------------------------------------

class BaseAgentOutput(BaseModel):
    agent_name: str = Field(..., description="Name of the agent")
    media_id: str = Field(..., description="Unique media identifier")
    success: bool = Field(..., description="Whether agent execution succeeded")
    error_message: Optional[str] = Field(
        None, description="Error message if success=False"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default_factory=dict, description="Additional debug or trace metadata"
    )


# -------------------------------------------------------------------
# Audio Agent Output
# -------------------------------------------------------------------

class TranscriptChunk(BaseModel):
    text: str
    start_time: float
    end_time: float
    speaker: Optional[str] = None


class AudioAnalysisOutput(BaseAgentOutput):
    language: Optional[str] = None
    duration_seconds: Optional[float] = None
    transcript_chunks: List[TranscriptChunk] = Field(default_factory=list)
    full_transcript: Optional[str] = None


# -------------------------------------------------------------------
# Video Agent Output
# -------------------------------------------------------------------

class SceneDescription(BaseModel):
    scene_id: int
    start_time: float
    end_time: float
    description: str
    key_objects: Optional[List[str]] = None


class VideoAnalysisOutput(BaseAgentOutput):
    total_scenes: int = 0
    scenes: List[SceneDescription] = Field(default_factory=list)


# -------------------------------------------------------------------
# Emotion Agent Output
# -------------------------------------------------------------------

class EmotionSpike(BaseModel):
    timestamp: float
    emotion: str
    intensity: float  # 0.0 - 1.0
    evidence: Optional[str] = None


class EmotionAnalysisOutput(BaseAgentOutput):
    dominant_emotion: Optional[str] = None
    emotion_spikes: List[EmotionSpike] = Field(default_factory=list)


# -------------------------------------------------------------------
# Reasoning Agent Output
# -------------------------------------------------------------------

class ReasoningInsight(BaseModel):
    insight: str
    evidence: Optional[str] = None
    confidence: Optional[float] = None  # 0.0 - 1.0


class ReasoningOutput(BaseAgentOutput):
    summary: Optional[str] = None
    key_themes: List[str] = Field(default_factory=list)
    insights: List[ReasoningInsight] = Field(default_factory=list)
    decisions: List[str] = Field(default_factory=list)


# -------------------------------------------------------------------
# Tagging Agent Output
# -------------------------------------------------------------------

class TaggingOutput(BaseAgentOutput):
    topics: List[str] = Field(default_factory=list)
    entities: List[str] = Field(default_factory=list)
    keywords: List[str] = Field(default_factory=list)


# -------------------------------------------------------------------
# Risk Agent Output
# -------------------------------------------------------------------

class RiskFlag(BaseModel):
    category: str
    description: str
    severity: str  # low / medium / high
    timestamp: Optional[float] = None


class RiskAssessmentOutput(BaseAgentOutput):
    overall_risk_level: Optional[str] = None
    risk_flags: List[RiskFlag] = Field(default_factory=list)


# -------------------------------------------------------------------
# RAG Chat Agent Output
# -------------------------------------------------------------------

class ChatCitation(BaseModel):
    source: str
    start_time: Optional[float] = None
    end_time: Optional[float] = None


class RAGChatOutput(BaseAgentOutput):
    answer: str
    citations: List[ChatCitation] = Field(default_factory=list)
