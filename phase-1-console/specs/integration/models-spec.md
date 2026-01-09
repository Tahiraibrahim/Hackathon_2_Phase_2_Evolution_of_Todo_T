# Data Models and Type Definitions Specification

## Overview
Shared type definitions, data models, and constants used across the application to ensure type safety and consistency.

## Purpose
Provide centralized type definitions using Python 3.12+ type hints, dataclasses, and enums to improve code quality, IDE support, and maintainability.

## File Location
`utils/models.py`

---

## Enumerations

### 1. Priority Enum

```python
from enum import Enum

class Priority(str, Enum):
    """Task priority levels."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

    @classmethod
    def default(cls) -> "Priority":
        """Return default priority."""
        return cls.MEDIUM

    @classmethod
    def from_string(cls, value: str) -> "Priority":
        """Parse priority from string (case-insensitive)."""
        try:
            return cls(value.lower())
        except ValueError:
            raise ValueError(
                f"Invalid priority: {value}. Must be one of: "
                f"{', '.join([p.value for p in cls])}"
            )
```

#### Usage
```python
priority = Priority.HIGH
priority_str = priority.value  # "high"

# Parse from user input
user_input = "HIGH"
priority = Priority.from_string(user_input)  # Priority.HIGH
```

---

### 2. Status Enum

```python
class Status(str, Enum):
    """Task status values."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

    @classmethod
    def default(cls) -> "Status":
        """Return default status."""
        return cls.PENDING

    @classmethod
    def from_string(cls, value: str) -> "Status":
        """Parse status from string (case-insensitive)."""
        try:
            return cls(value.lower())
        except ValueError:
            raise ValueError(
                f"Invalid status: {value}. Must be one of: "
                f"{', '.join([s.value for s in cls])}"
            )
```

---

### 3. OutputFormat Enum

```python
class OutputFormat(str, Enum):
    """Output format options for list command."""
    TABLE = "table"
    JSON = "json"
    SIMPLE = "simple"

    @classmethod
    def default(cls) -> "OutputFormat":
        """Return default format."""
        return cls.TABLE
```

---

### 4. SortOrder Enum

```python
class SortOrder(str, Enum):
    """Sort order directions."""
    ASC = "asc"
    DESC = "desc"

    @classmethod
    def default(cls) -> "SortOrder":
        """Return default sort order."""
        return cls.ASC
```

---

## Data Classes

### 1. Task Dataclass

```python
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional

@dataclass
class Task:
    """
    Represents a todo task.

    Attributes:
        id: Unique task identifier
        title: Task description (1-200 characters)
        priority: Task priority level
        category: Task category/grouping
        status: Current task status
        completed: Whether task is completed
        created_at: Creation timestamp (ISO 8601)
        updated_at: Last modification timestamp (ISO 8601)
        completed_at: Completion timestamp (ISO 8601)
        due_date: Optional due date (ISO 8601)
    """
    id: int
    title: str
    priority: Priority = Priority.MEDIUM
    category: str = "general"
    status: Status = Status.PENDING
    completed: bool = False
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    updated_at: Optional[str] = None
    completed_at: Optional[str] = None
    due_date: Optional[str] = None

    def __post_init__(self):
        """Validate and normalize fields after initialization."""
        # Convert enum strings to Enum instances if needed
        if isinstance(self.priority, str):
            self.priority = Priority.from_string(self.priority)
        if isinstance(self.status, str):
            self.status = Status.from_string(self.status)

        # Validate title
        self.title = self.title.strip()
        if not self.title:
            raise ValueError("Title cannot be empty")
        if len(self.title) > 200:
            raise ValueError("Title cannot exceed 200 characters")

        # Validate category
        if len(self.category) > 50:
            raise ValueError("Category cannot exceed 50 characters")

    def to_dict(self) -> dict:
        """
        Convert task to dictionary with string values.

        Returns:
            Dictionary representation suitable for JSON serialization.
        """
        data = asdict(self)
        # Convert enums to strings
        data['priority'] = self.priority.value
        data['status'] = self.status.value
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """
        Create Task instance from dictionary.

        Args:
            data: Dictionary with task data.

        Returns:
            Task instance.
        """
        return cls(**data)

    def mark_completed(self) -> None:
        """Mark task as completed with timestamp."""
        self.completed = True
        self.status = Status.COMPLETED
        self.completed_at = datetime.utcnow().isoformat() + "Z"
        self.updated_at = self.completed_at

    def mark_incomplete(self) -> None:
        """Mark task as incomplete."""
        self.completed = False
        self.status = Status.PENDING
        self.completed_at = None
        self.updated_at = datetime.utcnow().isoformat() + "Z"

    def update_fields(self, **kwargs) -> None:
        """
        Update task fields and set updated_at timestamp.

        Args:
            **kwargs: Fields to update.
        """
        for key, value in kwargs.items():
            if hasattr(self, key) and value is not None:
                setattr(self, key, value)
        self.updated_at = datetime.utcnow().isoformat() + "Z"

    def is_overdue(self) -> bool:
        """
        Check if task is overdue.

        Returns:
            True if task has due_date in the past and is not completed.
        """
        if not self.due_date or self.completed:
            return False
        try:
            due = datetime.fromisoformat(self.due_date.replace('Z', '+00:00'))
            return datetime.now(due.tzinfo) > due
        except (ValueError, AttributeError):
            return False

    def days_until_due(self) -> Optional[int]:
        """
        Calculate days until due date.

        Returns:
            Number of days (negative if overdue), None if no due date.
        """
        if not self.due_date:
            return None
        try:
            due = datetime.fromisoformat(self.due_date.replace('Z', '+00:00'))
            now = datetime.now(due.tzinfo)
            delta = (due - now).days
            return delta
        except (ValueError, AttributeError):
            return None
```

