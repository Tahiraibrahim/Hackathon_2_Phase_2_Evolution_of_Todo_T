"""
Scheduler Skill

Capability to manage time-sensitive aspects of tasks including due dates,
reminders, and overdue detection.
"""

from typing import List
from datetime import datetime
from utils import (
    Task,
    OperationResult,
    load_tasks,
    update_task as storage_update_task,
    find_task_by_id,
    validate_due_date,
    StorageError,
    ERROR_CODES
)


def set_due_date(task_id: int, due_date: str) -> OperationResult:
    """
    Set due date for a task.

    Args:
        task_id: ID of task to update
        due_date: Due date in ISO 8601 format

    Returns:
        OperationResult with success status
    """
    try:
        # Find task
        task_dict = find_task_by_id(task_id)
        if not task_dict:
            return OperationResult.error_result(
                error=f"Task with ID {task_id} not found",
                code=ERROR_CODES["NOT_FOUND"]
            )

        # Validate due date
        validated_due_date = validate_due_date(due_date)

        # Update task
        success = storage_update_task(task_id, {'due_date': validated_due_date})

        if success:
            return OperationResult.success_result(
                message=f"Due date set for task #{task_id}",
                data={"task_id": task_id, "due_date": validated_due_date}
            )
        else:
            return OperationResult.error_result(
                error=f"Failed to update task #{task_id}",
                code=ERROR_CODES["STORAGE_ERROR"]
            )

    except ValueError as e:
        return OperationResult.error_result(
            error=str(e),
            code=ERROR_CODES["VALIDATION_ERROR"]
        )
    except StorageError as e:
        return OperationResult.error_result(
            error=str(e),
            code=ERROR_CODES["STORAGE_ERROR"]
        )
    except Exception as e:
        return OperationResult.error_result(
            error=f"Unexpected error: {e}",
            code="UNKNOWN_ERROR"
        )


def get_upcoming_tasks(days: int = 7) -> OperationResult:
    """
    Get tasks due within the specified number of days.

    Args:
        days: Number of days to look ahead (default 7)

    Returns:
        OperationResult with list of upcoming tasks
    """
    try:
        task_dicts = load_tasks()
        tasks = [Task.from_dict(t) for t in task_dicts]

        # Filter upcoming tasks
        now = datetime.utcnow()
        upcoming = []

        for task in tasks:
            if task.completed or not task.due_date:
                continue

            try:
                due = datetime.fromisoformat(task.due_date.replace('Z', '+00:00'))
                days_until = (due.replace(tzinfo=None) - now).days

                if 0 <= days_until <= days:
                    upcoming.append(task)
            except (ValueError, AttributeError):
                continue

        # Sort by due date
        upcoming.sort(key=lambda t: t.due_date or "")

        return OperationResult.success_result(
            message=f"Found {len(upcoming)} upcoming tasks",
            data=[t.to_dict() for t in upcoming]
        )

    except StorageError as e:
        return OperationResult.error_result(
            error=str(e),
            code=ERROR_CODES["STORAGE_ERROR"]
        )
    except Exception as e:
        return OperationResult.error_result(
            error=f"Unexpected error: {e}",
            code="UNKNOWN_ERROR"
        )


def get_overdue_tasks() -> OperationResult:
    """
    Get all overdue tasks.

    Returns:
        OperationResult with list of overdue tasks
    """
    try:
        task_dicts = load_tasks()
        tasks = [Task.from_dict(t) for t in task_dicts]

        # Filter overdue tasks
        overdue = [t for t in tasks if t.is_overdue()]

        # Sort by priority (high first) and days overdue
        overdue.sort(key=lambda t: (
            {'high': 0, 'medium': 1, 'low': 2}.get(t.priority.value, 3),
            t.days_until_due() or 0
        ))

        return OperationResult.success_result(
            message=f"Found {len(overdue)} overdue tasks",
            data=[t.to_dict() for t in overdue]
        )

    except StorageError as e:
        return OperationResult.error_result(
            error=str(e),
            code=ERROR_CODES["STORAGE_ERROR"]
        )
    except Exception as e:
        return OperationResult.error_result(
            error=f"Unexpected error: {e}",
            code="UNKNOWN_ERROR"
        )
