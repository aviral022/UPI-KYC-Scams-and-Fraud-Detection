"""
Real-Time Scam & Fraud Intelligence System for India
FastAPI Backend — Main Entry Point
"""

import os
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv

from database import init_db
from routes import reports, analysis, dashboard

# Load environment variables
load_dotenv()

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ── Constants ──────────────────────────────────────────────────

FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")

# ── Lifespan ───────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database and log status on startup."""
    init_db()
    print("[OK] Database initialized")
    print(f"[INFO] Frontend directory: {FRONTEND_DIR}")
    if os.environ.get("GEMINI_API_KEY"):
        print("[AI] Gemini API key detected -- AI analysis enabled")
    else:
        print("[WARN] No GEMINI_API_KEY set -- AI analysis disabled (risk scoring still works)")
    yield


# ── App Setup ──────────────────────────────────────────────────

app = FastAPI(
    title="Fraud Intelligence System",
    description="Real-Time Scam & Fraud Intelligence System for India",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Register Routes ────────────────────────────────────────────

app.include_router(reports.router)
app.include_router(analysis.router)
app.include_router(dashboard.router)

# ── Serve Frontend ─────────────────────────────────────────────

if os.path.isdir(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

    @app.get("/")
    async def serve_frontend():
        return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))


if __name__ == "__main__":
    import uvicorn
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(backend_dir)
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=[backend_dir],
        reload_excludes=["*.db", "*.pyc", "__pycache__", "venv"],
    )
