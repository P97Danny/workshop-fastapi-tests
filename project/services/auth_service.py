from datetime import timedelta

from sqlalchemy.orm import Session

from project.config import get_settings
from project.db.models.user import User
from project.exceptions import AuthenticationError
from project.security import Token, TokenPayload, create_access_token, verify_password
from project.services.user_service import get_user_by_username


def authenticate_user(session: Session, username: str, password: str) -> User:
    """Authenticate user by username and password."""
    try:
        user = get_user_by_username(session, username)
    except Exception:
        raise AuthenticationError("Invalid username or password")

    if not verify_password(password, user.password_hash):
        raise AuthenticationError("Invalid username or password")

    return user


def create_user_token(user: User) -> Token:
    """Create access token for authenticated user."""
    settings = get_settings()

    payload = TokenPayload(
        username=user.username,
        role=user.role,
        user_uuid=str(user.uuid),
    )

    expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    return create_access_token(payload, expires_delta)


def login_user(session: Session, username: str, password: str) -> Token:
    """Authenticate and return token."""
    user = authenticate_user(session, username, password)
    return create_user_token(user)
