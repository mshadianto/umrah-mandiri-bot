# -*- coding: utf-8 -*-
"""
Configuration with FREE APIs
"""
from pydantic_settings import BaseSettings
from typing import List, Optional

class Settings(BaseSettings):
    """Application settings with FREE API options"""
    
    # App
    APP_NAME: str = "Umrah Assistant API"
    DEBUG: bool = True
    VERSION: str = "2.0.0"
    
    # Database (optional for now)
    DATABASE_URL: Optional[str] = None
    REDIS_URL: Optional[str] = None
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # AI/ML - FREE OPTIONS
    GROQ_API_KEY: Optional[str] = None  # FREE! Get from console.groq.com
    OPENAI_API_KEY: Optional[str] = None  # Optional, only for embeddings
    
    # Vector DB
    QDRANT_URL: Optional[str] = "http://localhost:6333"
    QDRANT_API_KEY: Optional[str] = None
    
    # External APIs - FREE OPTIONS
    TELEGRAM_BOT_TOKEN: Optional[str] = None
    
    # Free Location Services (NO API KEY NEEDED!)
    NOMINATIM_USER_AGENT: str = "umrah-assistant-app"  # For OpenStreetMap
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()