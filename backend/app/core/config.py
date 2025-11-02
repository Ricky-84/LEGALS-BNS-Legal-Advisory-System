"""
Configuration settings for LEGALS backend
"""
import os
from typing import List


class Settings:
    """Application settings"""
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "LEGALS"
    VERSION: str = "2.0.0"
    
    # CORS Configuration
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",  # React dev server
        "http://localhost:8000",  # FastAPI
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ]
    
    # Database Configuration
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "password")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "legals_db")
    
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"
    
    # Neo4j Configuration
    NEO4J_URI: str = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USER: str = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD: str = os.getenv("NEO4J_PASSWORD", "Avirup@190204")
    
    # Ollama Configuration
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "phi3:mini")
    
    # External Services
    AZURE_TRANSLATOR_KEY: str = os.getenv("AZURE_TRANSLATOR_KEY", "")
    AZURE_TRANSLATOR_ENDPOINT: str = os.getenv("AZURE_TRANSLATOR_ENDPOINT", "")
    AZURE_TRANSLATOR_REGION: str = os.getenv("AZURE_TRANSLATOR_REGION", "")
    
    GOOGLE_SPEECH_CREDENTIALS: str = os.getenv("GOOGLE_SPEECH_CREDENTIALS", "")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Application Settings
    MAX_QUERY_LENGTH: int = 1000
    RESPONSE_TIMEOUT: int = 60  # seconds
    
    def __init__(self):
        """Initialize settings with environment variables"""
        # Override with environment variables if available
        self.POSTGRES_SERVER = os.getenv("POSTGRES_SERVER", self.POSTGRES_SERVER)
        self.POSTGRES_USER = os.getenv("POSTGRES_USER", self.POSTGRES_USER)
        self.POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", self.POSTGRES_PASSWORD)
        self.POSTGRES_DB = os.getenv("POSTGRES_DB", self.POSTGRES_DB)
        
        self.NEO4J_URI = os.getenv("NEO4J_URI", self.NEO4J_URI)
        self.NEO4J_USER = os.getenv("NEO4J_USER", self.NEO4J_USER)
        self.NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", self.NEO4J_PASSWORD)
        
        self.OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", self.OLLAMA_BASE_URL)
        self.OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", self.OLLAMA_MODEL)


settings = Settings()