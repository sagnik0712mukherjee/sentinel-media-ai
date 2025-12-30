"""
Agent Graph
-----------

Defines the logical execution order and dependencies
between agents in the system.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class AgentNode:
    name: str
    depends_on: List[str]


class AgentGraph:
    """
    Represents a directed acyclic graph (DAG)
    of agents and their dependencies.
    """

    def __init__(self):
        self.nodes = self._build_graph()

    def _build_graph(self) -> dict[str, AgentNode]:
        """
        Defines the agent dependency graph.
        """

        return {
            "AudioAgent": AgentNode(
                name="AudioAgent",
                depends_on=[],
            ),
            "EmotionAgent": AgentNode(
                name="EmotionAgent",
                depends_on=["AudioAgent"],
            ),
            "TaggingAgent": AgentNode(
                name="TaggingAgent",
                depends_on=["AudioAgent"],
            ),
            "VideoAgent": AgentNode(
                name="VideoAgent",
                depends_on=[],
            ),
            "ReasoningAgent": AgentNode(
                name="ReasoningAgent",
                depends_on=[
                    "EmotionAgent",
                    "TaggingAgent",
                    "VideoAgent",
                ],
            ),
            "RiskAgent": AgentNode(
                name="RiskAgent",
                depends_on=["ReasoningAgent"],
            ),
        }

    def execution_order(self) -> List[str]:
        """
        Returns a valid execution order
        respecting dependencies.
        """
        visited = set()
        order = []

        def visit(node_name: str):
            if node_name in visited:
                return
            visited.add(node_name)

            for dep in self.nodes[node_name].depends_on:
                visit(dep)

            order.append(node_name)

        for node in self.nodes:
            visit(node)

        return order

