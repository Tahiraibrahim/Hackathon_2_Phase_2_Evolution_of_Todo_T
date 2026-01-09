# Phase 1 Console Todo App - Implementation Plan

## Plan Overview

**Goal:** Implement a fully functional console-based todo application following specification-driven development principles.

**Approach:** Bottom-up implementation starting with foundational layers (utilities) and building up to user-facing layers (CLI).

**Estimated Components:**
- 2 utility modules (models, storage)
- 6 skill implementations
- 1 CLI interface
- Test suite for each component

---

## Implementation Phases

### Phase 1: Foundation Layer (Utils)
Build the core utilities that all other components depend on.

### Phase 2: Skill Layer
Implement business logic for each feature following specifications.

### Phase 3: Integration Layer (CLI)
Create the user-facing CLI that ties everything together.

### Phase 4: Testing & Validation
Comprehensive testing and acceptance criteria verification.

---

## Phase 1: Foundation Layer

### Step 1.1: Implement `utils/models.py`

**Priority:** CRITICAL (no dependencies, required by all other components)

**Specification:** `specs/integration/models-spec.md`

**Tasks:**

#### 1.1.1: Create Basic Structure
- [ ] Create `utils/` directory
- [ ] Create empty `utils/__init__.py`
- [ ] Create `utils/models.py` file
- [ ] Add file docstring and imports

**Imports needed:**
```python
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import List, Dict, Any, Optional, Callable
```

#### 1.1.2: Implement Enumerations
- [ ] Implement `Priority` enum with HIGH, MEDIUM, LOW
  - [ ] Add `default()` classmethod
  - [ ] Add `from_string()` classmethod with validation
- [ ] Implement `Status` enum with PENDING, IN_PROGRESS, COMPLETED
  - [ ] Add `default()` classmethod
  - [ ] Add `from_string()` classmethod with validation
- [ ] Implement `OutputFormat` enum with TABLE, JSON, SIMPLE
  - [ ] Add `default()` classmethod
- [ ] Implement `SortOrder` enum with ASC, DESC
  - [ ] Add `default()` classmethod

**Acceptance:**
- All enums are str subclasses
- from_string() handles case-insensitive input
- from_string() raises ValueError with helpful message for invalid input

#### 1.1.3: Implement Task Dataclass
- [ ] Define `Task` dataclass with all fields per spec
  - [ ] id: int
  - [ ] title: str
  - [ ] priority: Priority (default MEDIUM)
  - [ ] category: str (default "general")
  - [ ] status: Status (default PENDING)
  - [ ] completed: bool (default False)
  - [ ] created_at: str (auto-generated ISO 8601)
  - [ ] updated_at: Optional[str] (default None)
  - [ ] completed_at: Optional[str] (default None)
  - [ ] due_date: Optional[str] (default None)

- [ ] Implement `__post_init__()` for validation
  - [ ] Convert string enums to Enum instances
  - [ ] Validate title (strip, not empty, max 200 chars)
  - [ ] Validate category (max 50 chars)

- [ ] Implement `to_dict()` method
  - [ ] Convert enums to string values
  - [ ] Return dict suitable for JSON serialization

- [ ] Implement `from_dict()` classmethod
  - [ ] Create Task instance from dictionary

- [ ] Implement helper methods
  - [ ] `mark_completed()` - Set completed=True, status=COMPLETED, add timestamp
  - [ ] `mark_incomplete()` - Set completed=False, status=PENDING, clear timestamp
  - [ ] `update_fields(**kwargs)` - Update fields and set updated_at
  - [ ] `is_overdue()` - Check if due_date is past and not completed
  - [ ] `days_until_due()` - Calculate days until/past due date

**Acceptance:**
- Validation in __post_init__ raises ValueError for invalid data
- to_dict() returns JSON-serializable dict
- from_dict() creates valid Task instances
- Helper methods work correctly with timestamps

#### 1.1.4: Implement Supporting Dataclasses
- [ ] Implement `TaskFilter` dataclass
  - [ ] Fields: status, priority, category, completed, overdue_only
  - [ ] Implement `matches(task: Task) -> bool` method

- [ ] Implement `OperationResult` dataclass
  - [ ] Fields: success, message, data, error, error_code
  - [ ] Implement `success_result()` classmethod
  - [ ] Implement `error_result()` classmethod
  - [ ] Implement `to_dict()` method

**Acceptance:**
- TaskFilter.matches() correctly filters tasks
- OperationResult provides consistent response format

#### 1.1.5: Implement Constants
- [ ] Define default values (DEFAULT_PRIORITY, DEFAULT_CATEGORY, etc.)
- [ ] Define validation limits (MIN_TITLE_LENGTH, MAX_TITLE_LENGTH, etc.)
- [ ] Define date formats (ISO_DATE_FORMAT, DISPLAY_DATE_FORMAT, etc.)
- [ ] Define color mappings (PRIORITY_COLORS, STATUS_COLORS, STATUS_ICONS)
- [ ] Define error codes (ERROR_CODES dict)

