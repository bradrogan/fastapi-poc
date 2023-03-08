from os import path
from typing import Generator
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session
from app.core.config import settings

from app.db.session import SessionLocal


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(
    tokenUrl=path.join(settings.API_V1_STR, "users/login")
)
