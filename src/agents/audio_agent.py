"""
AudioAgent
----------

Responsible for:
- Transcribing audio
- Generating timestamped transcript chunks
- Producing structured AudioAnalysisOutput

This agent uses OpenAI Whisper via openai-whisper.
"""

from typing import List
import os

import whisper

from src.agents.base_agent import BaseAgent
from src.schemas.agent_outputs import (
    AudioAnalysisOutput,
    TranscriptChunk,
)
from config.config import (
    WHISPER_MODEL,
    AUDIO_CHUNK_SECONDS,
)


class AudioAgent(BaseAgent):
    """
    Agent that performs speech-to-text transcription
    on extracted audio files.
    """

    def __init__(
        self,
        media_id: str,
        audio_path: str,
        config: dict | None = None,
    ):
        super().__init__(
            agent_name="AudioAgent",
            media_id=media_id,
            config=config,
        )

        if not audio_path or not os.path.exists(audio_path):
            raise ValueError(f"Invalid audio path: {audio_path}")

        self.audio_path = audio_path

    # ------------------------------------------------------------------
    # Core execution
    # ------------------------------------------------------------------

    def execute(self) -> AudioAnalysisOutput:
        """
        Runs Whisper transcription and converts output
        into structured transcript chunks.
        """

        model = whisper.load_model(WHISPER_MODEL)

        result = model.transcribe(self.audio_path)

        if not result or not result.get("segments"):
            raise RuntimeError(
                "Whisper returned no transcription segments (audio may be silent or unsupported)"
            )

        segments = result.get("segments", [])
        language = result.get("language")

        transcript_chunks: List[TranscriptChunk] = []
        full_transcript_parts: List[str] = []

        for segment in segments:
            text = segment.get("text", "").strip()
            start = float(segment.get("start", 0.0))
            end = float(segment.get("end", 0.0))

            if not text:
                continue

            transcript_chunks.append(
                TranscriptChunk(
                    text=text,
                    start_time=start,
                    end_time=end,
                    speaker=None,  # diarization can be added later
                )
            )

            full_transcript_parts.append(text)

        full_transcript = " ".join(full_transcript_parts)

        duration_seconds = (
            transcript_chunks[-1].end_time
            if transcript_chunks
            else None
        )

        return AudioAnalysisOutput(
            agent_name=self.agent_name,
            media_id=self.media_id,
            success=True,
            language=language,
            duration_seconds=duration_seconds,
            transcript_chunks=transcript_chunks,
            full_transcript=full_transcript,
        )
