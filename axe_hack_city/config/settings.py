from pathlib import Path

from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DB_PATH = BASE_DIR / "app.db"


class Settings(BaseSettings):
    database_file: str = str(DEFAULT_DB_PATH)
    database_url: str = f"sqlite:///{DEFAULT_DB_PATH}"
    environment: str = "development"

    minio_endpoint: str = "localhost:9000"
    minio_access_key: str = "minioadmin"
    minio_secret_key: str = "minioadmin"
    minio_bucket: str = "axe-hack-city-assets"
    minio_secure: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "forbid"


settings = Settings()
