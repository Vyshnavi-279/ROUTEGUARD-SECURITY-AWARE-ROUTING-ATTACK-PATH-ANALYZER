import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "RouteGuard"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = "routeguard-super-secret-jwt-key-2026-btech-cse"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120

    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "AdminSecurePassword123!"
    ANALYST_USERNAME: str = "analyst"
    ANALYST_PASSWORD: str = "AnalystSecurePassword123!"
    VIEWER_USERNAME: str = "viewer"
    VIEWER_PASSWORD: str = "ViewerSecurePassword123!"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()