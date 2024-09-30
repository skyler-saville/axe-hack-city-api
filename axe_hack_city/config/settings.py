from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    database_file: str = "app.db"
    database_url: str = f"sqlite:///{os.path.join(os.path.dirname(__file__), '..', database_file)}"
    environment: str  # Add this if you want to capture the environment

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "forbid"  # Can be "allow" if you want to accept extra inputs

settings = Settings()
