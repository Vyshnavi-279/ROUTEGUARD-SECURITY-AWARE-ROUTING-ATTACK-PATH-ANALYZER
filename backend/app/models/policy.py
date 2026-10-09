from enum import Enum
from typing import Optional
from pydantic import BaseModel
from app.models.node import ZoneType, NodeType

class PolicyAction(str, Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"

class Policy(BaseModel):
    id: str
    name: str
    source_zone: Optional[ZoneType] = None
    destination_zone: Optional[ZoneType] = None
    source_type: Optional[NodeType] = None
    destination_type: Optional[NodeType] = None
    protocol: str = "*"
    port: Optional[int] = None
    action: PolicyAction = PolicyAction.ALLOW
    priority: int = 100
    description: str = ""