---

### 2. TaskFilter Dataclass

```python
@dataclass
class TaskFilter:
    """
    Encapsulates filter criteria for task queries.

    Attributes:
        status: Filter by status (None for all)
        priority: Filter by priority (None for all)
        category: Filter by category (None for all)
        completed: Filter by completion status (None for all)
        overdue_only: Show only overdue tasks
    """
    status: Optional[Status] = None
    priority: Optional[Priority] = None
    category: Optional[str] = None
    completed: Optional[bool] = None
    overdue_only: bool = False

    def matches(self, task: Task) -> bool:
        """
        Check if task matches filter criteria.

        Args:
            task: Task to check.

        Returns:
            True if task matches all filter criteria.
        """
        if self.status and task.status != self.status:
            return False
        if self.priority and task.priority != self.priority:
            return False
        if self.category and task.category != self.category:
            return False
        if self.completed is not None and task.completed != self.completed:
            return False
        if self.overdue_only and not task.is_overdue():
            return False
        return True
```

---

### 3. OperationResult Dataclass

```python
@dataclass
class OperationResult:
    """
    Standardized result for skill operations.

    Attributes:
        success: Whether operation succeeded
        message: Human-readable message
        data: Operation-specific data (task, tasks list, etc.)
        error: Error message if failed
        error_code: Machine-readable error code
    """
    success: bool
    message: str
    data: Optional[Any] = None
    error: Optional[str] = None
    error_code: Optional[str] = None

    @classmethod
    def success_result(cls, message: str, data: Any = None) -> "OperationResult":
        """Create success result."""
        return cls(success=True, message=message, data=data)

    @classmethod
    def error_result(cls, error: str, code: str = "ERROR") -> "OperationResult":
        """Create error result."""
        return cls(
            success=False,
            message=f"Operation failed: {error}",
            error=error,
            error_code=code
        )

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return asdict(self)
```

---

## Type Aliases

```python
from typing import List, Dict, Any, Optional, Callable

# Task-related types
TaskDict = Dict[str, Any]
TaskList = List[Task]
TaskId = int

# Filter types
FilterFunc = Callable[[Task], bool]
SortFunc = Callable[[Task], Any]

# Result types
TaskResult = OperationResult
TaskListResult = OperationResult
```

---

## Constants

```python
# Default values
DEFAULT_PRIORITY = Priority.MEDIUM
DEFAULT_CATEGORY = "general"
DEFAULT_STATUS = Status.PENDING

# Validation limits
MIN_TITLE_LENGTH = 1
MAX_TITLE_LENGTH = 200
MAX_CATEGORY_LENGTH = 50

# Date formats
ISO_DATE_FORMAT = "%Y-%m-%d"
ISO_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
DISPLAY_DATE_FORMAT = "%b %d, %Y"
DISPLAY_DATETIME_FORMAT = "%b %d, %Y at %I:%M %p"

# Color mappings for rich
PRIORITY_COLORS = {
    Priority.HIGH: "red",
    Priority.MEDIUM: "yellow",
    Priority.LOW: "green",
}

STATUS_COLORS = {
    Status.PENDING: "white",
    Status.IN_PROGRESS: "blue",
    Status.COMPLETED: "green",
}

STATUS_ICONS = {
    Status.PENDING: "○",
    Status.IN_PROGRESS: "◐",
    Status.COMPLETED: "✓",
}

# Error codes
ERROR_CODES = {
    "NOT_FOUND": "TASK_NOT_FOUND",
    "VALIDATION_ERROR": "VALIDATION_ERROR",
    "STORAGE_ERROR": "STORAGE_ERROR",
    "INVALID_INPUT": "INVALID_INPUT",
    "NO_CHANGES": "NO_CHANGES_PROVIDED",
}
```

---

## Validation Functions