#### 1.1.6: Implement Validation Functions
- [ ] `validate_title(title: str) -> str`
  - [ ] Strip whitespace
  - [ ] Check not empty
  - [ ] Check max length
  - [ ] Raise ValueError with clear message

- [ ] `validate_category(category: str) -> str`
  - [ ] Strip whitespace
  - [ ] Check max length
  - [ ] Return default if empty

- [ ] `validate_due_date(due_date: str) -> str`
  - [ ] Parse ISO 8601 format
  - [ ] Reformat for consistency
  - [ ] Raise ValueError for invalid format

**Acceptance:**
- All validation functions raise ValueError with helpful messages
- Functions normalize input (strip, defaults)

#### 1.1.7: Implement Formatting Functions
- [ ] `format_priority(priority: Priority) -> str`
  - [ ] Return rich-formatted string with color

- [ ] `format_status(status: Status) -> str`
  - [ ] Return rich-formatted string with icon and color

- [ ] `format_date_display(iso_date: Optional[str]) -> str`
  - [ ] Convert ISO to human-readable format
  - [ ] Return "-" for None

- [ ] `format_datetime_display(iso_datetime: Optional[str]) -> str`
  - [ ] Convert ISO to human-readable datetime
  - [ ] Return "-" for None

**Acceptance:**
- Formatting functions return rich-compatible markup strings
- Functions handle None values gracefully

#### 1.1.8: Write Unit Tests
- [ ] Create `tests/test_models.py`
- [ ] Test all enum from_string() methods
- [ ] Test Task validation in __post_init__
- [ ] Test Task serialization (to_dict/from_dict)
- [ ] Test Task helper methods
- [ ] Test TaskFilter.matches()
- [ ] Test OperationResult factory methods
- [ ] Test all validation functions
- [ ] Test all formatting functions

**Acceptance:**
- 100% code coverage for models.py
- All tests pass

**Estimated Time:** 4-6 hours
**Dependencies:** None

---

### Step 1.2: Implement `utils/storage.py`

**Priority:** CRITICAL (required by all skills)

**Specification:** `specs/integration/storage-spec.md`

**Dependencies:** `utils/models.py` (for type hints only)

**Tasks:**

#### 1.2.1: Create Basic Structure
- [ ] Create `utils/storage.py` file
- [ ] Add file docstring
- [ ] Add imports

**Imports needed:**
```python
import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
```

#### 1.2.2: Define Custom Exception
- [ ] Create `StorageError` exception class
  - [ ] Inherit from Exception
  - [ ] Add docstring

#### 1.2.3: Define Constants
- [ ] `TODOS_FILE = "todos.json"`
- [ ] `BACKUP_PREFIX = "todos.backup"`
- [ ] `DEFAULT_PRIORITY = "medium"`
- [ ] `DEFAULT_CATEGORY = "general"`
- [ ] `DEFAULT_STATUS = "pending"`

#### 1.2.4: Implement `load_tasks()` Function
- [ ] Add function signature with type hints
- [ ] Add comprehensive docstring (Google style)
- [ ] Implement try-except block
  - [ ] Check if file exists
  - [ ] Return [] if FileNotFoundError
  - [ ] Read file contents
  - [ ] Parse JSON
  - [ ] Validate it's a list
  - [ ] Catch json.JSONDecodeError → raise StorageError
  - [ ] Catch PermissionError → raise StorageError
- [ ] Return task list

**Acceptance:**
- Returns [] if file doesn't exist (no error)
- Raises StorageError with clear message for corrupted JSON
- Raises StorageError for permission issues
- Returns list of task dicts for valid file

#### 1.2.5: Implement `save_tasks()` Function
- [ ] Add function signature with type hints
- [ ] Add comprehensive docstring
- [ ] Validate input is a list
- [ ] Implement atomic write strategy
  - [ ] Create temp file path: "todos.json.tmp"
  - [ ] Open temp file for writing
  - [ ] Write JSON with indent=2, ensure_ascii=False
  - [ ] Flush buffer: f.flush()
  - [ ] Force disk sync: os.fsync(f.fileno())
  - [ ] Close file
  - [ ] Atomic rename: os.replace(temp, target)
- [ ] Implement try-except-finally
  - [ ] Catch PermissionError → raise StorageError
  - [ ] Catch OSError → raise StorageError
  - [ ] Finally: clean up temp file if exists
- [ ] Return True on success

**Acceptance:**
- Writes are atomic (temp file + rename)
- File is synced to disk before rename
- Temp file is cleaned up even on failure
- Raises StorageError with clear messages

