from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # PostgreSQL
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    # MinIO
    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: str
    MINIO_ENDPOINT: str = "minio:9000"
    MINIO_BUCKET: str = "cloud-storage"

    # JWT
    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@db:5432/{self.POSTGRES_DB}"
        )

    @property
    def MINIO_URL(self) -> str:
        return f"http://{self.MINIO_ENDPOINT}"

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()
