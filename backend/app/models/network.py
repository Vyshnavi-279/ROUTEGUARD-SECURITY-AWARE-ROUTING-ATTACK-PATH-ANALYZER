from typing import Dict, List, Optional
from app.models.node import Node
from app.models.edge import Edge
from app.models.policy import Policy

class NetworkState(BaseModel):
    nodes: Dict[str, Node] = {}
    edges: List[Edge] = []
    policies: List[Policy] = []

    def get_node(self, node_id: str) -> Optional[Node]:
        return self.nodes.get(node_id)

    def add_node(self, node: Node) -> None:
        self.nodes[node.id] = node

    def add_edge(self, edge: Edge) -> None:
        self.edges.append(edge)