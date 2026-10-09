#!/bin/bash
echo "========================================================"
echo "          STARTING ROUTEGUARD SECURITY ENGINE          "
echo "========================================================"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "[+] Creating Python virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
echo "[+] Checking and installing dependencies..."
pip install -r backend/requirements.txt

# Start Backend Server
echo "[+] Launching RouteGuard Backend API on http://localhost:8000..."
PYTHONPATH=backend uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# Serve Frontend
echo "[+] Launching RouteGuard Web Dashboard on http://localhost:3000..."
cd frontend/public && python3 -m http.server 3000 &
FRONTEND_PID=$!

sleep 2
echo ""
echo "========================================================"
echo "  RouteGuard is live!"
echo "  - Web Dashboard: http://localhost:3000"
echo "  - API Docs (Swagger): http://localhost:8000/docs"
echo "========================================================"
echo "Press CTRL+C to stop both servers."

trap "kill $BACKEND_PID $FRONTEND_PID" EXIT
wait