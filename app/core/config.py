import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/lu_estilo_db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-super-secret-jwt-key")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    WHATSAPP_API_URL: str = os.getenv("WHATSAPP_API_URL", "https://api.whatsapp.com")
    WHATSAPP_API_TOKEN: str = os.getenv("WHATSAPP_API_TOKEN", "your_whatsapp_token")

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()