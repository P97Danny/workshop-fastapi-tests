from dataclasses import dataclass
from typing import Generic, Literal, Sequence, TypeVar

from fastapi import Query
from pydantic import BaseModel, Field

T = TypeVar("T")


@dataclass
class PaginatedData(Generic[T]):
    """Container for paginated query results."""

    total: int
    offset: int
    limit: int
    results: Sequence[T]


class PaginationParams(BaseModel):
    """Pagination parameters with validation."""

    limit: int = Field(default=10, gt=0, le=100)
    offset: int = Field(default=0, ge=0)
    sort_order: Literal["asc", "desc"] = "asc"


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response for API endpoints."""

    total: int
    offset: int
    limit: int
    results: list[T]


def get_pagination_params(
    limit: int = Query(default=10, gt=0, le=100, description="Items per page"),
    offset: int = Query(default=0, ge=0, description="Items to skip"),
    sort_order: Literal["asc", "desc"] = Query(default="asc", description="Sort order"),
) -> PaginationParams:
    """FastAPI dependency for pagination parameters."""
    return PaginationParams(limit=limit, offset=offset, sort_order=sort_order)


def calculate_total_pages(total: int, limit: int) -> int:
    """Calculate total number of pages."""
    if limit <= 0:
        return 0
    return (total + limit - 1) // limit


def has_next_page(total: int, offset: int, limit: int) -> bool:
    """Check if there's a next page."""
    return offset + limit < total


def has_previous_page(offset: int) -> bool:
    """Check if there's a previous page."""
    return offset > 0
