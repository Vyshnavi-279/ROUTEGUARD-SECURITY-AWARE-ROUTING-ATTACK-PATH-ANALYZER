# RouteGuard — 15 Most Likely Interview Questions & Answers

### 1. What core problem does RouteGuard solve?
RouteGuard bridges Computer Networks and Security Engineering by demonstrating that standard shortest-path routing (e.g., Dijkstra) does not prioritize security. It calculates security-aware routes, evaluates attack-path risks, and simulates node compromises.

### 2. How does Dijkstra's algorithm work in your project?
We implemented Dijkstra from scratch using Python's `heapq` min-heap module. It maintains a priority queue of unvisited nodes sorted by cumulative weight and computes the minimum-cost route between source and target.

### 3. How does Security-Aware Routing differ from Dijkstra?
Standard Dijkstra only considers edge link weights (latency/cost). Security-Aware Routing applies constraints on node trust levels, encryption status, zone boundaries, and excludes compromised nodes.

### 4. How is the transparent risk score computed?
Risk scores (0–100) are rule-based and explainable:
- Critical asset exposure: +30
- Compromised node in path: +25
- Untrusted node traversal: +20
- DMZ/Zone bypass: +15
- Unencrypted links: +10

### 5. What is a Single Point of Failure (SPOF) in RouteGuard?
An active node or link whose failure renders a critical target (e.g., Database) unreachable from public zones.

### 6. How does your JWT authentication and RBAC work?
FastAPI handles token decoding and authorization headers. Roles (`ADMIN`, `SECURITY_ANALYST`, `VIEWER`) restrict specific sensitive endpoints (e.g., running simulations or resetting graphs).

### 7. Why include CRC and framing modules?
CRC, character count, and bit stuffing fulfill Computer Networks syllabus topics while emphasizing that error-detection codes like CRC handle transmission noise, NOT intentional adversarial tampering.

### 8. How are zone transitions handled?
Zones represent trust boundaries (INTERNET, DMZ, APPLICATION, DATABASE). Direct transitions bypassing DMZ trigger risk flags.

### 9. What happens during a What-If compromise simulation?
The engine creates a cloned copy of the network state, flags the target node as compromised, recalculates paths/risk scores, and computes a BEFORE vs AFTER impact delta.

### 10. How does the Distance-Vector module work?
It simulates distributed Bellman-Ford updates across routers until routing tables reach convergence.

### 11. What is the role of the Leaky Bucket module?
It demonstrates network traffic shaping and queue overflow dropping when input rate exceeds bucket capacity.

### 12. How are security misconfigurations detected?
Rule-based evaluation scans for direct internet connections to private databases, unencrypted inter-zone links, and excessive node privileges.

### 13. Is RouteGuard Docker compatible?
Yes, `docker-compose.yml` orchestrates the Python FastAPI backend and Nginx frontend in isolated containers.

### 14. What security headers are implemented?
The middleware injects `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `X-XSS-Protection: 1; mode=block`, and rate limiting.

### 15. How are secrets managed?
All sensitive settings (JWT secret, credentials) are loaded from `.env` via `pydantic-settings`.