from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings


PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated=["auto"])


def hash_password(input_password: str) -> str:
    return PWD_CONTEXT.hash(input_password)


def verify_password(input_password: str, hashed_password: str) -> bool:
    return PWD_CONTEXT.verify(input_password, hashed_password)


def create_access_token(*, sub: str) -> str:
    payload = {}
    expire: datetime = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRY_IN_MINUTES
    )

    payload["type"] = "access_token"
    payload["exp"] = expire
    payload["iat"] = datetime.utcnow()
    payload["sub"] = sub

    return jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )
