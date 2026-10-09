from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class Severity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class SecurityFinding(BaseModel):
    id: str
    title: str
    severity: Severity
    description: str
    affected_nodes: List[str]
    why_it_matters: str
    recommendation: str

class PathRiskDetail(BaseModel):
    path: List[str]
    length: int
    total_cost: float
    risk_score: float
    severity: Severity
    reasons: List[str]
    trust_zone_transitions: int
    untrusted_nodes_count: int
    unencrypted_links_count: int
    has_compromised_nodes: bool
    policy_violations: List[str]

class RiskScoreBreakdown(BaseModel):
    score: float
    severity: Severity
    components: Dict[str, float]
    explanations: List[str]

class NetworkGraphModel(BaseModel):
    nodes: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]