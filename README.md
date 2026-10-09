# RouteGuard — Security-Aware Routing & Attack-Path Analyzer

> A full-stack network security analysis dashboard with JWT auth, RBAC, graph visualization, and real-time attack path detection.

## 🌐 Live Demo

**[https://routeguard-security-aware-routing-attack-7fl2.onrender.com](https://routeguard-security-aware-routing-attack-7fl2.onrender.com)**

### Login Credentials

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `AdminSecurePassword123!` |
| Analyst | `analyst` | `AnalystSecurePassword123!` |
| Viewer | `viewer` | `ViewerSecurePassword123!` |

---

## Features

- **Network Graph Visualization** — Interactive vis-network topology
- **Dijkstra Shortest Path** — Classic and security-aware routing
- **Attack Path Analysis** — All paths with risk scoring
- **What-If Simulation** — Compromise/disable nodes and links
- **Distance Vector Routing** — Bellman-Ford implementation
- **Reachability Tree** — BFS with policy enforcement
- **CRC & Framing Lab** — CRC-16/32, bit stuffing demos
- **Leaky Bucket** — Traffic shaping simulation
- **JWT Authentication** — HS256 tokens, 2-hour expiry
- **RBAC** — ADMIN / SECURITY_ANALYST / VIEWER roles
- **Audit Logs** — All actions logged with timestamp + user
- **Notifications** — Real-time event feed

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | FastAPI, Python 3.14 |
| Auth | python-jose (JWT), bcrypt |
| Algorithms | Custom implementations (no networkx for core logic) |
| Frontend | Vanilla JS, vis-network.js |
| Deploy | Render (free tier) |

---

## Local Development

```bash
# Clone
git clone https://github.com/Vyshnavi-279/ROUTEGUARD-SECURITY-AWARE-ROUTING-ATTACK-PATH-ANALYZER.git
cd ROUTEGUARD-SECURITY-AWARE-ROUTING-ATTACK-PATH-ANALYZER

# Install dependencies
pip install -r requirements.txt

# Run (from project root)
cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open [http://localhost:8000](http://localhost:8000)

---

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── main.py          ← FastAPI app + frontend serving
│   │   ├── api/
│   │   │   ├── routes.py    ← All API endpoints
│   │   │   └── auth.py      ← JWT login + RBAC
│   │   ├── algorithms/
│   │   │   ├── dijkstra.py
│   │   │   ├── attack_path.py
│   │   │   ├── reachability.py
│   │   │   ├── distance_vector.py
│   │   │   ├── crc.py
│   │   │   ├── framing.py
│   │   │   └── leaky_bucket.py
│   │   ├── models/          ← Pydantic models
│   │   ├── services/        ← SecurityAnalyzer, AttackSimulator
│   │   └── core/            ← Config, JWT utils
│   └── tests/               ← pytest (5 tests, all passing)
├── data/
│   ├── sample_network.json  ← Default topology
│   └── sample_policies.json
├── index.html               ← Full frontend (single file)
├── vis-network.min.js       ← Graph library
├── requirements.txt
├── render.yaml              ← Render deployment config
└── Procfile
```

---

## API Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/api/auth/login` | — | Get JWT token |
| GET | `/api/auth/me` | ✓ | Current user info |
| GET | `/api/network` | ✓ | Network topology |
| POST | `/api/network/reset` | ADMIN | Reset to default |
| GET | `/api/routing/dijkstra` | ✓ | Shortest path |
| GET | `/api/routing/security-aware` | ✓ | Security-weighted route |
| GET | `/api/routing/distance-vector` | ✓ | Distance vector table |
| GET | `/api/routing/reachability-tree` | ✓ | BFS reachability |
| GET | `/api/security/attack-paths` | ✓ | All attack paths + risk |
| GET | `/api/security/findings` | ✓ | Misconfigs + SPOFs |
| POST | `/api/simulation/what-if` | ADMIN/ANALYST | What-if simulation |
| POST | `/api/lab/crc/generate` | — | CRC computation |
| POST | `/api/lab/framing/bit-stuffing` | — | Bit stuffing demo |
| POST | `/api/lab/leaky-bucket` | — | Leaky bucket sim |
| GET | `/api/audit-logs` | ADMIN | Full audit trail |
| GET | `/api/notifications` | ✓ | User notifications |
| GET | `/api/user/profile` | ✓ | Profile + permissions |
| GET | `/health` | — | Health check |
