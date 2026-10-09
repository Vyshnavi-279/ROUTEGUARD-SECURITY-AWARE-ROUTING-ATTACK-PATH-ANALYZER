from typing import Dict, List, Any
from app.models.security import SecurityFinding, Severity
from app.algorithms.attack_path import find_all_paths, calculate_attack_path_risk

class SecurityAnalyzer:

    @staticmethod
    def analyze_network_misconfigurations(nodes: Dict[str, Any], edges: List[Any]) -> List[Dict[str, Any]]:
        """Detects security findings such as direct internet exposure, SPOFs, unencrypted links, and compromised nodes."""
        findings: List[Dict[str, Any]] = []

        # Map edges
        edge_map = {}
        for edge in edges:
            e_src = edge.source if hasattr(edge, 'source') else edge['source']
            e_dst = edge.destination if hasattr(edge, 'destination') else edge['destination']
            edge_map[(e_src, e_dst)] = edge
            edge_map[(e_dst, e_src)] = edge

        # 1. Direct Internet to Database connection
        internet_nodes = [n_id for n_id, n in nodes.items() if (n.zone if hasattr(n, 'zone') else n.get('zone')) in ["INTERNET"]]
        db_nodes = [n_id for n_id, n in nodes.items() if (n.zone if hasattr(n, 'zone') else n.get('zone')) in ["DATABASE"]]

        for i_id in internet_nodes:
            for d_id in db_nodes:
                if (i_id, d_id) in edge_map:
                    findings.append({
                        "id": "SEC-FIND-001",
                        "title": "Database Directly Exposed to Internet",
                        "severity": "HIGH",
                        "description": f"Critical Database node '{d_id}' has a direct routing link to Internet node '{i_id}'.",
                        "affected_nodes": [i_id, d_id],
                        "why_it_matters": "Direct internet exposure exposes critical databases to unauthenticated network traffic and remote attacks.",
                        "recommendation": "Remove direct link between Internet and Database. Enforce routing through DMZ and Application tiers."
                    })

        # 2. Compromised Node access to Critical Resources
        compromised_nodes = [n_id for n_id, n in nodes.items() if (n.compromised if hasattr(n, 'compromised') else n.get('compromised', False))]
        for comp_id in compromised_nodes:
            for d_id in db_nodes:
                paths = find_all_paths(nodes, edges, comp_id, d_id, max_depth=3)
                if paths:
                    findings.append({
                        "id": f"SEC-FIND-COMP-{comp_id}",
                        "title": "Critical Resource Reachable from Compromised Node",
                        "severity": "CRITICAL",
                        "description": f"Compromised node '{comp_id}' can reach Database '{d_id}' in {len(paths[0])-1} hops.",
                        "affected_nodes": [comp_id, d_id],
                        "why_it_matters": "Attackers controlling the compromised node can pivot directly to critical database infrastructure.",
                        "recommendation": "Isolate compromised node immediately and re-route traffic via security controls."
                    })

        # 3. Unencrypted Sensitive Connections
        for edge in edges:
            e_src = edge.source if hasattr(edge, 'source') else edge['source']
            e_dst = edge.destination if hasattr(edge, 'destination') else edge['destination']
            e_enc = edge.encrypted if hasattr(edge, 'encrypted') else edge.get('encrypted', True)

            src_zone = nodes[e_src].zone if hasattr(nodes[e_src], 'zone') else nodes[e_src].get('zone')
            dst_zone = nodes[e_dst].zone if hasattr(nodes[e_dst], 'zone') else nodes[e_dst].get('zone')

            if not e_enc and (src_zone in ["DATABASE", "APPLICATION"] or dst_zone in ["DATABASE", "APPLICATION"]):
                findings.append({
                    "id": f"SEC-FIND-ENC-{e_src}-{e_dst}",
                    "title": "Unencrypted Sensitive Communication Link",
                    "severity": "MEDIUM",
                    "description": f"Link between '{e_src}' and '{e_dst}' handling sensitive traffic is unencrypted.",
                    "affected_nodes": [e_src, e_dst],
                    "why_it_matters": "Cleartext traffic allows man-in-the-middle sniffing and data tampering across network zones.",
                    "recommendation": "Enable TLS/IPsec encryption on link."
                })

        return findings


    @staticmethod
    def detect_single_points_of_failure(nodes: Dict[str, Any], edges: List[Any], key_target: str = "db01") -> List[Dict[str, Any]]:
        """Identifies routers/firewalls whose failure completely disconnects critical target resources."""
        from app.algorithms.dijkstra import dijkstra_shortest_path
        spofs = []

        if key_target not in nodes:
            return spofs

        # Test reachability from Internet nodes
        internet_nodes = [n_id for n_id, n in nodes.items() if (n.zone if hasattr(n, 'zone') else n.get('zone')) in ["INTERNET"]]
        if not internet_nodes:
            return spofs

        source = internet_nodes[0]
        baseline = dijkstra_shortest_path(nodes, edges, source, key_target)
        if baseline["status"] != "REACHABLE":
            return spofs

        # Test disabling each non-source, non-target node
        for node_id in nodes:
            if node_id in [source, key_target]:
                continue

            # Simulate disabling node
            temp_nodes = {k: v for k, v in nodes.items() if k != node_id}
            temp_edges = [
                e for e in edges
                if ((e.source if hasattr(e, 'source') else e['source']) != node_id)
                and ((e.destination if hasattr(e, 'destination') else e['destination']) != node_id)
            ]

            result = dijkstra_shortest_path(temp_nodes, temp_edges, source, key_target)
            if result["status"] == "UNREACHABLE":
                spofs.append({"spof_node": node_id, "impacted_target": key_target})

        findings = []
        for item in spofs:
            node_id = item["spof_node"]
            findings.append({"node_id": node_id, "title": f"Single Point of Failure: {node_id}", "impact": f"Failure of '{node_id}' completely isolates '{key_target}' from the Internet.", "affected_services": [key_target], "recommendation": f"Deploy redundant security gateway or routing path alongside '{node_id}'."})

        return findings