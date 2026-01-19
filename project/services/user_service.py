from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from project.db.models.user import User, UserCreate
from project.exceptions import EntityNotFoundError
from project.security import encrypt_password


def get_user_by_uuid(session: Session, user_uuid: UUID) -> User:
    """Get user by UUID, raises EntityNotFoundError if not found."""
    user = session.execute(
        select(User).where(User.uuid == user_uuid)
    ).scalar_one_or_none()

    if not user:
        raise EntityNotFoundError("User", str(user_uuid))

    return user


def get_user_by_username(session: Session, username: str) -> User:
    """Get user by username, raises EntityNotFoundError if not found."""
    user = session.execute(
        select(User).where(User.username == username)
    ).scalar_one_or_none()

    if not user:
        raise EntityNotFoundError("User", username)

    return user


def create_user(session: Session, user_data: UserCreate) -> User:
    """Create a new user."""
    user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=encrypt_password(user_data.password),
        role=user_data.role.value,
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


def get_all_users(session: Session) -> list[User]:
    """Get all users."""
    result = session.execute(select(User))
    return list(result.scalars().all())