#### 1.2.6: Implement `get_next_id()` Function
- [ ] Add function signature with type hints
- [ ] Add comprehensive docstring
- [ ] Call load_tasks()
- [ ] If empty list, return 1
- [ ] Find max ID: max(task['id'] for task in tasks)
- [ ] Return max_id + 1
- [ ] Handle potential errors

**Acceptance:**
- Returns 1 for empty task list
- Returns max_id + 1 for existing tasks
- Handles gaps in ID sequence correctly

#### 1.2.7: Implement `backup_tasks()` Function
- [ ] Add function signature with type hints
- [ ] Add comprehensive docstring
- [ ] Check if todos.json exists
- [ ] Return "" if file doesn't exist
- [ ] Generate timestamp: YYYYMMDD-HHMMSS format
- [ ] Create backup filename: f"{BACKUP_PREFIX}.{timestamp}.json"
- [ ] Copy file to backup location
- [ ] Implement try-except
  - [ ] Catch exceptions → log warning, return ""
  - [ ] Don't fail the operation on backup failure
- [ ] Return backup path on success

**Acceptance:**
- Creates timestamped backup file
- Returns empty string if source doesn't exist
- Doesn't fail operation if backup fails (just warns)

#### 1.2.8: Implement `find_task_by_id()` Function
- [ ] Add function signature with type hints
- [ ] Add comprehensive docstring
- [ ] Call load_tasks()
- [ ] Search for task with matching ID
- [ ] Return task dict or None

**Acceptance:**
- Returns task dict if found
- Returns None if not found
- Doesn't raise exceptions

#### 1.2.9: Implement `update_task()` Function
- [ ] Add function signature with type hints
- [ ] Add comprehensive docstring
- [ ] Call load_tasks()
- [ ] Find task with matching ID
- [ ] Return False if not found
- [ ] Update specified fields
- [ ] Set updated_at timestamp
- [ ] Call save_tasks()
- [ ] Return True on success

**Acceptance:**
- Updates only specified fields
- Preserves other fields
- Sets updated_at timestamp
- Returns False if task not found
- Returns True on success

#### 1.2.10: Implement `delete_task()` Function
- [ ] Add function signature with type hints
- [ ] Add comprehensive docstring
- [ ] Call load_tasks()
- [ ] Filter out task with matching ID
- [ ] Check if list changed (task was found)
- [ ] Return False if no change
- [ ] Call save_tasks() with filtered list
- [ ] Return True on success

**Acceptance:**
- Removes task by ID
- Returns False if task not found
- Returns True on successful deletion

#### 1.2.11: Write Unit Tests
- [ ] Create `tests/test_storage.py`
- [ ] Set up temp directory for test files
- [ ] Test load_tasks() with missing file
- [ ] Test load_tasks() with valid file
- [ ] Test load_tasks() with corrupted JSON
- [ ] Test save_tasks() atomic behavior
- [ ] Test get_next_id() with empty/populated lists
- [ ] Test backup_tasks() creates timestamped files
- [ ] Test find_task_by_id() found/not found
- [ ] Test update_task() success/failure
- [ ] Test delete_task() success/failure

**Acceptance:**
- All storage functions tested
- Tests use temp directories (no side effects)
- 100% code coverage for storage.py
- All tests pass

**Estimated Time:** 4-5 hours
**Dependencies:** utils/models.py (type hints only)

---

### Step 1.3: Update `utils/__init__.py`

**Priority:** HIGH (provides clean API)

**Tasks:**

- [ ] Import all public APIs from models.py
- [ ] Import all public APIs from storage.py
- [ ] Define __all__ list for explicit exports
- [ ] Add module docstring

**Acceptance:**
- All public APIs can be imported from utils package
- No internal/private functions exposed
- Clean import statements: `from utils import Task, load_tasks`

**Estimated Time:** 30 minutes
**Dependencies:** utils/models.py, utils/storage.py

---

## Phase 2: Skill Layer

### Skill Implementation Order

Based on dependencies and complexity:
1. **add_skill** (simplest, foundational)
2. **list_skill** (depends on formatting, no mutations)
3. **update_skill** (depends on add concepts)
4. **complete_skill** (specialized update)
5. **delete_skill** (with confirmation logic)
6. **scheduler_skill** (most complex, date handling)

---

### Step 2.1: Implement `skills/add_skill.py`

**Priority:** HIGH (foundational skill)

**Specification:** `skills/add_skill.md`

**Dependencies:** utils.models, utils.storage

**Tasks:**

#### 2.1.1: Create Basic Structure
- [ ] Create `skills/add_skill.py` file
- [ ] Add file docstring
- [ ] Add imports

**Imports:**
```python
from datetime import datetime
from typing import Dict, Any, Optional
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
```

