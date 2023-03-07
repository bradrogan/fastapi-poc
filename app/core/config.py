import pathlib

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, validator
from typing import List


# Project Directories
ROOT = pathlib.Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        else:
            return v

    DB_URI: str = "sqlite:///example.db"
    FIRST_SUPERUSER: EmailStr = EmailStr("admin@recipeapi.com")
    # 10 days = 10 days * 24 hours * 60 mintues
    ACCESS_TOKEN_EXPIRY_IN_MINUTES: float = 10 * 24 * 60
    JWT_SECRET: str = "placeholder secret"
    JWT_ALGORITHM: str = "HS256"

    class Config(BaseSettings.Config):
        case_sensitive: bool = True


settings: Settings = Settings()
