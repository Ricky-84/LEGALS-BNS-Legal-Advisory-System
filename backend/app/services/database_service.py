"""
Database service for PostgreSQL operations
"""
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime
import json
import uuid

from app.models.database import get_db
from app.models.user_models import User, LegalQuery, QuerySession


class DatabaseService:
    """Service for database operations"""
    
    def __init__(self):
        pass
    
    def create_user(self, db: Session, user_id: str = None) -> User:
        """Create a new user"""
        if not user_id:
            user_id = str(uuid.uuid4())
        
        user = User(user_id=user_id)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    def get_user(self, db: Session, user_id: str) -> Optional[User]:
        """Get user by user_id"""
        return db.query(User).filter(User.user_id == user_id).first()
    
    def create_query_session(self, db: Session, user_id: str = None) -> QuerySession:
        """Create a new query session"""
        session = QuerySession(
            session_id=str(uuid.uuid4()),
            user_id=user_id
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        return session
    
    def save_legal_query(
        self, 
        db: Session, 
        query_text: str,
        language: str,
        entities: Dict[str, Any],
        applicable_laws: List[Dict[str, Any]],
        legal_advice: str,
        confidence_score: float,
        processing_time: float,
        user_id: str = None
    ) -> LegalQuery:
        """Save a legal query and its results"""
        
        query = LegalQuery(
            query_id=str(uuid.uuid4()),
            user_id=user_id,
            query_text=query_text,
            language=language,
            extracted_entities=json.dumps(entities),
            applicable_laws=json.dumps(applicable_laws),
            legal_advice=legal_advice,
            confidence_score=confidence_score,
            processing_time=processing_time
        )
        
        db.add(query)
        db.commit()
        db.refresh(query)
        return query
    
    def get_query_by_id(self, db: Session, query_id: str) -> Optional[LegalQuery]:
        """Get query by query_id"""
        return db.query(LegalQuery).filter(LegalQuery.query_id == query_id).first()
    
    def get_user_queries(self, db: Session, user_id: str, limit: int = 10) -> List[LegalQuery]:
        """Get recent queries for a user"""
        return (
            db.query(LegalQuery)
            .filter(LegalQuery.user_id == user_id)
            .order_by(LegalQuery.created_at.desc())
            .limit(limit)
            .all()
        )
    
    def update_query_verification(self, db: Session, query_id: str, verified: bool) -> bool:
        """Update query verification status"""
        query = self.get_query_by_id(db, query_id)
        if query:
            query.verified = verified
            db.commit()
            return True
        return False
    
    def get_query_statistics(self, db: Session) -> Dict[str, Any]:
        """Get query statistics for analytics"""
        total_queries = db.query(LegalQuery).count()
        verified_queries = db.query(LegalQuery).filter(LegalQuery.verified == True).count()
        
        avg_confidence = (
            db.query(LegalQuery.confidence_score)
            .filter(LegalQuery.confidence_score.isnot(None))
            .all()
        )
        
        if avg_confidence:
            avg_confidence_score = sum(score[0] for score in avg_confidence) / len(avg_confidence)
        else:
            avg_confidence_score = 0.0
        
        return {
            "total_queries": total_queries,
            "verified_queries": verified_queries,
            "verification_rate": verified_queries / total_queries if total_queries > 0 else 0,
            "average_confidence": avg_confidence_score
        }


# Global database service instance
database_service = DatabaseService()