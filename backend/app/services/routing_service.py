from typing import Dict, Any, List
from app.algorithms.dijkstra import dijkstra_shortest_path
from app.algorithms.attack_path import calculate_attack_path_risk

class RoutingService:

    @staticmethod
    def calculate_routes(
        nodes: Dict[str, Any],
        edges: List[Any],
        source: str,
        destination: str
    ) -> Dict[str, Any]:
        """Calculates normal Dijkstra path vs Security-Aware Path and provides security context."""
        normal_path = dijkstra_shortest_path(nodes, edges, source, destination, ignore_compromised=False)
        secure_path = dijkstra_shortest_path(nodes, edges, source, destination, ignore_compromised=True)

        normal_risk = None
        if normal_path["status"] == "REACHABLE":
            normal_risk = calculate_attack_path_risk(normal_path["path"], nodes, edges)

        secure_risk = None
        if secure_path["status"] == "REACHABLE":
            secure_risk = calculate_attack_path_risk(secure_path["path"], nodes, edges)

        return {
            "source": source,
            "destination": destination,
            "normal_dijkstra": {
                "route": normal_path,
                "risk_analysis": normal_risk
            },
            "security_aware_dijkstra": {
                "route": secure_path,
                "risk_analysis": secure_risk
            },
            "recommendation": (
                "Use Security-Aware path to bypass compromised or policy-violating nodes."
                if normal_path.get("path") != secure_path.get("path")
                else "Standard shortest path aligns with security requirements."
            )
        }