"""Application configuration using Pydantic Settings."""
import os
from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    app_name: str = "CareerForge AI"
    debug: bool = True
    secret_key: str = "dev-secret-key"
    access_token_expire_minutes: int = 30
    database_url: str = "sqlite:///./careerforge.db"
    ai_provider: str = "mock"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    mock_ai_mode: bool = True
    frontend_url: str = "http://localhost:5173"
    max_upload_size: int = 5 * 1024 * 1024  # 5MB
    upload_dir: str = str(BASE_DIR / "uploads")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
