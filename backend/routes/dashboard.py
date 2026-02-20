"""
Dashboard routes — aggregated stats and metrics.
"""

from fastapi import APIRouter
from schemas import DashboardStats
from database import get_dashboard_stats

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/stats", response_model=DashboardStats)
async def dashboard_stats():
    """Get aggregated dashboard statistics."""
    stats = get_dashboard_stats()
    return DashboardStats(**stats)