#### 2.1.2: Implement `add_task()` Function
- [ ] Define function signature per spec:
  ```python
  def add_task(
      title: str,
      priority: str = "medium",
      category: str = "general",
      due_date: Optional[str] = None
  ) -> OperationResult:
  ```

- [ ] Add comprehensive docstring (Google style)
  - [ ] Description
  - [ ] Args section
  - [ ] Returns section
  - [ ] Raises section (none - returns OperationResult)

- [ ] Implement main try-except block

- [ ] **Validation Phase:**
  - [ ] Validate title using validate_title()
  - [ ] Parse priority using Priority.from_string()
  - [ ] Validate category using validate_category()
  - [ ] Validate due_date if provided using validate_due_date()

- [ ] **Task Creation Phase:**
  - [ ] Get next ID using get_next_id()
  - [ ] Create timestamp: datetime.utcnow().isoformat() + "Z"
  - [ ] Create Task object with all fields
    - [ ] id (from get_next_id)
    - [ ] title (validated)
    - [ ] priority (enum)
    - [ ] category (validated)
    - [ ] status (default PENDING)
    - [ ] completed (False)
    - [ ] created_at (timestamp)
    - [ ] due_date (if provided)

- [ ] **Persistence Phase:**
  - [ ] Load existing tasks using load_tasks()
  - [ ] Convert task to dict using task.to_dict()
  - [ ] Append to tasks list
  - [ ] Save using save_tasks()

- [ ] **Success Response:**
  - [ ] Return OperationResult.success_result()
  - [ ] Message: f"Task #{task.id} added successfully"
  - [ ] Data: task.to_dict()

- [ ] **Error Handling:**
  - [ ] Catch ValueError → return error_result with VALIDATION_ERROR
  - [ ] Catch StorageError → return error_result with STORAGE_ERROR
  - [ ] Catch any Exception → return error_result with generic error

**Acceptance:**
- Function follows skill specification exactly
- All validation performed before creating task
- Returns OperationResult in all cases
- Never raises exceptions (all caught and wrapped)
- Success message includes task ID
- Task data included in success response

#### 2.1.3: Write Unit Tests
- [ ] Create `tests/test_add_skill.py`
- [ ] Mock storage functions (load_tasks, save_tasks, get_next_id)
- [ ] Test successful task addition
- [ ] Test with all optional parameters
- [ ] Test empty title validation failure
- [ ] Test title too long validation failure
- [ ] Test invalid priority validation failure
- [ ] Test category validation
- [ ] Test storage error handling
- [ ] Test due date validation

**Acceptance:**
- All paths tested (success + all error scenarios)
- Mocks verify storage functions called correctly
- 100% code coverage
- All tests pass

**Estimated Time:** 2-3 hours
**Dependencies:** utils layer complete

---

### Step 2.2: Implement `skills/list_skill.py`

**Priority:** HIGH (essential feature)

**Specification:** `skills/list_skill.md`

**Dependencies:** utils.models, utils.storage

**Tasks:**

#### 2.2.1: Create Basic Structure
- [ ] Create `skills/list_skill.py` file
- [ ] Add file docstring
- [ ] Add imports (storage, models, rich)

**Imports:**
```python
from typing import List, Dict, Any, Optional
from rich.table import Table
from rich.console import Console
from utils import (
    Task,
    TaskFilter,
    OperationResult,
    Priority,
    Status,
    OutputFormat,
    load_tasks,
    format_priority,
    format_status,
    format_date_display,
    ERROR_CODES
)
```

#### 2.2.2: Implement Helper Functions

- [ ] Implement `_filter_tasks()` helper
  - [ ] Takes task list and TaskFilter
  - [ ] Returns filtered list using filter.matches()

- [ ] Implement `_sort_tasks()` helper
  - [ ] Takes task list, sort_by field, sort_order
  - [ ] Returns sorted list
  - [ ] Handles None values (push to end)

- [ ] Implement `_create_rich_table()` helper
  - [ ] Creates Table object with proper columns
  - [ ] Adds header row
  - [ ] Returns configured Table

- [ ] Implement `_add_task_to_table()` helper
  - [ ] Takes table and task
  - [ ] Formats task fields with colors
  - [ ] Adds row to table

#### 2.2.3: Implement `list_tasks()` Function

- [ ] Define function signature per spec:
  ```python
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
  ```

- [ ] Add comprehensive docstring

- [ ] Implement main try-except block

- [ ] **Data Retrieval:**
  - [ ] Load tasks using load_tasks()
  - [ ] Convert dicts to Task objects

- [ ] **Filtering:**
  - [ ] Create TaskFilter from parameters
  - [ ] Convert string enums if needed
  - [ ] Filter tasks using _filter_tasks()

- [ ] **Sorting:**
  - [ ] Sort using _sort_tasks() helper
  - [ ] Apply limit if specified

