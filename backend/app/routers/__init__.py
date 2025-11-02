"""
API Routers for LEGALS
"""
from fastapi import APIRouter

from .legal_query import router as legal_router
from .health import router as health_router

# Main API router
api_router = APIRouter()

# Include sub-routers
api_router.include_router(health_router, prefix="/health", tags=["health"])
api_router.include_router(legal_router, prefix="/legal", tags=["legal"])