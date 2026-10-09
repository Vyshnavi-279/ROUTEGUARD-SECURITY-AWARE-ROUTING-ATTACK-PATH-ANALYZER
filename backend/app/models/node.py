from enum import Enum
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

class NodeType(str, Enum):
    USER = "USER"
    ROUTER = "ROUTER"
    FIREWALL = "FIREWALL"
    WEB_SERVER = "WEB_SERVER"
    APP_SERVER = "APP_SERVER"
    DATABASE = "DATABASE"
    INTERNET = "INTERNET"
    ADMIN = "ADMIN"
    SERVICE = "SERVICE"

class ZoneType(str, Enum):
    INTERNET = "INTERNET"
    DMZ = "DMZ"
    APPLICATION = "APPLICATION"
    PRIVATE = "PRIVATE"
    DATABASE = "DATABASE"
    MANAGEMENT = "MANAGEMENT"

class TrustLevel(str, Enum):
    UNTRUSTED = "UNTRUSTED"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class Criticality(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class Node(BaseModel):
    id: str
    name: str
    type: NodeType
    zone: ZoneType
    trust_level: TrustLevel = TrustLevel.MEDIUM
    criticality: Criticality = Criticality.LOW
    compromised: bool = False
    metadata: Dict[str, Any] = Field(default_factory=dict)