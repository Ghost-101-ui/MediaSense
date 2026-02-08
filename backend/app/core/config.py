import secrets
from typing import List, Union
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "MediaSense API"
    
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:3000"]'
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ]
    
    COOKIES_CONTENT: str = ""
    PROXY_URL: str = ""  # Optional: For bypassing YouTube IP blocks (e.g., http://user:pass@host:port)

    class Config:
        case_sensitive = True

settings = Settings()
