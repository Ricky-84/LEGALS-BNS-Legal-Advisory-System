"""
User and session related database models
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class User(Base):
    """User model for storing user information"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_active = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    queries = relationship("LegalQuery", back_populates="user")


class LegalQuery(Base):
    """Legal query model for storing user queries and responses"""
    __tablename__ = "legal_queries"
    
    id = Column(Integer, primary_key=True, index=True)
    query_id = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(String, ForeignKey("users.user_id"), nullable=True)
    
    # Query details
    query_text = Column(Text, nullable=False)
    language = Column(String, default="en")
    
    # Processing results
    extracted_entities = Column(Text)  # JSON string
    applicable_laws = Column(Text)     # JSON string  
    legal_advice = Column(Text)
    confidence_score = Column(Float)
    
    # Metadata
    processing_time = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    verified = Column(Boolean, default=False)
    
    # Relationships
    user = relationship("User", back_populates="queries")


class QuerySession(Base):
    """Session model for tracking user sessions"""
    __tablename__ = "query_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(String, nullable=True)
    
    # Session details
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    last_activity = Column(DateTime(timezone=True), server_default=func.now())
    ended_at = Column(DateTime(timezone=True), nullable=True)
    
    # Session metadata
    queries_count = Column(Integer, default=0)
    language_preference = Column(String, default="en")