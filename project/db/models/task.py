from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from project.db.models.base import BaseModel as BaseDBModel


class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class Task(BaseDBModel):
    __tablename__ = "task"

    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default=TaskStatus.TODO.value, nullable=False)
    priority: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    due_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # foreign keys
    created_by: Mapped[UUID] = mapped_column(Uuid(), ForeignKey("user.uuid"), nullable=False)
    assigned_to: Mapped[UUID | None] = mapped_column(Uuid(), ForeignKey("user.uuid"), nullable=True)

    # relationships
    creator: Mapped["User"] = relationship(  # noqa: F821
        "User",
        back_populates="created_tasks",
        foreign_keys=[created_by],
    )
    assignee: Mapped["User | None"] = relationship(  # noqa: F821
        "User",
        back_populates="assigned_tasks",
        foreign_keys=[assigned_to],
    )


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = None
    status: TaskStatus = TaskStatus.TODO
    priority: int = Field(default=3, ge=1, le=5)
    due_date: datetime | None = None
    assigned_to: UUID | None = None

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, v: int) -> int:
        if not 1 <= v <= 5:
            raise ValueError("Priority must be between 1 and 5")
        return v


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    status: TaskStatus | None = None
    priority: int | None = Field(default=None, ge=1, le=5)
    due_date: datetime | None = None
    assigned_to: UUID | None = None


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uuid: UUID
    title: str
    description: str | None
    status: str
    priority: int
    due_date: datetime | None
    created_at: datetime
    created_by: UUID
    assigned_to: UUID | None
