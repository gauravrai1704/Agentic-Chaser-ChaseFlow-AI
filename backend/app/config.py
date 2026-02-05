"""
ChaseFlow AI Configuration
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "ChaseFlow AI"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    CORS_ORIGINS: list = [
    "http://localhost:3000",
    "http://localhost:5173",
    "https://agentic-chaser-chase-flow-ai.vercel.app",  
    "https://agentic-chaser-chase-flow-27snhnwvd-gauravrai1704s-projects.vercel.app" 
    ]
    
    # Database
    DATABASE_URL: str = "sqlite:///./chaseflow.db"
    
    # Anthropic API (optional - for enhanced AI features)
    ANTHROPIC_API_KEY: Optional[str] = None
    
    # Agent Configuration
    AGENT_POLL_INTERVAL: int = 30  # seconds
    MAX_RETRY_ATTEMPTS: int = 3
    ESCALATION_THRESHOLD_DAYS: int = 7
    
    # Provider Configuration
    PROVIDER_AVERAGE_RESPONSE_DAYS: dict = {
        "Aviva": 15,
        "Legal & General": 12,
        "Scottish Widows": 18,
        "Standard Life": 14,
        "Prudential": 20,
        "Aegon": 16,
        "Royal London": 13,
        "Zurich": 15
    }
    
    # Communication
    EMAIL_SIMULATION: bool = True
    SMS_SIMULATION: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
