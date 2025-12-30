"""
RAGChatAgent
------------

Responsible for:
- Conversational Q&A over analyzed media
- Retrieval-augmented generation (RAG)
- Session-based memory handling

This is the primary user-facing agent.
"""

from typing import List

from openai import OpenAI

from src.agents.base_agent import BaseAgent
from src.schemas.agent_outputs import RAGChatOutput
from src.rag.prompt_templates import CHAT_SYSTEM_PROMPT
from src.rag.memory_manager import MemoryManager
from config.config import TEXT_MODEL


class RAGChatAgent(BaseAgent):
    """
    Agent that handles conversational interaction
    using retrieval-augmented generation.
    """

    def __init__(
        self,
        media_id: str,
        session_id: str,
        retrieved_context: List[str],
        user_question: str,
        config: dict | None = None,
    ):
        super().__init__(
            agent_name="RAGChatAgent",
            media_id=media_id,
            config=config,
        )

        if not user_question.strip():
            raise ValueError("User question is required for RAGChatAgent")

        self.session_id = session_id
        self.retrieved_context = retrieved_context
        self.user_question = user_question

        self.client = OpenAI()
        self.memory_manager = MemoryManager(session_id=session_id)

    # ------------------------------------------------------------------
    # Core execution
    # ------------------------------------------------------------------

    def execute(self) -> RAGChatOutput:
        messages = self._build_messages()

        response = self.client.chat.completions.create(
            model=TEXT_MODEL,
            messages=messages
        )

        answer = response.choices[0].message.content

        # Persist conversation memory
        self.memory_manager.add_interaction(
            user_message=self.user_question,
            assistant_message=answer,
        )

        return RAGChatOutput(
            agent_name=self.agent_name,
            media_id=self.media_id,
            success=True,
            answer=answer,
        )

    # ------------------------------------------------------------------
    # Prompt assembly
    # ------------------------------------------------------------------

    def _build_messages(self) -> List[dict]:
        context_block = "\n".join(self.retrieved_context)

        messages = [
            {
                "role": "system",
                "content": CHAT_SYSTEM_PROMPT,
            }
        ]

        # Inject memory
        messages.extend(self.memory_manager.get_conversation())

        # Inject retrieval context
        messages.append(
            {
                "role": "system",
                "content": f"Relevant context:\n{context_block}",
            }
        )

        # User query
        messages.append(
            {
                "role": "user",
                "content": self.user_question,
            }
        )

        return messages