- [ ] **Formatting:**
  - [ ] If format == "table": create and populate rich Table
  - [ ] If format == "json": return JSON-serializable list
  - [ ] If format == "simple": create simple text list

- [ ] **Success Response:**
  - [ ] Return OperationResult.success_result()
  - [ ] Message: f"Showing {count} tasks"
  - [ ] Data: formatted output or task list

- [ ] **Error Handling:**
  - [ ] Catch ValueError (invalid enum) → VALIDATION_ERROR
  - [ ] Catch StorageError → STORAGE_ERROR
  - [ ] Catch any Exception → generic error

**Acceptance:**
- All filter options work correctly
- Sorting works for all fields in both directions
- Table format uses rich with proper colors
- JSON format returns valid JSON
- Simple format is human-readable
- Empty list handled gracefully

#### 2.2.4: Write Unit Tests
- [ ] Create `tests/test_list_skill.py`
- [ ] Mock load_tasks()
- [ ] Test listing all tasks
- [ ] Test each filter option independently
- [ ] Test filter combinations
- [ ] Test sorting by each field
- [ ] Test ascending/descending order
- [ ] Test limit option
- [ ] Test each output format
- [ ] Test empty task list
- [ ] Test error handling

**Acceptance:**
- All filter/sort combinations tested
- Output formats verified
- 100% code coverage
- All tests pass

**Estimated Time:** 3-4 hours
**Dependencies:** utils layer complete

---

### Step 2.3: Implement `skills/update_skill.py`

**Priority:** MEDIUM (common operation)

**Specification:** `skills/update_skill.md`

**Dependencies:** utils.models, utils.storage

**Tasks:**

#### 2.3.1: Create Basic Structure
- [ ] Create `skills/update_skill.py` file
- [ ] Add file docstring
- [ ] Add imports

#### 2.3.2: Implement `update_task()` Function
- [ ] Define function signature per spec
- [ ] Add comprehensive docstring
- [ ] Validate at least one field to update provided
- [ ] Find task by ID
- [ ] Return error if not found
- [ ] Build updates dict with validated values
- [ ] Convert string enums to Enum types
- [ ] Update task using storage.update_task()
- [ ] Track which fields changed for response message
- [ ] Return success with change summary

**Acceptance:**
- At least one field required
- Non-existent task returns clear error
- Only specified fields updated
- updated_at timestamp set automatically
- Success message lists what changed

#### 2.3.3: Write Unit Tests
- [ ] Create `tests/test_update_skill.py`
- [ ] Test updating each field individually
- [ ] Test updating multiple fields
- [ ] Test with invalid task ID
- [ ] Test with no fields specified
- [ ] Test with invalid field values
- [ ] Test enum conversion

**Estimated Time:** 2-3 hours
**Dependencies:** utils layer complete

---

### Step 2.4: Implement `skills/complete_skill.py`

**Priority:** MEDIUM (frequently used)

**Specification:** `skills/complete_skill.md`

**Dependencies:** utils.models, utils.storage

**Tasks:**

#### 2.4.1: Create Basic Structure
- [ ] Create `skills/complete_skill.py` file
- [ ] Add file docstring
- [ ] Add imports

#### 2.4.2: Implement `complete_task()` Function
- [ ] Define function signature per spec:
  ```python
  def complete_task(
      task_id: int,
      uncomplete: bool = False,
      toggle: bool = False
  ) -> OperationResult:
  ```
- [ ] Find task by ID
- [ ] Return error if not found
- [ ] If toggle: flip completed status
- [ ] If uncomplete: mark as incomplete
- [ ] Else: mark as completed
- [ ] Use Task.mark_completed() or Task.mark_incomplete()
- [ ] Update task in storage
- [ ] Return success with appropriate message

**Acceptance:**
- Marks task as completed with timestamp
- Uncomplete flag works correctly
- Toggle flag works correctly
- Task not found returns error
- Already completed task handled gracefully

#### 2.4.3: Write Unit Tests
- [ ] Create `tests/test_complete_skill.py`
- [ ] Test marking as complete
- [ ] Test uncomplete flag
- [ ] Test toggle flag
- [ ] Test with invalid task ID
- [ ] Test timestamps set correctly

**Estimated Time:** 1.5-2 hours
**Dependencies:** utils layer complete

---

### Step 2.5: Implement `skills/delete_skill.py`

**Priority:** MEDIUM (destructive, needs care)

**Specification:** `skills/delete_skill.md`

**Dependencies:** utils.models, utils.storage

**Tasks:**

#### 2.5.1: Create Basic Structure
- [ ] Create `skills/delete_skill.py` file
- [ ] Add file docstring
- [ ] Add imports

#### 2.5.2: Implement `delete_task()` Function
- [ ] Define function signature per spec:
  ```python
  def delete_task(
      task_id: int,
      force: bool = False
  ) -> OperationResult:
  ```
- [ ] Find task by ID
- [ ] Return error if not found
- [ ] If not force, return with confirmation_required flag
  - [ ] Include task details in data
- [ ] Create backup using backup_tasks()
- [ ] Delete task using storage.delete_task()
- [ ] Return success with deleted task info

**Acceptance:**
- Task not found returns error
- Backup created before deletion
- Force flag skips confirmation
- Success message includes deleted task details

#### 2.5.3: Write Unit Tests
- [ ] Create `tests/test_delete_skill.py`
- [ ] Test successful deletion
- [ ] Test with invalid task ID
- [ ] Test force flag behavior
- [ ] Test backup creation

**Estimated Time:** 1.5-2 hours
**Dependencies:** utils layer complete

---

### Step 2.6: Implement `skills/scheduler_skill.py`

**Priority:** LOW (advanced feature)

**Specification:** `skills/scheduler_skill.md`

**Dependencies:** utils.models, utils.storage

**Tasks:**

#### 2.6.1: Create Basic Structure
- [ ] Create `skills/scheduler_skill.py` file
- [ ] Add file docstring
- [ ] Add imports (including dateutil if needed)

#### 2.6.2: Implement Due Date Functions
- [ ] `set_due_date(task_id: int, due_date: str) -> OperationResult`
  - [ ] Validate date format
  - [ ] Update task with due date
  - [ ] Return success

- [ ] `get_upcoming_tasks(days: int = 7) -> OperationResult`
  - [ ] Load all tasks
  - [ ] Filter by due date in range
  - [ ] Sort by due date
  - [ ] Return task list

- [ ] `get_overdue_tasks() -> OperationResult`
  - [ ] Load all tasks
  - [ ] Filter using Task.is_overdue()
  - [ ] Sort by priority and days overdue
  - [ ] Return task list

**Acceptance:**
- Due dates parsed and validated
- Upcoming tasks filtered correctly
- Overdue tasks identified correctly
- Date calculations handle timezones

#### 2.6.3: Write Unit Tests
- [ ] Create `tests/test_scheduler_skill.py`
- [ ] Test set_due_date with various formats
- [ ] Test get_upcoming_tasks
- [ ] Test get_overdue_tasks
- [ ] Test date edge cases

**Estimated Time:** 3-4 hours (complex date handling)
**Dependencies:** utils layer complete

---

## Phase 3: Integration Layer (CLI)

### Step 3.1: Implement `main.py`

**Priority:** CRITICAL (user-facing interface)

**Specification:** `specs/integration/main-cli-spec.md`

**Dependencies:** All skills, utils

**Tasks:**

#### 3.1.1: Create Basic Structure
- [ ] Create `main.py` file
- [ ] Add file docstring
- [ ] Add imports

**Imports:**
```python
import sys
from datetime import datetime
from typing import Optional, Dict, Any
import typer
from rich.console import Console
from rich.table import Table

# All skill imports
from skills.add_skill import add_task
from skills.list_skill import list_tasks as list_tasks_skill
from skills.update_skill import update_task
from skills.complete_skill import complete_task
from skills.delete_skill import delete_task
from skills.scheduler_skill import (
    set_due_date,
    get_upcoming_tasks,
    get_overdue_tasks
)
from utils import StorageError, find_task_by_id
```

#### 3.1.2: Initialize Typer App
- [ ] Create typer.Typer() instance
  - [ ] name="todo"
  - [ ] help="Phase 1 Console Todo Application"
  - [ ] add_completion=False

- [ ] Create Console() instance for rich output

- [ ] Define constants (APP_VERSION, etc.)

#### 3.1.3: Implement Helper Functions

- [ ] `handle_skill_response(response: OperationResult) -> None`
  - [ ] Check response.success
  - [ ] Print success message in green
  - [ ] Print error message in red and exit(1)

- [ ] `display_task(task: Dict[str, Any]) -> None`
  - [ ] Format and display single task details

#### 3.1.4: Implement Commands

**For each command:**

1. **`add` Command**
- [ ] Define @app.command() with proper signature
- [ ] Add typer.Argument and typer.Option decorators
- [ ] Add docstring
- [ ] Call add_task() skill function
- [ ] Handle response with handle_skill_response()
- [ ] Display formatted success output

2. **`list` Command**
- [ ] Define command with all filter options
- [ ] Build filter dict from parameters
- [ ] Call list_tasks_skill()
- [ ] Handle response
- [ ] Display table/json/simple output

3. **`update` Command**
- [ ] Define command with optional update fields
- [ ] Validate at least one field provided
- [ ] Build updates dict
- [ ] Call update_task()
- [ ] Display change summary

4. **`delete` Command**
- [ ] Define command with task_id and force flag
- [ ] If not force: display task and prompt for confirmation
- [ ] Call delete_task()
- [ ] Display success message

