"""
Elasticsearch Index Manager
---------------------------

Creates and manages indices for media,
transcripts, and embeddings.
"""

from elasticsearch import Elasticsearch


class IndexManager:
    """
    Manages Elasticsearch indices.
    """

    def __init__(self, es_client: Elasticsearch):
        self.es = es_client

    # --------------------------------------------------

    def create_media_index(self, index_name: str):
        mapping = {
            "mappings": {
                "properties": {
                    "media_id": {"type": "keyword"},
                    "content": {"type": "text"},
                    "tags": {"type": "keyword"},
                    "entities": {"type": "keyword"},
                    "timestamp": {"type": "date"},
                }
            }
        }

        if not self.es.indices.exists(index=index_name):
            self.es.indices.create(index=index_name, body=mapping)

    # --------------------------------------------------

    def create_vector_index(self, index_name: str, dims: int):
        mapping = {
            "mappings": {
                "properties": {
                    "media_id": {"type": "keyword"},
                    "text": {"type": "text"},
                    "embedding": {
                        "type": "dense_vector",
                        "dims": dims,
                        "index": True,
                        "similarity": "cosine",
                    },
                }
            }
        }

        if not self.es.indices.exists(index=index_name):
            self.es.indices.create(index=index_name, body=mapping)
