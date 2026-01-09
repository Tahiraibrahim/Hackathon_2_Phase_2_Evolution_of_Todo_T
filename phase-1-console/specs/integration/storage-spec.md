# Storage Layer Specification

## Overview
Shared storage utility module (`utils/storage.py`) that provides atomic, reliable file I/O operations for the `todos.json` data store.

## Purpose
Centralize all file system operations to ensure data integrity, prevent corruption, and provide consistent error handling across all skills.

## File Location
`utils/storage.py`

---

## Core Functions

### 1. `load_tasks() -> List[Dict[str, Any]]`

#### Purpose
Load all tasks from `todos.json` file.

#### Inputs
None

#### Returns
- **Type**: `List[Dict[str, Any]]`
- **Description**: List of task dictionaries
- **Empty case**: Returns `[]` if file doesn't exist or is empty

#### Processing Logic
1. Check if `todos.json` exists
2. If not, return empty list `[]`
3. Read file contents
4. Parse JSON
5. Validate structure (must be array)
6. Return task list

#### Error Handling
```python
try:
    # Read and parse JSON
except FileNotFoundError:
    return []
except json.JSONDecodeError as e:
    raise StorageError(f"Corrupted todos.json: {e}")
except PermissionError:
    raise StorageError("Permission denied reading todos.json")
```

#### Example Output
```python
[
    {
        "id": 1,
        "title": "Buy groceries",
        "priority": "high",
        "category": "shopping",
        "status": "pending",
        "completed": false,
        "created_at": "2025-12-25T10:30:00Z",
        "due_date": null
    }
]
```

---

### 2. `save_tasks(tasks: List[Dict[str, Any]]) -> bool`

#### Purpose
Save tasks to `todos.json` using atomic write operation.

#### Inputs
- **tasks** (`List[Dict[str, Any]]`): Complete list of tasks to save

#### Returns
- **Type**: `bool`
- **Value**: `True` on success, raises exception on failure

#### Processing Logic
1. Validate input is a list
2. Create temp file: `todos.json.tmp`
3. Write JSON to temp file with indentation (pretty print)
4. Flush to disk
5. Atomic rename: `todos.json.tmp` → `todos.json`
6. Return `True`

#### Atomic Write Strategy
```python
temp_file = "todos.json.tmp"
with open(temp_file, 'w') as f:
    json.dump(tasks, f, indent=2, ensure_ascii=False)
    f.flush()
    os.fsync(f.fileno())  # Force write to disk

os.replace(temp_file, "todos.json")  # Atomic on POSIX
```

#### Error Handling
```python
try:
    # Atomic write
except PermissionError:
    raise StorageError("Permission denied writing todos.json")
except OSError as e:
    raise StorageError(f"Disk error: {e}")
finally:
    # Clean up temp file if exists
    if os.path.exists(temp_file):
        os.remove(temp_file)
```

---

### 3. `get_next_id() -> int`

#### Purpose
Generate the next available task ID.

#### Inputs
None

#### Returns
- **Type**: `int`
- **Value**: Next ID (max current ID + 1, or 1 if no tasks)

#### Processing Logic
1. Load all tasks
2. If empty, return `1`
3. Find maximum ID: `max(task['id'] for task in tasks)`
4. Return `max_id + 1`

#### Example
```python
tasks = [{"id": 1}, {"id": 3}, {"id": 5}]
next_id = get_next_id()  # Returns 6
```

---

### 4. `backup_tasks() -> str`

#### Purpose
Create a timestamped backup of `todos.json`.

#### Inputs
None

#### Returns
- **Type**: `str`
- **Value**: Path to backup file

#### Processing Logic
1. Check if `todos.json` exists
2. If not, return empty string (nothing to back up)
3. Generate timestamp: `YYYYMMDD-HHMMSS`
4. Create backup filename: `todos.backup.YYYYMMDD-HHMMSS.json`
5. Copy file to backup location
6. Return backup path

#### Example
```python
backup_path = backup_tasks()
# Returns: "todos.backup.20251225-153045.json"
```

#### Error Handling
```python
try:
    # Copy file
except Exception as e:
    # Log warning but don't fail operation
    print(f"Warning: Could not create backup: {e}")
    return ""
```

---

### 5. `find_task_by_id(task_id: int) -> Optional[Dict[str, Any]]`

#### Purpose
Retrieve a single task by ID.

#### Inputs
- **task_id** (`int`): The task ID to find

#### Returns
- **Type**: `Optional[Dict[str, Any]]`
- **Value**: Task dictionary if found, `None` if not found

#### Processing Logic
1. Load all tasks
2. Search for task with matching ID
3. Return task or `None`

#### Example
```python
task = find_task_by_id(5)
if task:
    print(task['title'])
else:
    print("Task not found")
```

---

### 6. `update_task(task_id: int, updates: Dict[str, Any]) -> bool`

#### Purpose
Update specific fields of a task.

#### Inputs
- **task_id** (`int`): ID of task to update
- **updates** (`Dict[str, Any]`): Fields to update

#### Returns
- **Type**: `bool`
- **Value**: `True` if updated, `False` if task not found

#### Processing Logic
1. Load all tasks
2. Find task with matching ID
3. If not found, return `False`
4. Update specified fields (preserve others)
5. Set `updated_at` timestamp
6. Save tasks
7. Return `True`

