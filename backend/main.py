"""
LEGALS FastAPI Backend Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.websockets import WebSocket
import uvicorn

from app.core.config import settings
from app.routers import api_router
from app.services.ollama_service import ollama_service
from app.services.neo4j_service import neo4j_service

# Initialize FastAPI application
app = FastAPI(
    title="LEGALS API",
    description="Legal Empowerment and Awareness System - Backend API",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "LEGALS API",
        "version": "2.0.0",
        "status": "operational",
        "features": {
            "entity_extraction": "enabled",
            "legal_reasoning": "enabled", 
            "multilingual_support": "enabled",
            "slm_integration": "phi3-trained"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint with SLM status"""
    # Check Ollama service
    ollama_status = ollama_service.test_connection()
    
    return {
        "status": "healthy",
        "services": {
            "ollama": ollama_status.get("status", "unknown"),
            "neo4j": "checking...",
            "postgres": "checking..."
        },
        "model": settings.OLLAMA_MODEL,
        "timestamp": "2024-01-01T00:00:00Z"
    }


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time communication"""
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
    except Exception as e:
        print(f"WebSocket error: {e}")
        await websocket.close()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )