"""
TaggingAgent
------------

Responsible for:
- Extracting high-level topics
- Identifying named entities
- Generating search-friendly keywords

Operates on transcript text.
"""

from typing import List

from openai import OpenAI

from src.agents.base_agent import BaseAgent
from src.schemas.agent_outputs import TaggingOutput
from config.config import TEXT_MODEL


class TaggingAgent(BaseAgent):
    """
    Agent that extracts topics, entities, and keywords
    from transcript content.
    """

    def __init__(
        self,
        media_id: str,
        transcript_text: str,
        config: dict | None = None,
    ):
        super().__init__(
            agent_name="TaggingAgent",
            media_id=media_id,
            config=config,
        )

        if not transcript_text.strip():
            raise ValueError("Transcript text is required for TaggingAgent")

        self.transcript_text = transcript_text
        self.client = OpenAI()

    # ------------------------------------------------------------------
    # Core execution
    # ------------------------------------------------------------------

    def execute(self) -> TaggingOutput:
        prompt = self._build_prompt(self.transcript_text)

        response = self.client.chat.completions.create(
            model=TEXT_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert information extraction AI.",
                },
                {"role": "user", "content": prompt},
            ]
        )

        content = response.choices[0].message.content
        topics, entities, keywords = self._parse_response(content)

        return TaggingOutput(
            agent_name=self.agent_name,
            media_id=self.media_id,
            success=True,
            topics=topics,
            entities=entities,
            keywords=keywords,
        )

    # ------------------------------------------------------------------
    # Prompting
    # ------------------------------------------------------------------

    def _build_prompt(self, transcript_text: str) -> str:
        return f"""
            Extract structured metadata from the following transcript.

            Tasks:
            1. Identify 5–8 high-level TOPICS.
            2. Identify important NAMED ENTITIES (people, companies, products, locations).
            3. Identify concise SEARCH KEYWORDS (single words or short phrases).

            Rules:
            - Be concise
            - Avoid duplicates
            - Use lowercase
            - No explanations

            Respond STRICTLY in JSON format:

            {{
            "topics": ["topic1", "topic2"],
            "entities": ["entity1", "entity2"],
            "keywords": ["keyword1", "keyword2"]
            }}

            Transcript:
            {transcript_text}
        """

    # ------------------------------------------------------------------
    # Parsing
    # ------------------------------------------------------------------

    def _parse_response(self, content: str):
        import json

        content = content.strip().strip("```json").strip("```")
        data = json.loads(content)


        topics: List[str] = data.get("topics", [])
        entities: List[str] = data.get("entities", [])
        keywords: List[str] = data.get("keywords", [])

        return topics, entities, keywords
