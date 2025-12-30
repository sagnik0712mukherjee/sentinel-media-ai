"""
Initialize Elasticsearch Indices
--------------------------------

Run this script once to create
required Elasticsearch indices.
"""

from config.config import (
    MEDIA_TRANSCRIPTS_INDEX,
)
from src.storage.elastic.index_manager import IndexManager
from src.storage.elastic.es_client import get_es_client


def main():
    es = get_es_client()
    index_manager = IndexManager(es)

    # -------------------------------------------------
    # Media metadata index (if you already use this)
    # -------------------------------------------------
    print("Creating media index...")
    index_manager.create_media_index(index_name="media-index")

    # -------------------------------------------------
    # Vector index (for future embeddings / search)
    # -------------------------------------------------
    print("Creating vector index...")
    index_manager.create_vector_index(
        index_name="media-vectors",
        dims=384,  # match your embedding model
    )

    # -------------------------------------------------
    # Transcript chunks index (CRITICAL for RAG)
    # -------------------------------------------------
    print("Creating transcript index...")
    if not es.indices.exists(index=MEDIA_TRANSCRIPTS_INDEX):
        es.indices.create(
            index=MEDIA_TRANSCRIPTS_INDEX,
            body={
                "mappings": {
                    "properties": {
                        "media_id": {"type": "keyword"},
                        "text": {"type": "text"},
                        "start_time": {"type": "float"},
                        "end_time": {"type": "float"},
                    }
                }
            },
        )
    else:
        print(f"Index {MEDIA_TRANSCRIPTS_INDEX} already exists.")

    print("✅ Elasticsearch indices initialized successfully.")


if __name__ == "__main__":
    main()
