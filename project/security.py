from datetime import datetime, timedelta, timezone

import bcrypt
from jose import jwt
from pydantic import BaseModel

from project.config import get_settings


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

    def __str__(self) -> str:
        return self.access_token


class TokenData(BaseModel):
    username: str | None = None


class TokenPayload(BaseModel):
    username: str
    role: str
    user_uuid: str


def encrypt_password(password: str) -> str:
    """Hash a password using bcrypt."""
    password_bytes = password.encode("utf-8")
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )


def create_access_token(
    payload: TokenPayload,
    expires_delta: timedelta | None = None,
) -> Token:
    """Create a JWT access token from payload."""
    settings = get_settings()

    to_encode = payload.model_dump()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode["exp"] = expire

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    return Token(access_token=encoded_jwt)


def decode_token(token: str) -> TokenData:
    """Decode a JWT token and return token data."""
    settings = get_settings()

    payload = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
    )

    username = payload.get("username")
    return TokenData(username=username)
