import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.api.routes import router as api_router
from app.api.auth import router as auth_router

# When running "cd backend && uvicorn app.main:app":
#   __file__ = /opt/render/project/src/backend/app/main.py
#   BASE_DIR  = /opt/render/project/src/   (project root, 3 levels up)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="Security-Aware Routing & Attack-Path Analyzer"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers — must be registered BEFORE the catch-all static route
app.include_router(auth_router, prefix="/api")
app.include_router(api_router, prefix="/api")


# --- Serve vis-network.min.js explicitly ---
@app.get("/vis-network.min.js")
async def serve_vis():
    vis_path = BASE_DIR / "vis-network.min.js"
    if vis_path.exists():
        return FileResponse(str(vis_path), media_type="application/javascript")
    return JSONResponse(status_code=404, content={"detail": "vis-network.min.js not found"})


# --- Health check ---
@app.get("/health")
async def health():
    return {"status": "ok", "version": "1.0.0"}


# --- Serve index.html for all non-API routes (SPA catch-all) ---
@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    # Don't intercept API routes (already handled above)
    if full_path.startswith("api/"):
        return JSONResponse(status_code=404, content={"detail": "Not found"})
    index_path = BASE_DIR / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path), media_type="text/html")
    return JSONResponse(
        status_code=503,
        content={"detail": "Frontend not found. Backend is running.", "base_dir": str(BASE_DIR)}
    )
