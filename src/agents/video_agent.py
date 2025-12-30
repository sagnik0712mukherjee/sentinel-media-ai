"""
VideoAgent
----------

Responsible for:
- Analyzing visual content from videos
- Generating scene-level summaries
- Extracting visual tags and activities

Uses sampled frames for efficiency.
"""

from typing import List

from openai import OpenAI

from src.agents.base_agent import BaseAgent
from src.schemas.agent_outputs import VideoAnalysisOutput
from config import config


class VideoAgent(BaseAgent):
    """
    Agent that performs high-level visual analysis
    on sampled video frames.
    """

    def __init__(
        self,
        media_id: str,
        frame_paths: List[str],
        config: dict | None = None,
    ):
        super().__init__(
            agent_name="VideoAgent",
            media_id=media_id,
            config=config,
        )

        if not frame_paths:
            raise ValueError("At least one frame path is required for VideoAgent")

        self.frame_paths = frame_paths
        self.client = OpenAI()

    # ------------------------------------------------------------------
    # Core execution
    # ------------------------------------------------------------------

    def execute(self) -> VideoAnalysisOutput:

        prompt = self._build_prompt()

        response = self.client.chat.completions.create(
            model=config.VISION_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert computer vision analyst.",
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        *[
                            {
                                "type": "image_url",
                                "image_url": {"url": self._file_to_data_url(fp)},
                            }
                            for fp in self.frame_paths
                        ],
                    ],
                },
            ]
        )

        content = response.choices[0].message.content
        scenes, tags, activities = self._parse_response(content)

        return VideoAnalysisOutput(
            agent_name=self.agent_name,
            media_id=self.media_id,
            success=True,
            scene_summaries=scenes,
            visual_tags=tags,
            detected_activities=activities,
        )

    # ------------------------------------------------------------------
    # Prompting
    # ------------------------------------------------------------------

    def _build_prompt(self) -> str:
        return """
            Analyze the provided video frames.

            Tasks:
            1. Summarize the scenes depicted across frames.
            2. Identify visual tags (objects, environments, settings).
            3. Identify detected activities or actions.

            Rules:
            - Be concise
            - Avoid speculation
            - Use lowercase
            - No explanations

            Respond STRICTLY in JSON format:

            {
            "scene_summaries": ["scene 1", "scene 2"],
            "visual_tags": ["tag1", "tag2"],
            "detected_activities": ["activity1", "activity2"]
            }
        """

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------

    def _file_to_data_url(self, file_path: str) -> str:
        """
        Converts local image file to data URL
        for OpenAI vision input.
        """
        import base64
        import mimetypes

        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type is None:
            mime_type = "image/jpeg"

        with open(file_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")

        return f"data:{mime_type};base64,{encoded}"

    # ------------------------------------------------------------------
    # Parsing
    # ------------------------------------------------------------------

    def _parse_response(self, content: str):
        import json

        content = content.strip().strip("```json").strip("```")
        data = json.loads(content)


        scenes = data.get("scene_summaries", [])
        tags = data.get("visual_tags", [])
        activities = data.get("detected_activities", [])

        return scenes, tags, activities
