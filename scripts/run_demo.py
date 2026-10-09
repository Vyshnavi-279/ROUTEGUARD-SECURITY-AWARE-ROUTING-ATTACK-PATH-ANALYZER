import sys
import os
import json

# Ensure parent directory is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from app.models.node import Node
from app.models.edge import Edge
from app.algorithms.dijkstra import dijkstra_shortest_path
from app.algorithms.attack_path import find_all_paths, calculate_attack_path_risk
from app.services.routing_service import RoutingService
from app.services.security_analyzer import SecurityAnalyzer
from app.services.attack_simulator import AttackSimulator

def main():
    print("================================================================")
    print("    ROUTEGUARD — SECURITY-AWARE ROUTING & ATTACK-PATH DEMO     ")
    print("================================================================\n")

    # Load dataset
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "sample_network.json")
    with open(data_path, "r") as f:
        data = json.load(f)

    nodes = {item["id"]: Node(**item) for item in data["nodes"]}
    edges = [Edge(**item) for item in data["edges"]]

    print("1. EVALUATING DIJKSTRA vs SECURITY-AWARE ROUTE (Internet -> DB)")
    routes = RoutingService.calculate_routes(nodes, edges, "internet", "db01")
    print(f"Normal Dijkstra Cost: {routes['normal_dijkstra']['route']['cost']} | Path: {' -> '.join(routes['normal_dijkstra']['route']['path'])}")
    print(f"Security-Aware Cost: {routes['security_aware_dijkstra']['route']['cost']} | Path: {' -> '.join(routes['security_aware_dijkstra']['route']['path'])}\n")

    print("2. ATTACK-PATH RISK ANALYSIS")
    paths = find_all_paths(nodes, edges, "internet", "db01")
    for idx, p in enumerate(paths, 1):
        risk = calculate_attack_path_risk(p, nodes, edges)
        print(f"Path #{idx}: {' -> '.join(p)} | Risk Score: {risk['risk_score']}/100 [{risk['severity']}]")
        for r in risk["reasons"]:
            print(f"  - {r}")

    print("\n3. DETECTING SECURITY MISCONFIGURATIONS & SPOFs")
    findings = SecurityAnalyzer.analyze_network_misconfigurations(nodes, edges)
    spofs = SecurityAnalyzer.detect_single_points_of_failure(nodes, edges)
    print(f"Total Security Misconfigurations: {len(findings)}")
    print(f"Single Points of Failure Detected: {len(spofs)} ({[s['node_id'] for s in spofs]})\n")

    print("4. SIMULATING COMPROMISE OF APPLICATION SERVER (app01)")
    sim = AttackSimulator.run_what_if_simulation(nodes, edges, "COMPROMISE_NODE", "app01")
    comp = sim["comparison"]
    print("BEFORE vs AFTER COMPARISON:")
    print(f"  - Risk Score: {comp['before']['max_risk_score']} -> {comp['after']['max_risk_score']}")
    print(f"  - Reachable Paths: {comp['before']['reachable_paths_count']} -> {comp['after']['reachable_paths_count']}")
    print(f"  - Security Findings: {comp['before']['findings_count']} -> {comp['after']['findings_count']}\n")

    print("================================================================")
    print("                      DEMO COMPLETE                             ")
    print("================================================================")

if __name__ == "__main__":
    main()