```python
def validate_title(title: str) -> str:
    """
    Validate and normalize task title.

    Args:
        title: Raw title string.

    Returns:
        Normalized title.

    Raises:
        ValueError: If title is invalid.
    """
    title = title.strip()
    if not title:
        raise ValueError("Title cannot be empty")
    if len(title) > MAX_TITLE_LENGTH:
        raise ValueError(f"Title cannot exceed {MAX_TITLE_LENGTH} characters")
    return title


def validate_category(category: str) -> str:
    """
    Validate and normalize category.

    Args:
        category: Raw category string.

    Returns:
        Normalized category.

    Raises:
        ValueError: If category is invalid.
    """
    category = category.strip()
    if len(category) > MAX_CATEGORY_LENGTH:
        raise ValueError(f"Category cannot exceed {MAX_CATEGORY_LENGTH} characters")
    return category or DEFAULT_CATEGORY


def validate_due_date(due_date: str) -> str:
    """
    Validate due date format.

    Args:
        due_date: ISO 8601 date string.

    Returns:
        Validated date string.

    Raises:
        ValueError: If date format is invalid.
    """
    try:
        # Parse and reformat to ensure consistency
        dt = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
        return dt.isoformat() + "Z"
    except (ValueError, AttributeError) as e:
        raise ValueError(f"Invalid date format: {due_date}. Use YYYY-MM-DD or ISO 8601.")
```

---

## Utility Functions

```python
def format_priority(priority: Priority) -> str:
    """Format priority with color for rich output."""
    color = PRIORITY_COLORS[priority]
    return f"[{color}]{priority.value}[/{color}]"


def format_status(status: Status) -> str:
    """Format status with icon for rich output."""
    icon = STATUS_ICONS[status]
    color = STATUS_COLORS[status]
    return f"[{color}]{icon} {status.value}[/{color}]"


def format_date_display(iso_date: Optional[str]) -> str:
    """Format ISO date for human-readable display."""
    if not iso_date:
        return "-"
    try:
        dt = datetime.fromisoformat(iso_date.replace('Z', '+00:00'))
        return dt.strftime(DISPLAY_DATE_FORMAT)
    except (ValueError, AttributeError):
        return iso_date


def format_datetime_display(iso_datetime: Optional[str]) -> str:
    """Format ISO datetime for human-readable display."""
    if not iso_datetime:
        return "-"
    try:
        dt = datetime.fromisoformat(iso_datetime.replace('Z', '+00:00'))
        return dt.strftime(DISPLAY_DATETIME_FORMAT)
    except (ValueError, AttributeError):
        return iso_datetime
```

---

## Integration with Skills

### Import Pattern
```python
# In skills/*.py
from utils.models import (
    Task,
    TaskFilter,
    OperationResult,
    Priority,
    Status,
    validate_title,
    validate_category,
    ERROR_CODES
)
```

### Usage Example in Add Skill
```python
def add_task(
    title: str,
    priority: str = "medium",
    category: str = "general"
) -> OperationResult:
    """Add a new task."""
    try:
        # Validate and create task
        validated_title = validate_title(title)
        priority_enum = Priority.from_string(priority)

        task = Task(
            id=get_next_id(),
            title=validated_title,
            priority=priority_enum,
            category=validate_category(category)
        )

        # Save to storage
        tasks = load_tasks()
        tasks.append(task.to_dict())
        save_tasks(tasks)

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
```

---

## Testing Support

### Factory Functions
```python
def create_test_task(
    id: int = 1,
    title: str = "Test Task",
    **kwargs
) -> Task:
    """Create task for testing."""
    return Task(id=id, title=title, **kwargs)


def create_sample_tasks() -> List[Task]:
    """Create sample tasks for testing."""
    return [
        Task(1, "Buy groceries", Priority.HIGH, "shopping"),
        Task(2, "Submit report", Priority.MEDIUM, "work"),
        Task(3, "Call dentist", Priority.LOW, "health"),
    ]
```

---

## File Structure

```
utils/
├── __init__.py          # Export public API
├── models.py            # This specification
└── storage.py           # Storage functions
```

### `utils/__init__.py`
```python
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
    ERROR_CODES,
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
    # Storage
    "load_tasks",
    "save_tasks",
    "get_next_id",
    "find_task_by_id",
    "update_task",
    "delete_task",
    "backup_tasks",
    "StorageError",
    # Constants
    "ERROR_CODES",
]
```

---

## Acceptance Criteria

- [ ] All classes have type hints
- [ ] All enums have from_string() class methods
- [ ] Task dataclass has validation in __post_init__
- [ ] Task has to_dict() and from_dict() methods
- [ ] OperationResult standardizes all skill returns
- [ ] Constants defined for colors, formats, limits
- [ ] Validation functions raise clear ValueErrors
- [ ] Format functions return rich-compatible strings
- [ ] Full docstrings for all public APIs
- [ ] Factory functions for testing
- [ ] Clean __init__.py exports public API
- [ ] No circular imports
