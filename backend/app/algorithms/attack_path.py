from typing import Dict, List, Set, Any
from app.models.node import ZoneType, TrustLevel, Criticality

def find_all_paths(
    nodes: Dict[str, Any],
    edges: List[Any],
    source: str,
    target: str,
    max_depth: int = 8
) -> List[List[str]]:
    """Finds all simple paths between source and target up to a maximum depth using DFS."""
    adj: Dict[str, List[str]] = {n: [] for n in nodes}
    for edge in edges:
        e_src = edge.source if hasattr(edge, 'source') else edge['source']
        e_dst = edge.destination if hasattr(edge, 'destination') else edge['destination']
        e_active = edge.active if hasattr(edge, 'active') else edge.get('active', True)
        e_bidir = edge.bidirectional if hasattr(edge, 'bidirectional') else edge.get('bidirectional', True)

        if not e_active:
            continue
        if e_src in nodes and e_dst in nodes:
            adj[e_src].append(e_dst)
            if e_bidir:
                adj[e_dst].append(e_src)

    all_paths: List[List[str]] = []

    def dfs(current: str, path: List[str], visited: Set[str]):
        if len(path) > max_depth:
            return
        if current == target:
            all_paths.append(list(path))
            return

        for neighbor in adj.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                path.append(neighbor)
                dfs(neighbor, path, visited)
                path.pop()
                visited.remove(neighbor)

    if source in nodes and target in nodes:
        dfs(source, [source], {source})

    return all_paths


def calculate_attack_path_risk(
    path: List[str],
    nodes: Dict[str, Any],
    edges: List[Any],
    policies: List[Any] = None
) -> Dict[str, Any]:
    """
    Evaluates an attack path and computes a transparent risk score (0-100).
    Explanations are provided for all added penalty points.
    """
    score = 0.0
    reasons: List[str] = []
    policy_violations: List[str] = []
    untrusted_count = 0
    zone_transitions = 0
    unencrypted_count = 0
    has_compromised = False

    # Edge lookup helper
    edge_map = {}
    for edge in edges:
        e_src = edge.source if hasattr(edge, 'source') else edge['source']
        e_dst = edge.destination if hasattr(edge, 'destination') else edge['destination']
        edge_map[(e_src, e_dst)] = edge
        edge_map[(e_dst, e_src)] = edge

    path_nodes = [nodes[n_id] for n_id in path if n_id in nodes]

    # Rule 1: Critical Resource Exposed (+30)
    target_node = path_nodes[-1]
    target_crit = target_node.criticality if hasattr(target_node, 'criticality') else target_node.get('criticality')
    if target_crit in ["CRITICAL", Criticality.CRITICAL]:
        score += 30
        reasons.append("Path reaches critical target asset")

    # Rule 2: Compromised Node in Path (+25)
    for n in path_nodes:
        is_comp = n.compromised if hasattr(n, 'compromised') else n.get('compromised', False)
        if is_comp:
            has_compromised = True
            score += 25
            n_id = n.id if hasattr(n, 'id') else n.get('id')
            reasons.append(f"Compromised node '{n_id}' present in route")
            break

    # Rule 3: Untrusted / Low-Trust Node (+20)
    for n in path_nodes:
        trust = n.trust_level if hasattr(n, 'trust_level') else n.get('trust_level')
        if trust in ["UNTRUSTED", TrustLevel.UNTRUSTED]:
            untrusted_count += 1
            score += 20
            n_id = n.id if hasattr(n, 'id') else n.get('id')
            reasons.append(f"Traverses untrusted node '{n_id}'")

    # Rule 4: Zone Transitions / Missing Segmentation (+15)
    prev_zone = None
    for n in path_nodes:
        curr_zone = n.zone if hasattr(n, 'zone') else n.get('zone')
        if prev_zone and curr_zone != prev_zone:
            zone_transitions += 1
            # Bypassing DMZ directly from INTERNET to APPLICATION/DATABASE
            if prev_zone in ["INTERNET", ZoneType.INTERNET] and curr_zone in ["DATABASE", ZoneType.DATABASE, "APPLICATION", ZoneType.APPLICATION]:
                score += 15
                reasons.append(f"Direct bypass from {prev_zone} to inner zone {curr_zone}")
        prev_zone = curr_zone

    # Rule 5: Unencrypted Links (+10)
    for i in range(len(path) - 1):
        u, v = path[i], path[i+1]
        edge = edge_map.get((u, v))
        if edge:
            is_enc = edge.encrypted if hasattr(edge, 'encrypted') else edge.get('encrypted', True)
            if not is_enc:
                unencrypted_count += 1
                score += 10
                reasons.append(f"Unencrypted link between {u} and {v}")

    # Cap score at 100
    risk_score = min(100.0, score)

    # Determine Severity
    if risk_score >= 70:
        severity = "CRITICAL"
    elif risk_score >= 40:
        severity = "HIGH"
    elif risk_score >= 20:
        severity = "MEDIUM"
    else:
        severity = "LOW"

    return {
        "path": path,
        "length": len(path),
        "risk_score": risk_score,
        "severity": severity,
        "reasons": reasons,
        "trust_zone_transitions": zone_transitions,
        "untrusted_nodes_count": untrusted_count,
        "unencrypted_links_count": unencrypted_count,
        "has_compromised_nodes": has_compromised,
        "policy_violations": policy_violations
    }