import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "KrishiMitra Backend API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    PORT: int = 8000
    HOST: str = "0.0.0.0"

    DATABASE_URL: str = "sqlite:///./krishimitra.db"

    AI_FALLBACK_PROVIDER: str = "local"  # 'local', 'openai', 'gemini'
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"

    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-1.5-flash"

    WEATHER_PROVIDER: str = "open_meteo"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
