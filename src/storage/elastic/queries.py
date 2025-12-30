"""
Elasticsearch Queries
---------------------

Reusable queries for search and retrieval.
"""

from typing import List

from elasticsearch import Elasticsearch


class ElasticQueries:
    """
    Query helper for Elasticsearch.
    """

    def __init__(self, es_client: Elasticsearch, index_name: str):
        self.es = es_client
        self.index_name = index_name

    # --------------------------------------------------

    def keyword_search(self, query: str, top_k: int = 5) -> List[str]:
        body = {
            "size": top_k,
            "query": {
                "match": {
                    "content": query
                }
            }
        }

        response = self.es.search(index=self.index_name, body=body)
        return [hit["_source"]["content"] for hit in response["hits"]["hits"]]

    # --------------------------------------------------

    def vector_search(self, embedding: List[float], top_k: int = 5) -> List[str]:
        body = {
            "size": top_k,
            "query": {
                "script_score": {
                    "query": {"match_all": {}},
                    "script": {
                        "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                        "params": {"query_vector": embedding},
                    },
                }
            },
        }

        response = self.es.search(index=self.index_name, body=body)
        return [hit["_source"]["text"] for hit in response["hits"]["hits"]]
