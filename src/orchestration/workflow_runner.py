"""
Workflow Runner
---------------

Executes the agent graph in order,
passing outputs between agents and
persisting outputs where required.
"""

from typing import Dict, Any

from src.orchestration.agent_graph import AgentGraph

from src.agents.audio_agent import AudioAgent
from src.agents.emotion_agent import EmotionAgent
from src.agents.tagging_agent import TaggingAgent
from src.agents.video_agent import VideoAgent
from src.agents.reasoning_agent import ReasoningAgent
from src.agents.risk_agent import RiskAgent

from src.storage.elastic.es_client import get_es_client
from config.config import (
    ENABLE_VIDEO_AGENT,
    ENABLE_EMOTION_AGENT,
    ENABLE_RISK_AGENT,
    MEDIA_TRANSCRIPTS_INDEX,
)


class WorkflowRunner:
    """
    Central orchestrator for executing
    the agent pipeline.
    """

    def __init__(self, media_id: str):
        self.media_id = media_id
        self.graph = AgentGraph()
        self.context: Dict[str, Any] = {}
        self.es = get_es_client()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run(
        self,
        audio_path: str,
        frame_paths: list[str] | None = None,
    ) -> Dict[str, Any]:
        """
        Executes the full agent pipeline.
        """

        for agent_name in self.graph.execution_order():
            self._run_agent(agent_name, audio_path, frame_paths)

        return self.context

    # ------------------------------------------------------------------
    # Agent execution
    # ------------------------------------------------------------------

    def _run_agent(
        self,
        agent_name: str,
        audio_path: str,
        frame_paths: list[str] | None,
    ):
        # --------------------------------------------------
        # Audio Agent
        # --------------------------------------------------
        if agent_name == "AudioAgent":
            agent = AudioAgent(
                media_id=self.media_id,
                audio_path=audio_path,
            )
            output = agent.run()
            self.context["audio"] = output

            # ✅ Persist transcript chunks to Elasticsearch (RAG backbone)
            if output.success and output.transcript_chunks:
                for chunk in output.transcript_chunks:
                    self.es.index(
                        index=MEDIA_TRANSCRIPTS_INDEX,
                        document={
                            "media_id": self.media_id,
                            "text": chunk.text,
                            "start_time": chunk.start_time,
                            "end_time": chunk.end_time,
                        },
                    )

        # --------------------------------------------------
        # Emotion Agent
        # --------------------------------------------------
        elif agent_name == "EmotionAgent" and ENABLE_EMOTION_AGENT:
            agent = EmotionAgent(
                media_id=self.media_id,
                transcript_chunks=self.context["audio"].transcript_chunks,
            )
            output = agent.run()
            self.context["emotion"] = output

        # --------------------------------------------------
        # Tagging Agent
        # --------------------------------------------------
        elif agent_name == "TaggingAgent":
            agent = TaggingAgent(
                media_id=self.media_id,
                transcript_text=self.context["audio"].full_transcript,
            )
            output = agent.run()
            self.context["tagging"] = output

        # --------------------------------------------------
        # Video Agent
        # --------------------------------------------------
        elif agent_name == "VideoAgent" and ENABLE_VIDEO_AGENT:
            if frame_paths:
                agent = VideoAgent(
                    media_id=self.media_id,
                    frame_paths=frame_paths,
                )
                output = agent.run()
                self.context["video"] = output

        # --------------------------------------------------
        # Reasoning Agent
        # --------------------------------------------------
        elif agent_name == "ReasoningAgent":
            agent = ReasoningAgent(
                media_id=self.media_id,
                transcript_text=self.context["audio"].full_transcript,
                emotions=(
                    self.context.get("emotion").emotion_spikes
                    if ENABLE_EMOTION_AGENT and self.context.get("emotion")
                    else []
                ),
                topics=self.context.get("tagging").topics,
                entities=self.context.get("tagging").entities,
            )
            output = agent.run()
            self.context["reasoning"] = output

        # --------------------------------------------------
        # Risk Agent
        # --------------------------------------------------
        elif agent_name == "RiskAgent" and ENABLE_RISK_AGENT:
            agent = RiskAgent(
                media_id=self.media_id,
                transcript_text=self.context["audio"].full_transcript,
                conclusions=self.context.get("reasoning").decisions
                if self.context.get("reasoning")
                else [],
                topics=self.context.get("tagging").topics,
                entities=self.context.get("tagging").entities,
            )
            output = agent.run()
            self.context["risk"] = output
