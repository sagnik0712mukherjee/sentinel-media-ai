"""
RiskAgent
---------

Responsible for:
- Identifying potential risks in media content
- Assessing severity and category
- Suggesting mitigation or actions

Adds enterprise-grade intelligence.
"""

from typing import List, Optional
import json
from openai import OpenAI
from src.schemas.agent_outputs import RiskFlag

from src.agents.base_agent import BaseAgent
from src.schemas.agent_outputs import RiskAssessmentOutput
from config.config import TEXT_MODEL


class RiskAgent(BaseAgent):
    """
    Agent that evaluates content for risk, compliance,
    and reputational concerns.
    """

    def __init__(
        self,
        media_id: str,
        transcript_text: str,
        conclusions: Optional[List[str]] = None,
        topics: Optional[List[str]] = None,
        entities: Optional[List[str]] = None,
        config: dict | None = None,
    ):
        super().__init__(
            agent_name="RiskAgent",
            media_id=media_id,
            config=config,
        )

        if not transcript_text.strip():
            raise ValueError("Transcript text is required for RiskAgent")

        self.transcript_text = transcript_text
        self.conclusions = conclusions or []
        self.topics = topics or []
        self.entities = entities or []

        self.client = OpenAI()

    # ------------------------------------------------------------------
    # Core execution
    # ------------------------------------------------------------------

    def execute(self) -> RiskAssessmentOutput:
        MAX_CHARS = 4000  # risk analysis can be smaller

        transcript = self.transcript_text
        if len(transcript) > MAX_CHARS:
            transcript = transcript[:MAX_CHARS]

        prompt = self._build_prompt(transcript)

        response = self.client.chat.completions.create(
            model=TEXT_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI compliance and risk analysis expert.",
                },
                {"role": "user", "content": prompt},
            ]
        )

        content = response.choices[0].message.content
        risk_level, categories, explanation, actions = self._parse_response(content)

        flags = []

        for category in categories:
            flags.append(
                RiskFlag(
                    category=category,
                    description=explanation,
                    severity=risk_level,
                    timestamp=None,  # can be added later if needed
                )
            )

        return RiskAssessmentOutput(
            agent_name=self.agent_name,
            media_id=self.media_id,
            success=True,
            overall_risk_level=risk_level,
            risk_flags=flags,
        )

    # ------------------------------------------------------------------
    # Prompting
    # ------------------------------------------------------------------

    def _build_prompt(self, transcript) -> str:
        return f"""
            Evaluate the following media content for potential risks.

            Transcript:
            {transcript}

            Conclusions:
            {self.conclusions}

            Topics:
            {self.topics}

            Entities:
            {self.entities}

            Risk Categories to consider:
            - compliance
            - misinformation
            - safety
            - reputational
            - ethical
            - legal

            Tasks:
            1. Assign an OVERALL RISK LEVEL: low, medium, or high.
            2. Identify applicable RISK CATEGORIES.
            3. Briefly explain the risk.
            4. Suggest RECOMMENDED ACTIONS.

            Rules:
            - Be objective
            - Be conservative
            - Avoid speculation
            - No moralizing

            Respond STRICTLY in JSON format:

            {{
            "risk_level": "low|medium|high",
            "risk_categories": ["category1", "category2"],
            "explanation": "string",
            "recommended_actions": ["action1", "action2"]
            }}
        """

    # ------------------------------------------------------------------
    # Parsing
    # ------------------------------------------------------------------

    def _parse_response(self, content: str):

        try:
            cleaned = content.strip().strip("```json").strip("```")
            data = json.loads(cleaned)
        except Exception:
            # Absolute fallback – never crash pipeline
            return (
                "low",
                [],
                "Unable to reliably assess risk from the content.",
                [],
            )

        risk_level = data.get("risk_level", "low")
        risk_categories = data.get("risk_categories", [])
        explanation = data.get("explanation", "")
        recommended_actions = data.get("recommended_actions", [])

        # Final contract: ALWAYS return 4 values
        return (
            risk_level,
            risk_categories,
            explanation,
            recommended_actions,
        )

