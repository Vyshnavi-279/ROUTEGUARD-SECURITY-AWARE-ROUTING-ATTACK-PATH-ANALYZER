"""
Vercel serverless entry point for RouteGuard FastAPI backend.
This file is picked up by @vercel/python and must expose an ASGI `app` object.
"""
import sys
import os

# Add the backend directory to sys.path so `from app.xxx import yyy` works
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from app.main import app  # noqa: F401 - re-exported for Vercel
