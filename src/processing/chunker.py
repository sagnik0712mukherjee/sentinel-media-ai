"""
Chunker
-------

Splits long text into semantically manageable chunks
for embeddings, storage, and retrieval.
"""

from typing import List


class TextChunker:
    """
    Simple text chunker with overlap support.
    """

    def __init__(
        self,
        chunk_size: int = 500,
        overlap: int = 50,
    ):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, text: str) -> List[str]:
        if not text.strip():
            return []

        words = text.split()
        chunks = []

        start = 0
        while start < len(words):
            end = start + self.chunk_size
            chunk_words = words[start:end]
            chunks.append(" ".join(chunk_words))
            start = end - self.overlap

            if start < 0:
                start = 0

        return chunks