5. **`complete` Command**
- [ ] Define command with task_id and flags
- [ ] Call complete_task()
- [ ] Display success with task details

6. **`show` Command**
- [ ] Define command with task_id
- [ ] Call find_task_by_id()
- [ ] Display formatted task details

7. **`schedule` Command**
- [ ] Define command with task_id and options
- [ ] If upcoming flag: call get_upcoming_tasks()
- [ ] Else: call set_due_date()
- [ ] Display results

8. **`overdue` Command**
- [ ] Define command (no args)
- [ ] Call get_overdue_tasks()
- [ ] Display overdue tasks with warnings

#### 3.1.5: Implement Global Callback
- [ ] @app.callback() for version flag
- [ ] Handle --version option
- [ ] Display version and exit

#### 3.1.6: Add Main Entry Point
- [ ] Add `if __name__ == "__main__": app()` block

#### 3.1.7: Optional: Command Aliases
- [ ] Create alias commands (ls, rm, done)
- [ ] Wire to main commands

**Acceptance:**
- All commands work as specified
- Help text clear and useful (--help)
- Error messages displayed in red
- Success messages displayed in green
- Confirmation prompts work
- Exit codes correct (0 success, 1 error)

**Estimated Time:** 5-6 hours
**Dependencies:** All skills implemented

---

### Step 3.2: Create Command-Line Entry Point

**Tasks:**
- [ ] Update `pyproject.toml` with script entry point
  ```toml
  [project.scripts]
  todo = "main:app"
  ```
- [ ] Test installation: `pip install -e .`
- [ ] Verify `todo` command works from shell

**Estimated Time:** 30 minutes

---

## Phase 4: Testing & Validation

### Step 4.1: Integration Testing

**Tasks:**

#### 4.1.1: Create Integration Test Suite
- [ ] Create `tests/test_integration.py`
- [ ] Set up temp directory for test data
- [ ] Use typer.testing.CliRunner

#### 4.1.2: Test Complete Workflows
- [ ] Test full workflow: add → list → update → complete → delete
- [ ] Test filter combinations
- [ ] Test error scenarios
- [ ] Test with empty data file
- [ ] Test with populated data file

**Acceptance:**
- All workflows execute successfully
- Data persists correctly across operations
- Errors handled gracefully

**Estimated Time:** 2-3 hours

---

### Step 4.2: Manual Testing

**Tasks:**

#### 4.2.1: CLI Testing Checklist
- [ ] Install in development mode: `pip install -e .`
- [ ] Test each command manually
- [ ] Test `todo --help`
- [ ] Test `todo add --help`
- [ ] Verify colors display correctly
- [ ] Verify table formatting
- [ ] Test invalid inputs
- [ ] Test edge cases (empty lists, long titles, etc.)

#### 4.2.2: Create Sample Data
- [ ] Add diverse sample tasks
- [ ] Test filtering and sorting
- [ ] Test overdue detection
- [ ] Test completion marking

**Estimated Time:** 1-2 hours

---

### Step 4.3: Acceptance Criteria Verification

**Tasks:**

For each specification file, verify:

#### 4.3.1: Constitution Compliance
- [ ] All code has type hints
- [ ] All code has docstrings (Google style)
- [ ] All functions have try-except blocks
- [ ] All errors return structured responses
- [ ] No circular imports
- [ ] Modular architecture maintained

#### 4.3.2: Storage Specification
- [ ] All storage functions implemented
- [ ] Atomic writes verified
- [ ] Error handling tested
- [ ] Backup creation works

#### 4.3.3: Models Specification
- [ ] All enums implemented
- [ ] Task dataclass complete
- [ ] Validation functions work
- [ ] Format functions return rich markup

#### 4.3.4: Skill Specifications
For each skill:
- [ ] All inputs validated
- [ ] All outputs match spec
- [ ] All error scenarios handled
- [ ] Acceptance criteria met

#### 4.3.5: CLI Specification
- [ ] All commands implemented
- [ ] All options work correctly
- [ ] Help text useful
- [ ] Colors and formatting correct

**Estimated Time:** 2-3 hours

---

### Step 4.4: Code Quality Checks

**Tasks:**

#### 4.4.1: Run Linters (if configured)
- [ ] Run black (formatting)
- [ ] Run mypy (type checking)
- [ ] Run pylint (code quality)

#### 4.4.2: Test Coverage
- [ ] Run pytest with coverage
- [ ] Verify coverage > 80%
- [ ] Review uncovered lines
- [ ] Add missing tests if needed

#### 4.4.3: Documentation Check
- [ ] Verify all docstrings present
- [ ] Check docstring format consistency
- [ ] Verify examples in docstrings work

**Estimated Time:** 1-2 hours

---

## Phase 5: Documentation & Finalization

