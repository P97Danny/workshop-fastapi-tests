from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.db.models.base import BaseModel as BaseDBModel


class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"


class User(BaseDBModel):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(20), default=Role.USER.value, nullable=False)

    # relationships
    created_tasks: Mapped[list["Task"]] = relationship(  # noqa: F821
        "Task",
        back_populates="creator",
        foreign_keys="Task.created_by",
    )
    assigned_tasks: Mapped[list["Task"]] = relationship(  # noqa: F821
        "Task",
        back_populates="assignee",
        foreign_keys="Task.assigned_to",
    )


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Role = Role.USER


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uuid: UUID
    username: str
    email: str
    role: str
    created_at: datetime
