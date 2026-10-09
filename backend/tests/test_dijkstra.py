import pytest
from app.algorithms.dijkstra import dijkstra_shortest_path
from app.models.node import Node
from app.models.edge import Edge

def test_dijkstra_normal_path():
    nodes = {
        "A": Node(id="A", name="Node A", type="ROUTER", zone="DMZ"),
        "B": Node(id="B", name="Node B", type="ROUTER", zone="DMZ"),
        "C": Node(id="C", name="Node C", type="DATABASE", zone="DATABASE")
    }
    edges = [
        Edge(source="A", destination="B", cost=2.0),
        Edge(source="B", destination="C", cost=3.0)
    ]
    res = dijkstra_shortest_path(nodes, edges, "A", "C")
    assert res["status"] == "REACHABLE"
    assert res["cost"] == 5.0
    assert res["path"] == ["A", "B", "C"]

def test_dijkstra_unreachable_path():
    nodes = {
        "A": Node(id="A", name="Node A", type="ROUTER", zone="DMZ"),
        "B": Node(id="B", name="Node B", type="DATABASE", zone="DATABASE")
    }
    edges = []
    res = dijkstra_shortest_path(nodes, edges, "A", "B")
    assert res["status"] == "UNREACHABLE"