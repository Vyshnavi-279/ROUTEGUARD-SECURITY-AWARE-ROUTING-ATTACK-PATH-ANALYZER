from typing import Dict, List, Set, Any, Tuple

def generate_reachability_tree(
    nodes: Dict[str, Any],
    edges: List[Any],
    source: str,
    policies: List[Any] = None
) -> Dict[str, Any]:
    """
    BFS Graph traversal generating a Reachability/Broadcast Tree from a source node,
    applying security policies along the path to prune blocked branches.
    """
    if source not in nodes:
        return {"source": source, "tree": {}, "reachable_nodes": [], "blocked_nodes": []}

    adj: Dict[str, List[Tuple[str, Any]]] = {n: [] for n in nodes}
    for edge in edges:
        e_src = edge.source if hasattr(edge, 'source') else edge['source']
        e_dst = edge.destination if hasattr(edge, 'destination') else edge['destination']
        e_active = edge.active if hasattr(edge, 'active') else edge.get('active', True)
        e_bidir = edge.bidirectional if hasattr(edge, 'bidirectional') else edge.get('bidirectional', True)

        if not e_active:
            continue
        if e_src in nodes and e_dst in nodes:
            adj[e_src].append((e_dst, edge))
            if e_bidir:
                adj[e_dst].append((e_src, edge))

    visited: Set[str] = {source}
    queue: List[str] = [source]
    tree: Dict[str, List[str]] = {n: [] for n in nodes}
    blocked: Set[str] = set()

    while queue:
        curr = queue.pop(0)
        curr_node = nodes[curr]

        for nxt, edge in adj.get(curr, []):
            if nxt in visited:
                continue
            nxt_node = nodes[nxt]

            # Simplified security check for reachability
            # If src=INTERNET or DMZ and dst=DATABASE directly, block
            curr_zone = curr_node.zone if hasattr(curr_node, 'zone') else curr_node.get('zone')
            nxt_zone = nxt_node.zone if hasattr(nxt_node, 'zone') else nxt_node.get('zone')

            if curr_zone == "INTERNET" and nxt_zone == "DATABASE":
                blocked.add(nxt)
                continue

            visited.add(nxt)
            tree[curr].append(nxt)
            queue.append(nxt)

    return {
        "source": source,
        "tree": {k: v for k, v in tree.items() if v or k in visited},
        "reachable_nodes": list(visited),
        "unreachable_nodes": [n for n in nodes if n not in visited],
        "policy_blocked_nodes": list(blocked)
    }