"""
ReasoningAgent
--------------

Responsible for:
- High-level interpretation of media content
- Deriving insights, intent, and conclusions
- Synthesizing signals from multiple agents

This agent represents the "thinking" layer.
"""

from typing import Optional, List

from openai import OpenAI

from src.agents.base_agent import BaseAgent
from src.schemas.agent_outputs import ReasoningOutput
from config.config import TEXT_MODEL


class ReasoningAgent(BaseAgent):
    """
    Agent that performs semantic reasoning and insight generation
    over media content and agent signals.
    """

    def __init__(
        self,
        media_id: str,
        transcript_text: str,
        emotions: Optional[List[str]] = None,
        topics: Optional[List[str]] = None,
        entities: Optional[List[str]] = None,
        config: dict | None = None,
    ):
        super().__init__(
            agent_name="ReasoningAgent",
            media_id=media_id,
            config=config,
        )

        if not transcript_text.strip():
            raise ValueError("Transcript text is required for ReasoningAgent")

        self.transcript_text = transcript_text
        self.emotions = emotions or []
        self.topics = topics or []
        self.entities = entities or []

        self.client = OpenAI()

    # ------------------------------------------------------------------
    # Core execution
    # ------------------------------------------------------------------

    def execute(self) -> ReasoningOutput:
        MAX_CHARS = 6000

        transcript = self.transcript_text
        if len(transcript) > MAX_CHARS:
            transcript = transcript[:MAX_CHARS]

        prompt = self._build_prompt(transcript)


        response = self.client.chat.completions.create(
            model=TEXT_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a senior analyst AI capable of deep reasoning.",
                },
                {"role": "user", "content": prompt},
            ]
        )

        content = response.choices[0].message.content
        insights, intent, conclusions = self._parse_response(content)

        return ReasoningOutput(
            agent_name=self.agent_name,
            media_id=self.media_id,
            success=True,
            summary=intent,
            key_themes=self.topics,
            insights=[
                {"insight": insight} if isinstance(insight, str) else insight
                for insight in insights
            ],
            decisions=conclusions,
        )


    # ------------------------------------------------------------------
    # Prompting
    # ------------------------------------------------------------------

    def _build_prompt(self, transcript) -> str:
        return f"""
            Analyze the following media content and agent signals.

            Transcript:
            {transcript}

            Detected Emotions:
            {self.emotions}

            Detected Topics:
            {self.topics}

            Detected Entities:
            {self.entities}

            Tasks:
            1. Identify the PRIMARY INTENT of the speaker/content.
            2. Generate 3–5 KEY INSIGHTS.
            3. Provide 2–3 HIGH-LEVEL CONCLUSIONS.

            Rules:
            - Be concise
            - Be analytical
            - Avoid repeating transcript verbatim
            - No explanations

            Respond STRICTLY in JSON format:

            {{
            "intent": "string",
            "key_insights": ["insight1", "insight2"],
            "conclusions": ["conclusion1", "conclusion2"]
            }}
        """

    # ------------------------------------------------------------------
    # Parsing
    # ------------------------------------------------------------------

    def _parse_response(self, content: str):
        import json

        content = content.strip().strip("```json").strip("```")
        data = json.loads(content)


        intent = data.get("intent", "")
        key_insights = data.get("key_insights", [])
        conclusions = data.get("conclusions", [])

        return key_insights, intent, conclusions
