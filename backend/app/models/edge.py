from typing import List, Optional
from pydantic import BaseModel, Field

class Edge(BaseModel):
    id: Optional[str] = None
    source: str
    destination: str
    cost: float = Field(default=1.0, ge=0.1)
    bidirectional: bool = True
    allowed_protocols: List[str] = Field(default_factory=lambda: ["TCP", "HTTP", "HTTPS"])
    encrypted: bool = True
    trusted: bool = True
    active: bool = True