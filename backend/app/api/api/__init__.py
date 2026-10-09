import json
import os
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from pydantic import BaseModel

from app.models.node import Node
from app.models.edge import Edge
from app.models.policy import Policy
from app.algorithms.dijkstra import dijkstra_shortest_path
from app.algorithms.distance_vector import run_distance_vector
from app.algorithms.reachability import generate_reachability_tree
from app.algorithms.attack_path import find_all_paths, calculate_attack_path_risk
from app.algorithms.crc import compute_crc, verify_crc
from app.algorithms.framing import character_count_framing, byte_stuffing, bit_stuffing
from app.algorithms.leaky_bucket import simulate_leaky_bucket
from app.services.routing_service import RoutingService
from app.services.security_analyzer import SecurityAnalyzer
from app.services.attack_simulator import AttackSimulator
from app.api.auth import get_current_user, require_roles

router = APIRouter()

# In-memory state initialized from JSON
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data")
NETWORK_FILE = os.path.join(DATA_DIR, "sample_network.json")
POLICIES_FILE = os.path.join(DATA_DIR, "sample_policies.json")

CURRENT_NETWORK: Dict[str, Any] = {"nodes": {}, "edges": []}
AUDIT_LOGS: List[Dict[str, Any]] = []

def log_audit_event(username: str, action: str, details: Dict[str, Any]):
    AUDIT_LOGS.append({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "username": username,
        "action": action,
        "details": details
    })

def load_default_network():
    global CURRENT_NETWORK
    if os.path.exists(NETWORK_FILE):
        with open(NETWORK_FILE, "r") as f:
            data = json.load(f)
            nodes = {item["id"]: Node(**item) for item in data.get("nodes", [])}
            edges = [Edge(**item) for item in data.get("edges", [])]
            CURRENT_NETWORK = {"nodes": nodes, "edges": edges}

load_default_network()

@router.get("/network", tags=["Network Graph"])
def get_network_graph(user: Dict[str, Any] = Depends(get_current_user)):
    return {
        "nodes": [n.model_dump() for n in CURRENT_NETWORK["nodes"].values()],
        "edges": [e.model_dump() for e in CURRENT_NETWORK["edges"]]
    }

@router.post("/network/reset", tags=["Network Graph"])
def reset_network_graph(user: Dict[str, Any] = Depends(require_roles(["ADMIN", "SECURITY_ANALYST"]))):
    load_default_network()
    log_audit_event(user["username"], "RESET_NETWORK", {})
    return {"message": "Network graph reset to default state"}

@router.get("/routing/dijkstra", tags=["Routing Algorithms"])
def calculate_dijkstra(
    source: str = Query("internet"),
    destination: str = Query("db01"),
    user: Dict[str, Any] = Depends(get_current_user)
):
    result = dijkstra_shortest_path(CURRENT_NETWORK["nodes"], CURRENT_NETWORK["edges"], source, destination)
    log_audit_event(user["username"], "RUN_DIJKSTRA", {"source": source, "destination": destination})
    return result

@router.get("/routing/security-aware", tags=["Routing Algorithms"])
def calculate_security_aware_route(
    source: str = Query("internet"),
    destination: str = Query("db01"),
    user: Dict[str, Any] = Depends(get_current_user)
):
    result = RoutingService.calculate_routes(CURRENT_NETWORK["nodes"], CURRENT_NETWORK["edges"], source, destination)
    log_audit_event(user["username"], "RUN_SECURITY_AWARE_ROUTING", {"source": source, "destination": destination})
    return result

@router.get("/security/attack-paths", tags=["Security Analysis"])
def analyze_attack_paths(
    source: str = Query("internet"),
    target: str = Query("db01"),
    user: Dict[str, Any] = Depends(get_current_user)
):
    paths = find_all_paths(CURRENT_NETWORK["nodes"], CURRENT_NETWORK["edges"], source, target)
    evaluations = [calculate_attack_path_risk(p, CURRENT_NETWORK["nodes"], CURRENT_NETWORK["edges"]) for p in paths]
    log_audit_event(user["username"], "RUN_ATTACK_PATH_ANALYSIS", {"source": source, "target": target})
    return {"source": source, "target": target, "total_paths": len(paths), "attack_paths": evaluations}

@router.get("/security/findings", tags=["Security Analysis"])
def get_security_findings(user: Dict[str, Any] = Depends(get_current_user)):
    misconfigs = SecurityAnalyzer.analyze_network_misconfigurations(CURRENT_NETWORK["nodes"], CURRENT_NETWORK["edges"])
    spofs = SecurityAnalyzer.detect_single_points_of_failure(CURRENT_NETWORK["nodes"], CURRENT_NETWORK["edges"])
    return {"misconfigurations": misconfigs, "single_points_of_failure": spofs}

@router.post("/simulation/what-if", tags=["Simulation"])
def run_what_if_simulation(
    action: str = Query(..., description="COMPROMISE_NODE, DISABLE_NODE, or DISABLE_LINK"),
    target_id: str = Query(...),
    source_id: str = Query("internet"),
    dest_id: str = Query("db01"),
    user: Dict[str, Any] = Depends(require_roles(["ADMIN", "SECURITY_ANALYST"]))
):
    res = AttackSimulator.run_what_if_simulation(
        CURRENT_NETWORK["nodes"], CURRENT_NETWORK["edges"], action, target_id, source_id, dest_id
    )
    log_audit_event(user["username"], "RUN_WHAT_IF_SIMULATION", {"action": action, "target": target_id})
    return res

@router.get("/routing/distance-vector", tags=["Networking Syllabus Modules"])
def get_distance_vector(user: Dict[str, Any] = Depends(get_current_user)):
    return run_distance_vector(CURRENT_NETWORK["nodes"], CURRENT_NETWORK["edges"])

@router.get("/routing/reachability-tree", tags=["Networking Syllabus Modules"])
def get_reachability(source: str = Query("internet"), user: Dict[str, Any] = Depends(get_current_user)):
    return generate_reachability_tree(CURRENT_NETWORK["nodes"], CURRENT_NETWORK["edges"], source)

# Educational syllabus endpoints
class CRCRequest(BaseModel):
    data_bits: str
    polynomial: str = "CRC-16"

@router.post("/lab/crc/generate", tags=["Networking Syllabus Modules"])
def crc_generate(req: CRCRequest):
    return compute_crc(req.data_bits, req.polynomial)

class BitStuffingRequest(BaseModel):
    bit_stream: str

@router.post("/lab/framing/bit-stuffing", tags=["Networking Syllabus Modules"])
def bit_stuffing_demo(req: BitStuffingRequest):
    return bit_stuffing(req.bit_stream)

class LeakyBucketRequest(BaseModel):
    capacity: int = 10
    leak_rate: int = 3
    incoming_packets: List[int] = [4, 2, 6, 1, 8, 2]

@router.post("/lab/leaky-bucket", tags=["Networking Syllabus Modules"])
def leaky_bucket_demo(req: LeakyBucketRequest):
    return simulate_leaky_bucket(req.capacity, req.leak_rate, req.incoming_packets)

@router.get("/audit-logs", tags=["API Security"])
def get_audit_logs(user: Dict[str, Any] = Depends(require_roles(["ADMIN"]))):
    return {"audit_logs": AUDIT_LOGS}