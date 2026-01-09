"""
List Tasks Skill

Capability to display todos in a formatted table with filtering and sorting options.
"""

from typing import Optional, List
from rich.table import Table
from rich.console import Console
from utils import (
    Task,
    TaskFilter,
    OperationResult,
    Priority,
    Status,
    load_tasks,
    format_priority,
    format_status,
    format_date_display,
    StorageError,
    ERROR_CODES
)


def list_tasks(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    category: Optional[str] = None,
    completed: Optional[bool] = None,
    overdue_only: bool = False,
    sort_by: str = "id",
    sort_order: str = "asc",
    limit: Optional[int] = None,
    output_format: str = "table"
) -> OperationResult:
    """
    List tasks with optional filters and sorting.

    Args:
        status: Filter by status (pending/in_progress/completed)
        priority: Filter by priority (high/medium/low)
        category: Filter by category
        completed: Filter by completion status
        overdue_only: Show only overdue tasks
        sort_by: Sort field (id/title/priority/created_at/due_date)
        sort_order: Sort order (asc/desc)
        limit: Maximum number of results
        output_format: Output format (table/json/simple)

    Returns:
        OperationResult with task list
    """
    try:
        # Load tasks
        task_dicts = load_tasks()
        tasks = [Task.from_dict(t) for t in task_dicts]

        # Build filter
        filter_status = Status.from_string(status) if status and status != "all" else None
        filter_priority = Priority.from_string(priority) if priority and priority != "all" else None

        task_filter = TaskFilter(
            status=filter_status,
            priority=filter_priority,
            category=category if category and category != "all" else None,
            completed=completed,
            overdue_only=overdue_only
        )

        # Apply filter
        filtered_tasks = [t for t in tasks if task_filter.matches(t)]

        # Sort tasks
        reverse = (sort_order == "desc")
        try:
            filtered_tasks.sort(
                key=lambda t: getattr(t, sort_by) if getattr(t, sort_by) is not None else "",
                reverse=reverse
            )
        except AttributeError:
            pass  # Invalid sort field, skip sorting

        # Apply limit
        if limit and limit > 0:
            filtered_tasks = filtered_tasks[:limit]

        # Format output
        if output_format == "json":
            return OperationResult.success_result(
                message=f"Showing {len(filtered_tasks)} tasks",
                data=[t.to_dict() for t in filtered_tasks]
            )
        elif output_format == "simple":
            lines = []
            for t in filtered_tasks:
                status_mark = "✓" if t.completed else "○"
                due_info = f" - Due: {t.due_date}" if t.due_date else ""
                lines.append(f"{t.id}. [{status_mark}] {t.title} ({t.priority.value}){due_info}")
            return OperationResult.success_result(
                message=f"Showing {len(filtered_tasks)} tasks",
                data="\n".join(lines) if lines else "No tasks found."
            )
        else:  # table format
            return OperationResult.success_result(
                message=f"Showing {len(filtered_tasks)} tasks",
                data={"tasks": filtered_tasks, "format": "table"}
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
