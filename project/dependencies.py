from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from project.db.db import get_session
from project.db.models.user import Role, User
from project.security import decode_token
from project.services.user_service import get_user_by_username

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
SessionDep = Annotated[Session, Depends(get_session)]


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: SessionDep,
) -> User:
    """Get current authenticated user from JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        token_data = decode_token(token)

        if token_data.username is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    try:
        user = get_user_by_username(session, token_data.username)
    except Exception:
        raise credentials_exception

    return user


def require_admin(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Require current user to have admin role."""
    if current_user.role != Role.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user


CurrentUserDep = Annotated[User, Depends(get_current_user)]
AdminUserDep = Annotated[User, Depends(require_admin)]
