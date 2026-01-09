"""
Update Task Skill

Capability to modify existing task attributes.
"""

from typing import Optional
from utils import (
    Task,
    OperationResult,
    Priority,
    Status,
    find_task_by_id,
    update_task as storage_update_task,
    validate_title,
    validate_category,
    validate_due_date,
    StorageError,
    ERROR_CODES
)


def update_task(
    task_id: int,
    title: Optional[str] = None,
    priority: Optional[str] = None,
    category: Optional[str] = None,
    status: Optional[str] = None,
    due_date: Optional[str] = None
) -> OperationResult:
    """
    Update an existing task.

    Args:
        task_id: ID of task to update
        title: New title
        priority: New priority (high/medium/low)
        category: New category
        status: New status (pending/in_progress/completed)
        due_date: New due date (ISO 8601)

    Returns:
        OperationResult with success status and updated task
    """
    try:
        # Check if at least one field provided
        if not any([title, priority, category, status, due_date]):
            return OperationResult.error_result(
                error="No fields to update. Please specify at least one field.",
                code=ERROR_CODES["NO_CHANGES"]
            )

        # Find task
        task_dict = find_task_by_id(task_id)
        if not task_dict:
            return OperationResult.error_result(
                error=f"Task with ID {task_id} not found",
                code=ERROR_CODES["NOT_FOUND"]
            )

        # Build updates dict
        updates = {}
        changes = []

        if title is not None:
            updates['title'] = validate_title(title)
            changes.append("title")

        if priority is not None:
            priority_enum = Priority.from_string(priority)
            updates['priority'] = priority_enum.value
            changes.append("priority")

        if category is not None:
            updates['category'] = validate_category(category)
            changes.append("category")

        if status is not None:
            status_enum = Status.from_string(status)
            updates['status'] = status_enum.value
            # Update completed flag if status is completed
            if status_enum == Status.COMPLETED:
                updates['completed'] = True
            changes.append("status")

        if due_date is not None:
            updates['due_date'] = validate_due_date(due_date) if due_date else None
            changes.append("due_date")

        # Update task
        success = storage_update_task(task_id, updates)

        if success:
            # Get updated task
            updated_task = find_task_by_id(task_id)
            return OperationResult.success_result(
                message=f"Task #{task_id} updated successfully ({', '.join(changes)} changed)",
                data=updated_task
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