#### Example
```python
success = update_task(5, {
    "priority": "high",
    "status": "in_progress"
})
```

---

### 7. `delete_task(task_id: int) -> bool`

#### Purpose
Remove a task by ID.

#### Inputs
- **task_id** (`int`): ID of task to delete

#### Returns
- **Type**: `bool`
- **Value**: `True` if deleted, `False` if task not found

#### Processing Logic
1. Load all tasks
2. Filter out task with matching ID
3. If list unchanged, return `False`
4. Save filtered list
5. Return `True`

#### Example
```python
deleted = delete_task(5)
if deleted:
    print("Task deleted")
else:
    print("Task not found")
```

---

## Custom Exceptions

### `StorageError`
Base exception for all storage-related errors.

```python
class StorageError(Exception):
    """Raised when storage operations fail."""
    pass
```

#### Usage
```python
try:
    tasks = load_tasks()
except StorageError as e:
    print(f"Storage error: {e}")
    sys.exit(1)
```

---

## Data File Schema

### File: `todos.json`

#### Structure
```json
[
  {
    "id": 1,
    "title": "Task title",
    "priority": "medium",
    "category": "general",
    "status": "pending",
    "completed": false,
    "created_at": "2025-12-25T10:30:00Z",
    "updated_at": "2025-12-25T10:30:00Z",
    "completed_at": null,
    "due_date": null
  }
]
```

#### Field Specifications

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | int | Yes | Unique task identifier (auto-increment) |
| `title` | str | Yes | Task description (1-200 chars) |
| `priority` | enum | Yes | One of: `high`, `medium`, `low` |
| `category` | str | Yes | Category name (default: `general`) |
| `status` | enum | Yes | One of: `pending`, `in_progress`, `completed` |
| `completed` | bool | Yes | Completion flag |
| `created_at` | str | Yes | ISO 8601 timestamp |
| `updated_at` | str | No | ISO 8601 timestamp (set on modifications) |
| `completed_at` | str/null | No | ISO 8601 timestamp when completed |
| `due_date` | str/null | No | ISO 8601 date/datetime |

---

## File System Layout

```
phase-1-console/
├── todos.json                           # Main data file
├── todos.backup.YYYYMMDD-HHMMSS.json   # Timestamped backups
├── utils/
│   ├── __init__.py                      # Empty or re-exports
│   └── storage.py                       # This specification
└── skills/
    └── *.py                             # Skills import from utils.storage
```

---

## Constants

```python
TODOS_FILE = "todos.json"
BACKUP_PREFIX = "todos.backup"
DEFAULT_PRIORITY = "medium"
DEFAULT_CATEGORY = "general"
DEFAULT_STATUS = "pending"
```

---

## Type Definitions

```python
from typing import List, Dict, Any, Optional
from datetime import datetime

TaskDict = Dict[str, Any]  # Type alias for task dictionaries
TaskList = List[TaskDict]  # Type alias for list of tasks
```

---

## Integration with Skills

### Import Pattern
```python
# In skills/add_skill.py
from utils.storage import (
    load_tasks,
    save_tasks,
    get_next_id,
    StorageError
)
```

### Usage Example
```python
def add_task(title: str, priority: str = "medium") -> Dict[str, Any]:
    try:
        tasks = load_tasks()
        new_task = {
            "id": get_next_id(),
            "title": title,
            "priority": priority,
            # ... other fields
        }
        tasks.append(new_task)
        save_tasks(tasks)
        return {"success": True, "task": new_task}
    except StorageError as e:
        return {"success": False, "error": str(e)}
```

---

## Performance Considerations

### File Locking
- Not required for Phase 1 (single-user CLI)
- Consider `fcntl.flock()` for Phase 2+ (concurrent access)

### Optimization
- Keep file size reasonable (< 10MB recommended)
- Consider pagination for large task lists
- Use in-memory caching if performance issues arise

### Scalability Limits
- Current design supports ~10,000 tasks efficiently
- For larger datasets, consider SQLite migration

---

## Testing Requirements

### Unit Tests (`tests/test_storage.py`)

1. **test_load_tasks_empty**: Returns `[]` when file missing
2. **test_load_tasks_valid**: Loads valid JSON correctly
3. **test_load_tasks_corrupted**: Raises `StorageError` on bad JSON
4. **test_save_tasks_atomic**: Verifies atomic write behavior
5. **test_get_next_id**: Returns correct next ID
6. **test_backup_tasks**: Creates timestamped backup
7. **test_find_task_by_id**: Finds existing task
8. **test_update_task**: Updates fields correctly
9. **test_delete_task**: Removes task by ID

### Integration Tests

1. **test_concurrent_writes**: Verify atomic writes prevent corruption
2. **test_backup_restore**: Backup and restore workflow
3. **test_error_recovery**: Handles disk full, permissions errors

---

## Acceptance Criteria

- [ ] All functions have type hints
- [ ] All functions have comprehensive docstrings
- [ ] Atomic writes prevent data corruption
- [ ] Missing file handled gracefully (returns empty list)
- [ ] Corrupted JSON raises clear error
- [ ] All errors wrapped in `StorageError`
- [ ] Backup creates timestamped files
- [ ] Next ID calculation handles gaps correctly
- [ ] Unit tests achieve 100% coverage
- [ ] No external dependencies (stdlib only)
