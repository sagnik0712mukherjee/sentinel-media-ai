"""
Retriever
---------

Hybrid retriever:
- Elasticsearch (primary)
- Local keyword fallback
"""

from typing import List

from config.config import (
    ELASTICSEARCH_URL,
    MEDIA_TRANSCRIPTS_INDEX,
    RAG_TOP_K,
)
from src.processing.chunker import TextChunker
from src.storage.elastic.es_client import get_es_client


class Retriever:
    def __init__(self):
        self.chunker = TextChunker()
        self.use_es = ELASTICSEARCH_URL is not None

        if self.use_es:
            self.es = get_es_client()

    # --------------------------------------------------
    # Public API
    # --------------------------------------------------

    def retrieve(
        self,
        media_id: str,
        transcript_text: str,
        query: str,
        top_k: int = RAG_TOP_K,
    ) -> List[str]:
        """
        Retrieve relevant context for a query.
        """
        if self.use_es:
            results = self._es_retrieve(media_id, query, top_k)
            if results:
                return results

        # Fallback: local keyword matching
        return self._local_retrieve(transcript_text, query, top_k)

    # --------------------------------------------------
    # Elasticsearch retrieval
    # --------------------------------------------------

    def _es_retrieve(
        self,
        media_id: str,
        query: str,
        top_k: int,
    ) -> List[str]:
        body = {
            "size": top_k,
            "query": {
                "bool": {
                    "must": [
                        {"term": {"media_id": media_id}}
                    ],
                    "should": [
                        {"match": {"text": query}}
                    ],
                    "minimum_should_match": 1,
                }
            },
        }

        response = self.es.search(
            index=MEDIA_TRANSCRIPTS_INDEX,
            body=body,
        )

        hits = response.get("hits", {}).get("hits", [])
        return [hit["_source"]["text"] for hit in hits]

    # --------------------------------------------------
    # Local fallback
    # --------------------------------------------------

    def _local_retrieve(
        self,
        transcript_text: str,
        query: str,
        top_k: int,
    ) -> List[str]:
        chunks = self.chunker.chunk(transcript_text)
        scored = []

        query_lower = query.lower()
        for chunk in chunks:
            score = sum(
                1 for word in query_lower.split()
                if word in chunk.lower()
            )
            if score > 0:
                scored.append((score, chunk))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [chunk for score, chunk in scored[:top_k]]
