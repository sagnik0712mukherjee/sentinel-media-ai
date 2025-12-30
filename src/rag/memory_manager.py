"""
Memory Manager
--------------

Handles session-based conversation memory
for RAG chat.
"""

from typing import List, Dict


class MemoryManager:
    """
    Simple in-memory conversation store.
    Can be swapped with DB/Redis later.
    """

    def __init__(self, session_id: str, max_turns: int = 6):
        self.session_id = session_id
        self.max_turns = max_turns
        self._memory: List[Dict[str, str]] = []

    # --------------------------------------------------

    def add_interaction(self, user_message: str, assistant_message: str):
        self._memory.append({"role": "user", "content": user_message})
        self._memory.append({"role": "assistant", "content": assistant_message})

        # Trim memory
        if len(self._memory) > self.max_turns * 2:
            self._memory = self._memory[-self.max_turns * 2 :]

    # --------------------------------------------------

    def get_conversation(self) -> List[Dict[str, str]]:
        return list(self._memory)
