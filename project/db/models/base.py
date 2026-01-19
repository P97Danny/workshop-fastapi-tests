from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class BaseModel(Base):
    """Abstract base model with common fields."""

    __abstract__ = True

    uuid: Mapped[UUID] = mapped_column(
        Uuid(),
        primary_key=True,
        default=uuid4,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(),
        default=datetime.now,
        nullable=False,
    )
