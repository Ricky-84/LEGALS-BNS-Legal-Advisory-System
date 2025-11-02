"""
Health check endpoints
"""
from fastapi import APIRouter
from datetime import datetime

router = APIRouter()


@router.get("/")
async def health_check():
    """Basic health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "LEGALS Backend"
    }


@router.get("/detailed")
async def detailed_health_check():
    """Detailed health check including dependencies"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "LEGALS Backend",
        "dependencies": {
            "postgres": "checking...",
            "neo4j": "checking...",
            "ollama": "checking..."
        }
    }