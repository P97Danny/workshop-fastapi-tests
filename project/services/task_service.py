from uuid import UUID

from sqlalchemy import asc, desc, select
from sqlalchemy.orm import Session

from project.db.models.task import Task, TaskCreate, TaskStatus, TaskUpdate
from project.db.models.user import User
from project.exceptions import EntityNotFoundError, ValidationError
from project.utils.pagination import PaginatedData, PaginationParams


def get_task_by_uuid(session: Session, task_uuid: UUID) -> Task:
    """Get task by UUID, raises EntityNotFoundError if not found."""
    task = session.execute(
        select(Task).where(Task.uuid == task_uuid)
    ).scalar_one_or_none()

    if not task:
        raise EntityNotFoundError("Task", str(task_uuid))

    return task


def create_task(session: Session, task_data: TaskCreate, created_by: User) -> Task:
    """Create a new task."""
    if task_data.priority < 1 or task_data.priority > 5:
        raise ValidationError("Priority must be between 1 and 5", field="priority")

    task = Task(
        title=task_data.title,
        description=task_data.description,
        status=task_data.status.value,
        priority=task_data.priority,
        due_date=task_data.due_date,
        created_by=created_by.uuid,
        assigned_to=task_data.assigned_to,
    )

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


def update_task(session: Session, task_uuid: UUID, task_data: TaskUpdate) -> Task:
    """Update an existing task."""
    task = get_task_by_uuid(session, task_uuid)

    update_data = task_data.model_dump(exclude_unset=True)

    if "priority" in update_data and update_data["priority"] is not None:
        if update_data["priority"] < 1 or update_data["priority"] > 5:
            raise ValidationError("Priority must be between 1 and 5", field="priority")

    if "status" in update_data and update_data["status"] is not None:
        update_data["status"] = update_data["status"].value

    for key, value in update_data.items():
        setattr(task, key, value)

    session.commit()
    session.refresh(task)

    return task


def delete_task(session: Session, task_uuid: UUID) -> None:
    """Delete a task."""
    task = get_task_by_uuid(session, task_uuid)
    session.delete(task)
    session.commit()


def get_tasks(
    session: Session,
    pagination: PaginationParams,
    status_filter: TaskStatus | None = None,
    assigned_to: UUID | None = None,
) -> PaginatedData[Task]:
    """Get paginated tasks with optional filters."""
    query = select(Task)

    # apply filters
    if status_filter:
        query = query.where(Task.status == status_filter.value)

    if assigned_to:
        query = query.where(Task.assigned_to == assigned_to)

    # count total
    count_query = select(Task)
    if status_filter:
        count_query = count_query.where(Task.status == status_filter.value)
    if assigned_to:
        count_query = count_query.where(Task.assigned_to == assigned_to)

    total = len(list(session.execute(count_query).scalars().all()))

    # apply sorting
    order_func = asc if pagination.sort_order == "asc" else desc
    query = query.order_by(order_func(Task.created_at))

    # apply pagination
    query = query.offset(pagination.offset).limit(pagination.limit)

    results = list(session.execute(query).scalars().all())

    return PaginatedData(
        total=total,
        offset=pagination.offset,
        limit=pagination.limit,
        results=results,
    )
