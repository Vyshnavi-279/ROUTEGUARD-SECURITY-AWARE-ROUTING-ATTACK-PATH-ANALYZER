@echo off
echo ========================================================
echo          STARTING ROUTEGUARD SECURITY ENGINE          
echo ========================================================

if not exist .venv (
    echo [+] Creating Python virtual environment...
    python -m venv .venv
)

call .venv\Scripts\activate.bat

echo [+] Installing backend dependencies...
pip install -r backend\requirements.txt

set PYTHONPATH=backend

start "RouteGuard Backend API" cmd /k "uvicorn app.main:app --host 0.0.0.0 --port 8000"
start "RouteGuard Web Dashboard" cmd /k "cd frontend\public && python -m http.server 3000"

echo.
echo ========================================================
echo  RouteGuard is live!
echo  - Web Dashboard: http://localhost:3000
echo  - API Docs (Swagger): http://localhost:8000/docs
echo ========================================================
pause
