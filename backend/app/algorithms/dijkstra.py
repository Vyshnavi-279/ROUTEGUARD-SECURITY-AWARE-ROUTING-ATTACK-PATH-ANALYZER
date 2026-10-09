import heapq
from typing import Dict, List, Tuple, Set, Optional, Any

def dijkstra_shortest_path(
    nodes: Dict[str, Any],
    edges: List[Any],
    source: str,
    destination: str,
    ignore_disabled: bool = True,
    ignore_compromised: bool = False
) -> Dict[str, Any]:
    """
    Dijkstra's Algorithm implemented from scratch using a Min-Heap.
    Returns the shortest path, total cost, path sequence, and reachability status.
    """
    if source not in nodes:
        return {"status": "UNREACHABLE", "reason": f"Source node '{source}' not found", "cost": float("inf"), "path": []}
    if destination not in nodes:
        return {"status": "UNREACHABLE", "reason": f"Destination node '{destination}' not found", "cost": float("inf"), "path": []}

    # Build adjacency list
    adj: Dict[str, List[Tuple[str, float, str]]] = {node_id: [] for node_id in nodes}
    for edge in edges:
        # Access edge attributes (dict or pydantic model)
        e_src = edge.source if hasattr(edge, 'source') else edge['source']
        e_dst = edge.destination if hasattr(edge, 'destination') else edge['destination']
        e_cost = edge.cost if hasattr(edge, 'cost') else edge.get('cost', 1.0)
        e_active = edge.active if hasattr(edge, 'active') else edge.get('active', True)
        e_bidir = edge.bidirectional if hasattr(edge, 'bidirectional') else edge.get('bidirectional', True)

        if ignore_disabled and not e_active:
            continue

        if e_src in nodes and e_dst in nodes:
            # Check compromised nodes filter if required
            src_node = nodes[e_src]
            dst_node = nodes[e_dst]
            src_comp = src_node.compromised if hasattr(src_node, 'compromised') else src_node.get('compromised', False)
            dst_comp = dst_node.compromised if hasattr(dst_node, 'compromised') else dst_node.get('compromised', False)

            if ignore_compromised and (src_comp or dst_comp):
                continue

            adj[e_src].append((e_dst, float(e_cost), e_src))
            if e_bidir:
                adj[e_dst].append((e_src, float(e_cost), e_dst))

    # Priority queue storing tuples of (accumulated_cost, current_node)
    pq: List[Tuple[float, str]] = [(0.0, source)]
    distances: Dict[str, float] = {node_id: float("inf") for node_id in nodes}
    distances[source] = 0.0
    predecessors: Dict[str, Optional[str]] = {node_id: None for node_id in nodes}
    visited: Set[str] = set()

    while pq:
        current_dist, u = heapq.heappop(pq)

        if u in visited:
            continue
        visited.add(u)

        if u == destination:
            break

        for v, weight, _ in adj.get(u, []):
            if v in visited:
                continue
            new_dist = current_dist + weight
            if new_dist < distances[v]:
                distances[v] = new_dist
                predecessors[v] = u
                heapq.heappush(pq, (new_dist, v))

    if distances[destination] == float("inf"):
        return {
            "status": "UNREACHABLE",
            "reason": f"No valid physical or active path from {source} to {destination}",
            "cost": float("inf"),
            "path": []
        }

    # Reconstruct path
    path = []
    curr: Optional[str] = destination
    while curr is not None:
        path.append(curr)
        curr = predecessors[curr]
    path.reverse()

    return {
        "status": "REACHABLE",
        "source": source,
        "destination": destination,
        "cost": distances[destination],
        "path": path,
        "nodes_visited_count": len(visited)
    }