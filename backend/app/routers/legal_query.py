"""
Legal query processing endpoints - Integrated with trained SLM
"""
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
import logging

from ..services.legal_processing_service import legal_processor

logger = logging.getLogger(__name__)
router = APIRouter()


class LegalQueryRequest(BaseModel):
    """Legal query request model"""
    query: str = Field(..., min_length=10, max_length=1000, description="Legal incident description")
    language: Optional[str] = Field("en", pattern="^(en|hi)$", description="Language: 'en' for English, 'hi' for Hindi")
    user_id: Optional[str] = Field(None, description="Optional user identifier")


class LegalQueryResponse(BaseModel):
    """Legal query response model"""
    query_id: str
    query: str
    language: str
    entities: Dict[str, List[str]]
    applicable_laws: List[Dict[str, Any]]
    legal_advice: str
    confidence_score: float
    processing_time: float
    timestamp: str
    verified: bool = False
    disclaimers: List[str]
    system_info: Optional[Dict[str, str]] = None


@router.post("/query", response_model=LegalQueryResponse)
async def process_legal_query(request: LegalQueryRequest):
    """
    Process a legal query through the complete integrated pipeline:
    1. Entity extraction using trained Phi-3 SLM (factual only)
    2. Legal reasoning using Neo4j deterministic rules
    3. Response generation using Phi-3 templates
    4. Fact verification and storage
    """
    try:
        logger.info(f"Processing legal query: {request.query[:100]}...")
        
        # Process through integrated SLM pipeline
        result = legal_processor.process_legal_query(
            query=request.query,
            language=request.language,
            user_id=request.user_id
        )
        
        # Handle error responses
        if "error" in result:
            logger.error(f"Query processing error: {result['error']}")
            raise HTTPException(
                status_code=500, 
                detail=f"Legal processing failed: {result['error']}"
            )
        
        # Convert to response model
        response = LegalQueryResponse(
            query_id=result["query_id"],
            query=result["query"],
            language=result["language"],
            entities=result["entities"],
            applicable_laws=result["applicable_laws"],
            legal_advice=result["legal_advice"],
            confidence_score=result["confidence_score"],
            processing_time=result["processing_time"],
            timestamp=result["timestamp"],
            verified=result.get("verified", False),
            disclaimers=result["disclaimers"],
            system_info=result.get("system_info")
        )
        
        logger.info(f"Query processed successfully: {result['query_id']}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error processing query: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Internal server error during legal query processing"
        )


@router.get("/query/{query_id}")
async def get_query_result(query_id: str):
    """Get results of a previously processed query"""
    try:
        # This would retrieve from database when implemented
        return {
            "message": f"Query {query_id} retrieval not yet implemented",
            "status": "pending_database_integration"
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Query {query_id} not found")


@router.get("/supported-laws")
async def get_supported_laws():
    """Get list of supported legal sections"""
    return {
        "supported_laws": [
            "BNS Chapter XVII - Property Offenses",
            "BNS Section 303 - Theft",
            "BNS Section 304 - Snatching", 
            "BNS Section 305 - Theft in dwelling house",
            "BNS Section 306 - Theft by employee",
            "BNS Section 308 - Extortion",
            "BNS Section 309 - Robbery"
        ],
        "total_sections": 6,
        "training_data": "Official BNS Chapter XVII",
        "entity_categories": [
            "persons", "objects", "locations", "actions", 
            "intentions", "circumstances", "relationships"
        ],
        "last_updated": datetime.utcnow().isoformat()
    }


@router.post("/extract-entities")
async def extract_entities_only(request: Dict[str, Any]):
    """Extract entities only (for testing entity extraction separately)"""
    try:
        query = request.get("query", "")
        language = request.get("language", "en")
        
        if not query or len(query.strip()) < 10:
            raise HTTPException(status_code=400, detail="Query must be at least 10 characters long")
        
        # Extract entities using SLM
        entities = legal_processor.ollama.extract_entities(query, language)
        
        return {
            "query": query,
            "language": language,
            "entities": entities,
            "extraction_method": "phi3_trained_slm",
            "note": "This extracts factual entities only - no legal classification"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Entity extraction failed: {str(e)}")


@router.get("/system-status")
async def get_system_status():
    """Get status of integrated legal processing system"""
    try:
        status = legal_processor.get_system_status()
        return status
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": "Failed to check system status"
        }