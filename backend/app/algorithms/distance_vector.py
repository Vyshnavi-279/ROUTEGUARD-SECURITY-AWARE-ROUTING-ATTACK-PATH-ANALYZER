from typing import Dict, List, Any

def run_distance_vector(nodes: Dict[str, Any], edges: List[Any], max_iterations: int = 15) -> Dict[str, Any]:
    """
    Simplified Distance-Vector routing algorithm (Bellman-Ford distributed simulation).
    Demonstrates hop-by-hop distance vector computation and routing table convergence.
    """
    node_ids = list(nodes.keys())
    # Routing table structure: table[router][destination] = {"cost": float, "next_hop": str}
    tables: Dict[str, Dict[str, Dict[str, Any]]] = {}

    for u in node_ids:
        tables[u] = {}
        for v in node_ids:
            if u == v:
                tables[u][v] = {"cost": 0.0, "next_hop": u}
            else:
                tables[u][v] = {"cost": float("inf"), "next_hop": None}

    # Initialize direct link costs
    for edge in edges:
        e_src = edge.source if hasattr(edge, 'source') else edge['source']
        e_dst = edge.destination if hasattr(edge, 'destination') else edge['destination']
        e_cost = edge.cost if hasattr(edge, 'cost') else edge.get('cost', 1.0)
        e_active = edge.active if hasattr(edge, 'active') else edge.get('active', True)
        e_bidir = edge.bidirectional if hasattr(edge, 'bidirectional') else edge.get('bidirectional', True)

        if not e_active:
            continue

        if e_src in tables and e_dst in tables:
            tables[e_src][e_dst] = {"cost": float(e_cost), "next_hop": e_dst}
            if e_bidir:
                tables[e_dst][e_src] = {"cost": float(e_cost), "next_hop": e_src}

    iterations = 0
    converged = False

    while iterations < max_iterations and not converged:
        converged = True
        iterations += 1
        new_tables = {u: {v: dict(tables[u][v]) for v in node_ids} for u in node_ids}

        for u in node_ids:
            for v in node_ids:
                # Share routing info with neighbors
                for neighbor in node_ids:
                    direct_cost = tables[u][neighbor]["cost"]
                    if direct_cost < float("inf") and neighbor != u:
                        cost_via_neighbor = direct_cost + tables[neighbor][v]["cost"]
                        if cost_via_neighbor < new_tables[u][v]["cost"]:
                            new_tables[u][v] = {"cost": cost_via_neighbor, "next_hop": neighbor}
                            converged = False

        tables = new_tables

    return {
        "iterations_to_converge": iterations,
        "converged": converged,
        "routing_tables": tables
    }