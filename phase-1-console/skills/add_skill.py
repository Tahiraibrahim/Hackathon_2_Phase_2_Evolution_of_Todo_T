"""
Add Task Skill

Capability to add a new todo task to the system with customizable attributes.
"""

from datetime import datetime
from typing import Optional
from utils import (
    Task,
    OperationResult,
    Priority,
    load_tasks,
    save_tasks,
    get_next_id,
    validate_title,
    validate_category,
    validate_due_date,
    StorageError,
    ERROR_CODES
)


def add_task(
    title: str,
    priority: str = "medium",
    category: str = "general",
    due_date: Optional[str] = None
) -> OperationResult:
    """
    Add a new task to the system.

    Args:
        title: Task description (1-200 chars)
        priority: Priority level (high/medium/low), default medium
        category: Task category, default general
        due_date: Optional due date (ISO 8601)

    Returns:
        OperationResult with success status and task data
    """
    try:
        # Validation phase
        validated_title = validate_title(title)
        priority_enum = Priority.from_string(priority)
        validated_category = validate_category(category)

        # Validate due_date if provided
        if due_date:
            due_date = validate_due_date(due_date)

        # Task creation phase
        task_id = get_next_id()
        task = Task(
            id=task_id,
            title=validated_title,
            priority=priority_enum,
            category=validated_category,
            due_date=due_date
        )

        # Persistence phase
        tasks = load_tasks()
        tasks.append(task.to_dict())
        save_tasks(tasks)

        # Success response
        return OperationResult.success_result(
            message=f"Task #{task.id} added successfully",
            data=task.to_dict()
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
