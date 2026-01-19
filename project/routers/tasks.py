from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from project.db.models.task import TaskCreate, TaskResponse, TaskStatus, TaskUpdate
from project.dependencies import AdminUserDep, CurrentUserDep, SessionDep
from project.exceptions import EntityNotFoundError, ValidationError
from project.services import task_service
from project.utils.pagination import PaginatedResponse, PaginationParams, get_pagination_params

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("", response_model=PaginatedResponse[TaskResponse])
def list_tasks(
    session: SessionDep,
    current_user: CurrentUserDep,
    pagination: Annotated[PaginationParams, Depends(get_pagination_params)],
    status_filter: TaskStatus | None = Query(default=None, alias="status"),
    assigned_to: UUID | None = Query(default=None),
) -> PaginatedResponse[TaskResponse]:
    """List tasks with pagination and optional filters."""
    result = task_service.get_tasks(
        session=session,
        pagination=pagination,
        status_filter=status_filter,
        assigned_to=assigned_to,
    )

    return PaginatedResponse(
        total=result.total,
        offset=result.offset,
        limit=result.limit,
        results=[TaskResponse.model_validate(task) for task in result.results],
    )


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> TaskResponse:
    """Create a new task."""
    try:
        task = task_service.create_task(session, task_data, current_user)
        return TaskResponse.model_validate(task)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.message,
        )


@router.get("/{task_uuid}", response_model=TaskResponse)
def get_task(
    task_uuid: UUID,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> TaskResponse:
    """Get a specific task by UUID."""
    try:
        task = task_service.get_task_by_uuid(session, task_uuid)
        return TaskResponse.model_validate(task)
    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )


@router.patch("/{task_uuid}", response_model=TaskResponse)
def update_task(
    task_uuid: UUID,
    task_data: TaskUpdate,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> TaskResponse:
    """Update an existing task."""
    try:
        task = task_service.update_task(session, task_uuid, task_data)
        return TaskResponse.model_validate(task)
    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.message,
        )


@router.delete("/{task_uuid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_uuid: UUID,
    session: SessionDep,
    admin_user: AdminUserDep,
) -> None:
    """Delete a task (admin only)."""
    try:
        task_service.delete_task(session, task_uuid)
    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
