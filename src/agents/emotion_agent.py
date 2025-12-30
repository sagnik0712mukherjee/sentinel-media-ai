"""
EmotionAgent
------------

Responsible for:
- Analyzing emotional tone from transcript text
- Detecting emotion spikes over time
- Producing structured EmotionAnalysisOutput

This agent operates purely on text (from AudioAgent output).
"""

from typing import List

from src.agents.base_agent import BaseAgent
from src.schemas.agent_outputs import (
    EmotionAnalysisOutput,
    EmotionSpike,
    TranscriptChunk,
)
from config.config import TEXT_MODEL
from openai import OpenAI


class EmotionAgent(BaseAgent):
    """
    Agent that analyzes emotional tone and detects
    emotion spikes from transcript chunks.
    """

    def __init__(
        self,
        media_id: str,
        transcript_chunks: List[TranscriptChunk],
        config: dict | None = None,
    ):
        super().__init__(
            agent_name="EmotionAgent",
            media_id=media_id,
            config=config,
        )

        if not transcript_chunks:
            raise ValueError("Transcript chunks are required for EmotionAgent")

        self.transcript_chunks = transcript_chunks
        self.client = OpenAI()

    # ------------------------------------------------------------------
    # Core execution
    # ------------------------------------------------------------------

    def execute(self) -> EmotionAnalysisOutput:
        """
        Uses LLM reasoning to detect emotional tone
        and emotion spikes across the transcript.
        """

        # Combine transcript with timestamps
        transcript_text = "\n".join(
            f"[{chunk.start_time:.1f}s - {chunk.end_time:.1f}s] {chunk.text}"
            for chunk in self.transcript_chunks
        )

        prompt = self._build_prompt(transcript_text)

        response = self.client.chat.completions.create(
            model=TEXT_MODEL,
            messages=[
                {"role": "system", "content": "You are an expert emotion analysis AI."},
                {"role": "user", "content": prompt},
            ]
        )

        content = response.choices[0].message.content

        # Parse response
        dominant_emotion, emotion_spikes = self._parse_response(content)

        return EmotionAnalysisOutput(
            agent_name=self.agent_name,
            media_id=self.media_id,
            success=True,
            dominant_emotion=dominant_emotion,
            emotion_spikes=emotion_spikes,
        )

    # ------------------------------------------------------------------
    # Prompting
    # ------------------------------------------------------------------

    def _build_prompt(self, transcript_text: str) -> str:
        return f"""
            Analyze the emotional tone of the following transcript.

            Tasks:
            1. Identify the dominant overall emotion (single word).
            2. Detect moments where emotion noticeably spikes.

            For each spike, provide:
            - timestamp (in seconds)
            - emotion (e.g. anger, excitement, sadness, neutral)
            - intensity (0.0 to 1.0)
            - short explanation

            Respond STRICTLY in JSON format:

            {{
            "dominant_emotion": "<emotion>",
            "emotion_spikes": [
                {{
                "timestamp": 12.3,
                "emotion": "anger",
                "intensity": 0.8,
                "evidence": "raised voice while discussing pricing"
                }}
            ]
            }}

            Transcript:
            {transcript_text}
        """

    # ------------------------------------------------------------------
    # Parsing
    # ------------------------------------------------------------------

    def _parse_response(self, content: str):
        """
        Parses LLM JSON output into schema objects.
        """

        import json

        content = content.strip().strip("```json").strip("```")
        data = json.loads(content)


        dominant_emotion = data.get("dominant_emotion")
        spikes_raw = data.get("emotion_spikes", [])

        emotion_spikes: List[EmotionSpike] = []

        for spike in spikes_raw:
            emotion_spikes.append(
                EmotionSpike(
                    timestamp=spike.get("timestamp"),
                    emotion=spike.get("emotion"),
                    intensity=spike.get("intensity"),
                    evidence=spike.get("evidence"),
                )
            )

        return dominant_emotion, emotion_spikes
