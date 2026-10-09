1. Executive Summary
RouteGuard is a security-aware network routing engine, architecture risk analyzer, and interactive simulation dashboard. Built as a portfolio-grade Computer Science & Cybersecurity project, it bridges core networking topics (graph routing, distance-vector protocols, framing, error detection) with modern Application and Cloud Security engineering practices (attack-path analysis, single point of failure detection, RBAC, JWT security, and Docker containerization).

2. System Architecture & Component Design

3. +-----------------------------------------------------------------------+
|                           FRONTEND LAYER                              |
|   HTML5 / Tailwind CSS / VisNetwork.js Graph Dashboard (Port 3000)    |
+-----------------------------------+-----------------------------------+
                                    |
                                    | HTTP / REST (JSON) + JWT
                                    v
+-----------------------------------------------------------------------+
|                            BACKEND LAYER                              |
|                   FastAPI REST Engine (Port 8000)                     |
|                                                                       |
|  +--------------------+  +----------------------+  +---------------+  |
|  | Auth & Security    |  | Routing & Algorithms |  | Analysis      |  |
|  | - JWT Bearer Tokens|  | - Custom Dijkstra    |  | - Attack Paths|  |
|  | - Password Hashing |  | - Distance Vector    |  | - SPOF Engine |  |
|  | - RBAC Middleware  |  | - Security-Aware     |  | - What-If Sim |  |
|  +--------------------+  +----------------------+  +---------------+  |
|                                                                       |
|  +-----------------------------------------------------------------+  |
|  | Syllabus Educational Modules                                     |  |
|  | - CRC-12 / CRC-16 / CRC-CCITT (Polynomial Modulo-2 Division)   |  |
|  | - Bit & Byte Framing / Leaky Bucket Traffic Shaper             |  |
|  +-----------------------------------------------------------------+  |
+-----------------------------------+-----------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------+
|                          DATA & STATE STORE                           |
|      JSON Topology Seed Data (`/data/sample_network.json`) + Memory   |
+-----------------------------------------------------------------------+

1. Directory Layout
   RouteGuard/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                     # FastAPI application entrypoint & middleware
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py                 # JWT Authentication & RBAC endpoints
│   │   │   └── routes.py               # Graph, routing, simulation, & lab endpoints
│   │   ├── algorithms/
│   │   │   ├── __init__.py
│   │   │   ├── dijkstra.py             # Custom Min-Heap Dijkstra implementation
│   │   │   ├── distance_vector.py      # Bellman-Ford Distance Vector simulator
│   │   │   ├── reachability.py          # BFS Reachability Tree & Policy Pruning
│   │   │   ├── attack_path.py          # DFS Path Finding & Risk Score Engine
│   │   │   ├── crc.py                  # CRC Polynomial Generation & Verification
│   │   │   ├── framing.py              # Bit & Byte Stuffing algorithms
│   │   │   └── leaky_bucket.py         # Leaky Bucket Traffic Shaper
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── node.py                 # Node schema (Type, Zone, Trust Level)
│   │   │   ├── edge.py                 # Link schema (Cost, Encryption, Active status)
│   │   │   ├── policy.py               # Security Policy rules schema
│   │   │   ├── network.py              # In-memory graph structure
│   │   │   └── security.py             # Findings & Path Risk models
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── routing_service.py      # Dijkstra vs Security-Aware route comparison
│   │   │   ├── security_analyzer.py    # Misconfigurations & SPOF detector
│   │   │   └── attack_simulator.py     # What-If node/link mutation engine
│   │   └── core/
│   │       ├── __init__.py
│   │       ├── config.py               # Application environment configurations
│   │       └── security.py             # Password hashing (Bcrypt) & JWT encoding
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_dijkstra.py
│   │   ├── test_attack_paths.py
│   │   └── test_crc_and_framing.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   └── public/
│       └── index.html                  # Interactive VisNetwork Dashboard
├── data/
│   ├── sample_network.json             # Seed topology
│   └── sample_policies.json            # Security zone policies
├── docs/
│   ├── interview_questions.md          # 15 Key Interview Q&As
│   └── spec.md                         # Full technical specification
├── scripts/
│   └── run_demo.py                     # CLI verification script
├── .env.example
├── .gitignore
├── docker-compose.yml
├── pytest.ini                          # Test configuration (sets pythonpath = backend)
└── README.md

4. Core Algorithms & Risk Score Model
4.1 Dijkstra's Algorithm (Custom Min-Heap)
Time Complexity: O((V+E)logV)
Implementation: Uses Python's native heapq library to traverse graph adjacency lists.
Security-Aware Mode: Excludes nodes flagged as compromised or links marked as inactive (active = False), re-routing traffic along verified non-compromised channels.
4.2 Transparent Risk Score Engine
Risk scores range from 0 to 100, calculated using transparent, deterministic penalty rules:
Critical Resource Target Exposure: +30 pts
Compromised Node Traversal: +25 pts
Untrusted / Low-Trust Node Traversal: +20 pts
DMZ / Inner Zone Direct Bypass: +15 pts
Unencrypted Link Traversal: +10 pts
Severity Tiers:
0 - 19: LOW
20 - 39: MEDIUM
40 - 69: HIGH
70 - 100: CRITICAL

5. REST API Specification
Authentication & Authorization
Method	Endpoint	Access Level	Description
POST	/api/auth/login	Public	Authenticates credentials and returns JWT bearer token.
GET	/api/auth/me	Authenticated	Returns current authenticated user details and role.
Network & Security Endpoints
Method	  Endpoint	                     Access Level	              Description
GET	    /api/network	                Authenticated	   Retrieves active network topology (nodes & edges).
POST	/api/network/reset	            ADMIN, ANALYST	   Resets the network graph to default state.
GET	    /api/routing/dijkstra	        Authenticated	   Calculates shortest path between source and target.
GET	    /api/routing/security-aware. 	Authenticated	   Compares standard shortest path with security-aware path.
GET	    /api/security/attack-paths	    Authenticated	   Evaluates all simple paths and returns risk breakdown.
GET	    /api/security/findings	        Authenticated	   Detects network misconfigurations and single points of failure.
POST	/api/simulation/what-if	        ADMIN, ANALYST	   Simulates node compromise or failure and returns BEFORE vs AFTER metrics.

6. Testing & Module Execution
To run automated tests with proper path resolution:
Bash
# Method 1: Using pytest.ini (configured with pythonpath = backend)
pytest backend/tests

# Method 2: Explicit PYTHONPATH execution
PYTHONPATH=backend pytest backend/tests
To execute the standalone demo script:
Bash
python scripts/run_demo.py

7. Security & Compliance
Authentication: Standard JWT Bearer Tokens using HS256.
Password Security: Password hashing using passlib with bcrypt.
Role-Based Access Control (RBAC): Three user roles (ADMIN, SECURITY_ANALYST, VIEWER).
HTTP Security Headers: Injected headers include X-Content-Type-Options: nosniff, X-Frame-Options: DENY, and X-XSS-Protection: 1; mode=block.
Rate Limiting: IP-based request throttling (max 120 requests/minute).