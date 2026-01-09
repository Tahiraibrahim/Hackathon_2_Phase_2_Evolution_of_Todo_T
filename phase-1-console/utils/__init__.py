"""Utility modules for Todo App."""

from .models import (
    Task,
    TaskFilter,
    OperationResult,
    Priority,
    Status,
    OutputFormat,
    SortOrder,
    validate_title,
    validate_category,
    validate_due_date,
    format_priority,
    format_status,
    format_date_display,
    format_datetime_display,
    ERROR_CODES,
    PRIORITY_COLORS,
    STATUS_COLORS,
    STATUS_ICONS,
    DEFAULT_PRIORITY,
    DEFAULT_CATEGORY,
    DEFAULT_STATUS,
)

from .storage import (
    load_tasks,
    save_tasks,
    get_next_id,
    find_task_by_id,
    update_task,
    delete_task,
    backup_tasks,
    StorageError,
)

__all__ = [
    # Models
    "Task",
    "TaskFilter",
    "OperationResult",
    "Priority",
    "Status",
    "OutputFormat",
    "SortOrder",
    # Validation
    "validate_title",
    "validate_category",
    "validate_due_date",
    # Formatting
    "format_priority",
    "format_status",
    "format_date_display",
    "format_datetime_display",
    # Constants
    "ERROR_CODES",
    "PRIORITY_COLORS",
    "STATUS_COLORS",
    "STATUS_ICONS",
    "DEFAULT_PRIORITY",
    "DEFAULT_CATEGORY",
    "DEFAULT_STATUS",
    # Storage
    "load_tasks",
    "save_tasks",
    "get_next_id",
    "find_task_by_id",
    "update_task",
    "delete_task",
    "backup_tasks",
    "StorageError",
]
