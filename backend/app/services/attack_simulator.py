import copy
from typing import Dict, List, Any
from app.algorithms.dijkstra import dijkstra_shortest_path
from app.algorithms.attack_path import find_all_paths, calculate_attack_path_risk
from app.services.security_analyzer import SecurityAnalyzer

class AttackSimulator:

    @staticmethod
    def run_what_if_simulation(
        nodes: Dict[str, Any],
        edges: List[Any],
        action: str,
        target_id: str,
        source_id: str = "internet",
        dest_id: str = "db01"
    ) -> Dict[str, Any]:
        """
        Executes a What-If failure or attack simulation (node compromise, node failure, link disable)
        and provides a side-by-side BEFORE vs AFTER security impact comparison.
        """
        # BEFORE state evaluation
        before_paths = find_all_paths(nodes, edges, source_id, dest_id)
        before_risks = [calculate_attack_path_risk(p, nodes, edges) for p in before_paths]
        before_findings = SecurityAnalyzer.analyze_network_misconfigurations(nodes, edges)

        mod_nodes = copy.deepcopy(nodes)
        mod_edges = copy.deepcopy(edges)

        # Apply simulation mutation
        if action == "COMPROMISE_NODE":
            if target_id in mod_nodes:
                if hasattr(mod_nodes[target_id], 'compromised'):
                    mod_nodes[target_id].compromised = True
                else:
                    mod_nodes[target_id]['compromised'] = True

        elif action == "DISABLE_NODE":
            mod_nodes = {k: v for k, v in mod_nodes.items() if k != target_id}
            mod_edges = [
                e for e in mod_edges
                if ((e.source if hasattr(e, 'source') else e['source']) != target_id)
                and ((e.destination if hasattr(e, 'destination') else e['destination']) != target_id)
            ]

        elif action == "DISABLE_LINK":
            mod_edges = [
                e for e in mod_edges
                if not (
                    ((e.source if hasattr(e, 'source') else e['source']) == target_id) or
                    ((e.destination if hasattr(e, 'destination') else e['destination']) == target_id)
                )
            ]

        # AFTER state evaluation
        after_paths = find_all_paths(mod_nodes, mod_edges, source_id, dest_id)
        after_risks = [calculate_attack_path_risk(p, mod_nodes, mod_edges) for p in after_paths]
        after_findings = SecurityAnalyzer.analyze_network_misconfigurations(mod_nodes, mod_edges)

        before_max_risk = max([r["risk_score"] for r in before_risks], default=0)
        after_max_risk = max([r["risk_score"] for r in after_risks], default=0)

        return {
            "simulation_action": action,
            "target_id": target_id,
            "comparison": {
                "before": {
                    "reachable_paths_count": len(before_paths),
                    "max_risk_score": before_max_risk,
                    "findings_count": len(before_findings),
                    "paths": before_paths
                },
                "after": {
                    "reachable_paths_count": len(after_paths),
                    "max_risk_score": after_max_risk,
                    "findings_count": len(after_findings),
                    "paths": after_paths
                },
                "delta": {
                    "risk_change": after_max_risk - before_max_risk,
                    "paths_change": len(after_paths) - len(before_paths),
                    "new_findings": len(after_findings) - len(before_findings)
                }
            },
            "findings_after": after_findings
        }