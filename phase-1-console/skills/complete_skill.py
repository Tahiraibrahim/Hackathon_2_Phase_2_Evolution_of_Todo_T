"""
Complete Task Skill

Capability to mark a task as completed or toggle its completion status.
"""

from utils import (
    Task,
    OperationResult,
    Status,
    find_task_by_id,
    update_task as storage_update_task,
    StorageError,
    ERROR_CODES
)
from datetime import datetime


def complete_task(
    task_id: int,
    uncomplete: bool = False,
    toggle: bool = False
) -> OperationResult:
    """
    Mark a task as completed (or incomplete).

    Args:
        task_id: ID of task to complete
        uncomplete: Mark as incomplete instead
        toggle: Toggle completion status

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

        # Create Task object to access methods
        task = Task.from_dict(task_dict)

        # Determine action
        if toggle:
            # Toggle current status
            if task.completed:
                task.mark_incomplete()
                action = "reopened"
            else:
                task.mark_completed()
                action = "completed"
        elif uncomplete:
            task.mark_incomplete()
            action = "reopened"
        else:
            task.mark_completed()
            action = "completed"

        # Update in storage
        updates = {
            'completed': task.completed,
            'status': task.status.value,
            'completed_at': task.completed_at,
            'updated_at': task.updated_at
        }

        success = storage_update_task(task_id, updates)

        if success:
            symbol = "✓" if task.completed else "○"
            return OperationResult.success_result(
                message=f"{symbol} Task #{task_id} {action}: \"{task.title}\"",
                data=task.to_dict()
            )
        else:
            return OperationResult.error_result(
                error=f"Failed to update task #{task_id}",
                code=ERROR_CODES["STORAGE_ERROR"]
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
