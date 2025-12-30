"""
Session Store
-------------

Handles persistence of chat sessions.
"""

from typing import Dict, List


class SessionStore:
    """
    Simple in-memory session store.
    Replace with DB/Redis later.
    """

    def __init__(self):
        self.sessions: Dict[str, List[dict]] = {}

    # --------------------------------------------------

    def get(self, session_id: str) -> List[dict]:
        return self.sessions.get(session_id, [])

    # --------------------------------------------------

    def save(self, session_id: str, messages: List[dict]):
        self.sessions[session_id] = messages

    # --------------------------------------------------

    def clear(self, session_id: str):
        if session_id in self.sessions:
            del self.sessions[session_id]