### Step 5.1: Create User Documentation

**Tasks:**

#### 5.1.1: Update README.md
- [ ] Add project description
- [ ] Add installation instructions
- [ ] Add usage examples for each command
- [ ] Add features list
- [ ] Add requirements
- [ ] Add development setup instructions
- [ ] Add testing instructions

#### 5.1.2: Create Examples
- [ ] Add examples/ directory with sample workflows
- [ ] Create tutorial walkthrough

**Estimated Time:** 1-2 hours

---

### Step 5.2: Final Review

**Tasks:**

- [ ] Review all code against specifications
- [ ] Verify constitution compliance
- [ ] Check all acceptance criteria
- [ ] Run full test suite
- [ ] Manual end-to-end testing
- [ ] Review error messages for clarity
- [ ] Check performance (load time, response time)

**Estimated Time:** 1-2 hours

---

## Summary & Timeline

### Implementation Summary

| Phase | Component | Est. Time |
|-------|-----------|-----------|
| 1.1 | utils/models.py | 4-6 hours |
| 1.2 | utils/storage.py | 4-5 hours |
| 1.3 | utils/__init__.py | 0.5 hours |
| 2.1 | skills/add_skill.py | 2-3 hours |
| 2.2 | skills/list_skill.py | 3-4 hours |
| 2.3 | skills/update_skill.py | 2-3 hours |
| 2.4 | skills/complete_skill.py | 1.5-2 hours |
| 2.5 | skills/delete_skill.py | 1.5-2 hours |
| 2.6 | skills/scheduler_skill.py | 3-4 hours |
| 3.1 | main.py | 5-6 hours |
| 3.2 | Entry point setup | 0.5 hours |
| 4.1 | Integration testing | 2-3 hours |
| 4.2 | Manual testing | 1-2 hours |
| 4.3 | Acceptance verification | 2-3 hours |
| 4.4 | Code quality checks | 1-2 hours |
| 5.1 | Documentation | 1-2 hours |
| 5.2 | Final review | 1-2 hours |
| **Total** | | **37-52 hours** |

### Recommended Schedule

**Week 1: Foundation**
- Days 1-2: utils/models.py + tests
- Days 3-4: utils/storage.py + tests
- Day 5: utils/__init__.py + review

**Week 2: Skills (Part 1)**
- Day 1: add_skill.py + tests
- Day 2: list_skill.py + tests
- Day 3: update_skill.py + tests
- Day 4: complete_skill.py + tests
- Day 5: delete_skill.py + tests

**Week 3: Skills (Part 2) + CLI**
- Day 1: scheduler_skill.py + tests
- Days 2-4: main.py + all commands
- Day 5: Entry point + initial testing

**Week 4: Testing & Polish**
- Days 1-2: Integration testing
- Day 3: Manual testing + bug fixes
- Day 4: Acceptance criteria verification
- Day 5: Documentation + final review

---

## Risk Mitigation

### Potential Risks

1. **Atomic writes not working on Windows**
   - Mitigation: Test on target platform early
   - Fallback: Use different strategy for Windows

2. **Date parsing complexity**
   - Mitigation: Start with simple ISO format only
   - Enhancement: Add natural language parsing in Phase 2

3. **Rich library formatting issues in terminals**
   - Mitigation: Test in multiple terminal emulators
   - Fallback: Provide simple text mode

4. **Test coverage gaps**
   - Mitigation: Write tests alongside implementation
   - Regular coverage checks

5. **Specification ambiguities**
   - Mitigation: Clarify with user before implementation
   - Document decisions

---

## Success Criteria

### Must Have (Phase 1)
- ✅ All 6 core skills implemented
- ✅ CLI with all 8 commands functional
- ✅ Data persists reliably (atomic writes)
- ✅ Rich formatted output
- ✅ Comprehensive error handling
- ✅ Test coverage > 80%
- ✅ All constitution principles followed

### Nice to Have (Future Phases)
- Command aliases working
- Natural language date parsing
- Recurring tasks
- Task search
- Export functionality

---

## Next Steps

1. **Get approval** for this implementation plan
2. **Begin with Phase 1.1**: Implement utils/models.py
3. **Follow sequence**: Don't skip ahead - dependencies matter
4. **Test continuously**: Write tests alongside implementation
5. **Review regularly**: Check against specifications frequently

---

## Questions for User

Before proceeding with implementation:

1. **Platform target**: Primary OS for development/testing? (impacts atomic write testing)
2. **Date handling**: Start with simple ISO format or include natural language parsing?
3. **Testing framework**: Any preference beyond pytest?
4. **Code quality tools**: Want black, mypy, pylint configured?
5. **Documentation**: Any specific format preferences for README?

---

**Version**: 1.0.0
**Created**: 2025-12-25
**Status**: Ready for implementation
