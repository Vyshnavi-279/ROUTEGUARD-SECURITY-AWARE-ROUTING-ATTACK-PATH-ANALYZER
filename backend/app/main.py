import copy
import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse

from app.core.config import settings
from app.api.routes import router as api_router
from app.api.auth import router as auth_router

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

# Include API routers
app.include_router(auth_router, prefix="/api")
app.include_router(api_router, prefix="/api")


# --- Static Asset Routes ---
@app.get("/vis-network.min.js")
async def serve_vis():
    vis_path = BASE_DIR / "vis-network.min.js"
    if vis_path.exists():
        return FileResponse(vis_path, media_type="application/javascript")
    return JSONResponse(status_code=404, content={"detail": "vis-network.min.js not found"})


@app.get("/")
async def serve_index():
    # Serve the main index.html from the project root
    index_path = BASE_DIR / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return {"project": "RouteGuard", "status": "running", "version": "1.0.0"}
