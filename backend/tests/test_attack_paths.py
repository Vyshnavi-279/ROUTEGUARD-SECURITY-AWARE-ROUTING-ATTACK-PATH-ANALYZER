import pytest
from app.algorithms.attack_path import find_all_paths, calculate_attack_path_risk
from app.models.node import Node
from app.models.edge import Edge

def test_attack_path_risk_calculation():
    nodes = {
        "internet": Node(id="internet", name="Internet", type="INTERNET", zone="INTERNET"),
        "app": Node(id="app", name="App", type="APP_SERVER", zone="APPLICATION", compromised=True),
        "db": Node(id="db", name="DB", type="DATABASE", zone="DATABASE", criticality="CRITICAL")
    }
    edges = [
        Edge(source="internet", destination="app", cost=1.0),
        Edge(source="app", destination="db", cost=1.0)
    ]
    paths = find_all_paths(nodes, edges, "internet", "db")
    assert len(paths) == 1
    eval_res = calculate_attack_path_risk(paths[0], nodes, edges)
    assert eval_res["risk_score"] >= 50
    assert eval_res["has_compromised_nodes"] is True