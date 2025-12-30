from elasticsearch import Elasticsearch
from config.config import (
    ELASTICSEARCH_URL,
    ELASTICSEARCH_USER,
    ELASTICSEARCH_PASSWORD,
)


def get_es_client() -> Elasticsearch:
    if not ELASTICSEARCH_URL:
        raise ValueError("ELASTICSEARCH_URL not set")

    return Elasticsearch(
        ELASTICSEARCH_URL,
        basic_auth=(ELASTICSEARCH_USER, ELASTICSEARCH_PASSWORD),
        verify_certs=False,  # local docker https
    )
