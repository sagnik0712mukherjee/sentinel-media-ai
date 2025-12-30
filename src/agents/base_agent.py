"""
BaseAgent defines the standard lifecycle and contract
for all agent implementations in Sentinel Media AI.

All agents MUST inherit from this class.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from datetime import datetime
import traceback
import uuid

from src.schemas.agent_outputs import BaseAgentOutput
from config.config import AGENT_TIMEOUT_SECONDS
from typing import TypeVar

T = TypeVar("T", bound=BaseAgentOutput)


class BaseAgent(ABC):
    """
    Abstract base class for all agents.

    Responsibilities:
    - Enforce a standard run lifecycle
    - Capture success / failure
    - Attach metadata & trace info
    - Return structured outputs only
    """

    def __init__(
        self,
        agent_name: str,
        media_id: str,
        config: Optional[Dict[str, Any]] = None,
    ):
        self.agent_name = agent_name
        self.media_id = media_id
        self.config = config or {}

        # Traceability
        self.run_id = str(uuid.uuid4())
        self.started_at: Optional[datetime] = None
        self.finished_at: Optional[datetime] = None

    # ------------------------------------------------------------------
    # Public API (DO NOT override)
    # ------------------------------------------------------------------

    def run(self) -> T:
        """
        Executes the agent with standardized lifecycle management.

        This method should NEVER be overridden by child classes.
        """
        self.started_at = datetime.utcnow()

        try:
            result: T = self.execute()

            self.finished_at = datetime.utcnow()

            # Attach common metadata WITHOUT changing the object type
            result.agent_name = self.agent_name
            result.media_id = self.media_id
            result.success = True

            result.metadata = result.metadata or {}
            result.metadata.update(self._execution_metadata())

            return result

        except Exception as e:
            self.finished_at = datetime.utcnow()
            print(f"\n❌ AGENT FAILED: {self.agent_name}")
            print("AudioAgent failed with:", e)
            traceback.print_exc()
            if "rate limit" in str(e).lower():
                raise RuntimeError("LLM rate-limited, please retry after cooldown") from e
            return self._handle_failure(e)  # type: ignore

    # ------------------------------------------------------------------
    # Methods to be implemented by child agents
    # ------------------------------------------------------------------

    @abstractmethod
    def execute(self) -> BaseAgentOutput:
        """
        Core logic of the agent.

        Child classes MUST implement this method and
        return a subclass of BaseAgentOutput.
        """
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Failure handling
    # ------------------------------------------------------------------

    def _handle_failure(self, exception: Exception) -> BaseAgentOutput:
        """
        Handles failures in a controlled and observable way.
        """
        error_trace = traceback.format_exc()

        return BaseAgentOutput(
            agent_name=self.agent_name,
            media_id=self.media_id,
            success=False,
            error_message=str(exception),
            metadata={
                "run_id": self.run_id,
                "started_at": self.started_at.isoformat()
                if self.started_at
                else None,
                "finished_at": self.finished_at.isoformat()
                if self.finished_at
                else None,
                "traceback": error_trace,
            },
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _execution_metadata(self) -> Dict[str, Any]:
        """
        Standard execution metadata attached to every agent output.
        """
        duration_seconds = None
        if self.started_at and self.finished_at:
            duration_seconds = (
                self.finished_at - self.started_at
            ).total_seconds()

        return {
            "run_id": self.run_id,
            "started_at": self.started_at.isoformat()
            if self.started_at
            else None,
            "finished_at": self.finished_at.isoformat()
            if self.finished_at
            else None,
            "duration_seconds": duration_seconds,
            "timeout_seconds": AGENT_TIMEOUT_SECONDS,
        }
