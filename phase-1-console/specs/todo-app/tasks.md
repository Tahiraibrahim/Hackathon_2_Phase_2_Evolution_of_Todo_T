# Phase 1 Console Todo App - Implementation Tasks

## Task Overview

This document provides a detailed, actionable checklist for implementing the Todo App. Follow tasks in the exact order listed to respect dependencies.

**Total Estimated Time:** 37-52 hours over 4 weeks

---

## PHASE 0: Project Setup & Dependencies

### Task 0.1: Environment Setup
**Estimated Time:** 30 minutes

#### Setup Tasks
- [ ] Verify Python 3.12+ installed: `python --version`
- [ ] Navigate to project directory: `cd /home/tahiraibrahim7/Evolution-of-Todo/phase-1-console`
- [ ] Create virtual environment: `python -m venv venv`
- [ ] Activate virtual environment:
  - Linux/Mac: `source venv/bin/activate`
  - Windows: `venv\Scripts\activate`
- [ ] Verify venv active: `which python` should show venv path

**Acceptance Criteria:**
- [ ] Python 3.12+ confirmed
- [ ] Virtual environment created and activated
- [ ] `which python` points to venv

---

### Task 0.2: Install Dependencies
**Estimated Time:** 15 minutes

#### Core Dependencies (Production)
- [ ] Install typer: `pip install "typer[all]"`
- [ ] Install rich: `pip install rich`
- [ ] Verify typer installed: `python -c "import typer; print(typer.__version__)"`
- [ ] Verify rich installed: `python -c "import rich; print(rich.__version__)"`

#### Development Dependencies
- [ ] Install pytest: `pip install pytest`
- [ ] Install pytest-cov: `pip install pytest-cov`
- [ ] Install pytest-mock: `pip install pytest-mock`
- [ ] Verify pytest: `pytest --version`

#### Optional Quality Tools
- [ ] Install black (formatter): `pip install black`
- [ ] Install mypy (type checker): `pip install mypy`
- [ ] Install pylint (linter): `pip install pylint`

#### Create Requirements Files
- [ ] Create `requirements.txt`:
  ```
  typer[all]>=0.9.0
  rich>=13.0.0
  ```
- [ ] Create `requirements-dev.txt`:
  ```
  -r requirements.txt
  pytest>=7.0.0
  pytest-cov>=4.0.0
  pytest-mock>=3.10.0
  black>=23.0.0
  mypy>=1.0.0
  pylint>=2.17.0
  ```
- [ ] Install from requirements: `pip install -r requirements-dev.txt`
- [ ] Freeze current environment: `pip freeze > requirements-frozen.txt`

**Acceptance Criteria:**
- [ ] All core dependencies installed
- [ ] All dev dependencies installed
- [ ] Can import typer, rich, pytest
- [ ] requirements.txt created
- [ ] requirements-dev.txt created

---

### Task 0.3: Create Project Structure
**Estimated Time:** 10 minutes

#### Directory Structure
- [ ] Create `utils/` directory: `mkdir -p utils`
- [ ] Create `skills/` directory: `mkdir -p skills`
- [ ] Create `tests/` directory: `mkdir -p tests`
- [ ] Create `specs/` directory (if not exists): `mkdir -p specs`
- [ ] Create `.gitignore` file with:
  ```
  # Python
  __pycache__/
  *.py[cod]
  *$py.class
  *.so
  .Python
  venv/
  env/
  ENV/

  # Testing
  .pytest_cache/
  .coverage
  htmlcov/

  # IDE
  .vscode/
  .idea/
  *.swp
  *.swo

  # Data files
  todos.json
  todos.backup.*.json

  # OS
  .DS_Store
  Thumbs.db
  ```

#### Verify Structure
- [ ] Run: `tree -L 2 -a` (or `ls -R`) to verify structure
- [ ] Expected structure exists:
  ```
  phase-1-console/
  ├── .gitignore
  ├── requirements.txt
  ├── requirements-dev.txt
  ├── utils/
  ├── skills/
  ├── tests/
  └── specs/
  ```

**Acceptance Criteria:**
- [ ] All directories created
- [ ] .gitignore configured
- [ ] Requirements files in place
- [ ] Directory structure verified

---

## PHASE 1: Foundation Layer (Utils)

### Task 1.1: Implement `utils/models.py`
**Priority:** CRITICAL
**Estimated Time:** 4-6 hours
**Dependencies:** None
**Specification:** `specs/integration/models-spec.md`

#### Files to Create
- [ ] `utils/__init__.py` (empty for now)
- [ ] `utils/models.py`
- [ ] `tests/test_models.py`

#### 1.1.1: Create Basic Structure (30 min)
- [ ] Create `utils/models.py` file: `touch utils/models.py`
- [ ] Add file docstring:
  ```python
  """
  Data models and type definitions for Todo App.

  Provides type-safe data structures, enums, validation functions,
  and formatting utilities used across the application.
  """
  ```
- [ ] Add imports:
  ```python
  from dataclasses import dataclass, field, asdict
  from datetime import datetime
  from enum import Enum
  from typing import List, Dict, Any, Optional, Callable
  ```

**Test:** `python -c "import utils.models"` should not error

#### 1.1.2: Implement Enumerations (1 hour)
- [ ] Implement `Priority` enum (HIGH, MEDIUM, LOW)
  - [ ] Add `default()` classmethod → returns MEDIUM
  - [ ] Add `from_string(value)` classmethod with case-insensitive parsing
  - [ ] Raise ValueError for invalid values with helpful message

- [ ] Implement `Status` enum (PENDING, IN_PROGRESS, COMPLETED)
  - [ ] Add `default()` classmethod → returns PENDING
  - [ ] Add `from_string(value)` classmethod

- [ ] Implement `OutputFormat` enum (TABLE, JSON, SIMPLE)
  - [ ] Add `default()` classmethod → returns TABLE

- [ ] Implement `SortOrder` enum (ASC, DESC)
  - [ ] Add `default()` classmethod → returns ASC

**Test Cases:**
```python
# In tests/test_models.py
def test_priority_from_string():
    assert Priority.from_string("high") == Priority.HIGH
    assert Priority.from_string("HIGH") == Priority.HIGH
    with pytest.raises(ValueError):
        Priority.from_string("invalid")

def test_priority_default():
    assert Priority.default() == Priority.MEDIUM
```

#### 1.1.3: Implement Task Dataclass (2 hours)
- [ ] Define `Task` dataclass with fields:
  - [ ] id: int
  - [ ] title: str
  - [ ] priority: Priority = Priority.MEDIUM
  - [ ] category: str = "general"
  - [ ] status: Status = Status.PENDING
  - [ ] completed: bool = False
  - [ ] created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
  - [ ] updated_at: Optional[str] = None
  - [ ] completed_at: Optional[str] = None
  - [ ] due_date: Optional[str] = None

- [ ] Implement `__post_init__()`:
  - [ ] Convert string priority to Priority enum if needed
  - [ ] Convert string status to Status enum if needed
  - [ ] Validate title (strip, not empty, max 200 chars)
  - [ ] Validate category (max 50 chars)
  - [ ] Raise ValueError with clear messages for invalid data

- [ ] Implement `to_dict()` method:
  - [ ] Use asdict()
  - [ ] Convert enums to string values
  - [ ] Return JSON-serializable dict

- [ ] Implement `from_dict(data)` classmethod:
  - [ ] Create Task from dictionary
  - [ ] Handle string enum conversions

- [ ] Implement helper methods:
  - [ ] `mark_completed()` → set completed=True, status=COMPLETED, add timestamp
  - [ ] `mark_incomplete()` → set completed=False, status=PENDING, clear timestamp
  - [ ] `update_fields(**kwargs)` → update fields, set updated_at
  - [ ] `is_overdue()` → check if due_date < now and not completed
  - [ ] `days_until_due()` → calculate days (negative if overdue)

**Test Cases:**
```python
def test_task_creation():
    task = Task(id=1, title="Test Task")
    assert task.priority == Priority.MEDIUM
    assert task.status == Status.PENDING
    assert task.completed == False

def test_task_validation():
    with pytest.raises(ValueError, match="empty"):
        Task(id=1, title="   ")

def test_task_to_dict():
    task = Task(id=1, title="Test")
    data = task.to_dict()
    assert data["priority"] == "medium"
    assert isinstance(data, dict)

def test_mark_completed():
    task = Task(id=1, title="Test")
    task.mark_completed()
    assert task.completed == True
    assert task.status == Status.COMPLETED
    assert task.completed_at is not None
```

#### 1.1.4: Implement Supporting Dataclasses (45 min)
- [ ] Implement `TaskFilter` dataclass:
  - [ ] Fields: status, priority, category, completed, overdue_only (all Optional except overdue_only)
  - [ ] Implement `matches(task: Task) -> bool` method

- [ ] Implement `OperationResult` dataclass:
  - [ ] Fields: success, message, data, error, error_code
  - [ ] Implement `success_result(message, data)` classmethod
  - [ ] Implement `error_result(error, code)` classmethod
  - [ ] Implement `to_dict()` method

**Test Cases:**
```python
def test_task_filter_matches():
    task = Task(id=1, title="Test", priority=Priority.HIGH)
    filter = TaskFilter(priority=Priority.HIGH)
    assert filter.matches(task) == True

def test_operation_result_success():
    result = OperationResult.success_result("Success", {"id": 1})
    assert result.success == True
    assert result.message == "Success"
    assert result.data["id"] == 1
```

#### 1.1.5: Implement Constants (30 min)
- [ ] DEFAULT_PRIORITY = Priority.MEDIUM
- [ ] DEFAULT_CATEGORY = "general"
- [ ] DEFAULT_STATUS = Status.PENDING
- [ ] MIN_TITLE_LENGTH = 1
- [ ] MAX_TITLE_LENGTH = 200
- [ ] MAX_CATEGORY_LENGTH = 50
- [ ] ISO_DATE_FORMAT = "%Y-%m-%d"
- [ ] ISO_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
- [ ] DISPLAY_DATE_FORMAT = "%b %d, %Y"
- [ ] DISPLAY_DATETIME_FORMAT = "%b %d, %Y at %I:%M %p"
- [ ] PRIORITY_COLORS = {Priority.HIGH: "red", Priority.MEDIUM: "yellow", Priority.LOW: "green"}
- [ ] STATUS_COLORS = {Status.PENDING: "white", Status.IN_PROGRESS: "blue", Status.COMPLETED: "green"}
- [ ] STATUS_ICONS = {Status.PENDING: "○", Status.IN_PROGRESS: "◐", Status.COMPLETED: "✓"}
- [ ] ERROR_CODES = {
    "NOT_FOUND": "TASK_NOT_FOUND",
    "VALIDATION_ERROR": "VALIDATION_ERROR",
    "STORAGE_ERROR": "STORAGE_ERROR",
    "INVALID_INPUT": "INVALID_INPUT",
    "NO_CHANGES": "NO_CHANGES_PROVIDED"
  }

#### 1.1.6: Implement Validation Functions (45 min)
- [ ] `validate_title(title: str) -> str`:
  - [ ] Strip whitespace
  - [ ] Check not empty → raise ValueError
  - [ ] Check max length → raise ValueError
  - [ ] Return normalized title

- [ ] `validate_category(category: str) -> str`:
  - [ ] Strip whitespace
  - [ ] Check max length → raise ValueError
  - [ ] Return default if empty

- [ ] `validate_due_date(due_date: str) -> str`:
  - [ ] Parse ISO 8601 format
  - [ ] Reformat for consistency
  - [ ] Raise ValueError for invalid format

**Test Cases:**
```python
def test_validate_title():
    assert validate_title("  Test  ") == "Test"
    with pytest.raises(ValueError):
        validate_title("")
    with pytest.raises(ValueError):
        validate_title("x" * 201)
```

#### 1.1.7: Implement Formatting Functions (30 min)
- [ ] `format_priority(priority: Priority) -> str`:
  - [ ] Return `[{color}]{value}[/{color}]` for rich

- [ ] `format_status(status: Status) -> str`:
  - [ ] Return `[{color}]{icon} {value}[/{color}]` for rich

- [ ] `format_date_display(iso_date: Optional[str]) -> str`:
  - [ ] Convert ISO to human-readable
  - [ ] Return "-" for None

- [ ] `format_datetime_display(iso_datetime: Optional[str]) -> str`:
  - [ ] Convert ISO to human-readable datetime
  - [ ] Return "-" for None

**Test Cases:**
```python
def test_format_priority():
    result = format_priority(Priority.HIGH)
    assert "[red]high[/red]" == result

def test_format_date_display():
    assert format_date_display(None) == "-"
    # Test valid ISO date formatting
```

#### 1.1.8: Write Unit Tests (1 hour)
- [ ] Create `tests/test_models.py`
- [ ] Test all enum from_string() methods (4 enums)
- [ ] Test all enum default() methods (4 enums)
- [ ] Test Task creation with defaults
- [ ] Test Task validation in __post_init__ (empty title, long title, long category)
- [ ] Test Task to_dict() serialization
- [ ] Test Task from_dict() deserialization
- [ ] Test Task.mark_completed()
- [ ] Test Task.mark_incomplete()
- [ ] Test Task.update_fields()
- [ ] Test Task.is_overdue()
- [ ] Test Task.days_until_due()
- [ ] Test TaskFilter.matches() with various filters
- [ ] Test OperationResult.success_result()
- [ ] Test OperationResult.error_result()
- [ ] Test validate_title() (valid, empty, too long)
- [ ] Test validate_category() (valid, empty, too long)
- [ ] Test validate_due_date() (valid ISO, invalid format)
- [ ] Test all formatting functions

- [ ] Run tests: `pytest tests/test_models.py -v`
- [ ] Check coverage: `pytest tests/test_models.py --cov=utils.models --cov-report=term-missing`
- [ ] Verify >95% coverage

**Acceptance Criteria:**
- [ ] All tests pass
- [ ] Coverage >95%
- [ ] No linting errors: `pylint utils/models.py`
- [ ] Type checking passes: `mypy utils/models.py`
- [ ] Can import all classes and functions

---

### Task 1.2: Implement `utils/storage.py`
**Priority:** CRITICAL
**Estimated Time:** 4-5 hours
**Dependencies:** utils/models.py (for type hints only)
**Specification:** `specs/integration/storage-spec.md`

#### Files to Create
- [ ] `utils/storage.py`
- [ ] `tests/test_storage.py`

#### 1.2.1: Create Basic Structure (30 min)
- [ ] Create `utils/storage.py` file: `touch utils/storage.py`
- [ ] Add file docstring
- [ ] Add imports:
  ```python
  import json
  import os
  from datetime import datetime
  from pathlib import Path
  from typing import List, Dict, Any, Optional
  ```

- [ ] Define `StorageError` exception:
  ```python
  class StorageError(Exception):
      """Raised when storage operations fail."""
      pass
  ```

- [ ] Define constants:
  ```python
  TODOS_FILE = "todos.json"
  BACKUP_PREFIX = "todos.backup"
  DEFAULT_PRIORITY = "medium"
  DEFAULT_CATEGORY = "general"
  DEFAULT_STATUS = "pending"
  ```

**Test:** `python -c "from utils.storage import StorageError"` should work

#### 1.2.2: Implement `load_tasks()` (45 min)
- [ ] Function signature: `def load_tasks() -> List[Dict[str, Any]]:`
- [ ] Add comprehensive docstring (Google style)
- [ ] Check if TODOS_FILE exists
- [ ] Return [] if FileNotFoundError
- [ ] Read file contents
- [ ] Parse JSON
- [ ] Validate it's a list
- [ ] Catch json.JSONDecodeError → raise StorageError("Corrupted todos.json")
- [ ] Catch PermissionError → raise StorageError("Permission denied")
- [ ] Return task list

**Test Cases:**
```python
def test_load_tasks_missing_file(tmp_path):
    os.chdir(tmp_path)
    tasks = load_tasks()
    assert tasks == []

def test_load_tasks_valid(tmp_path):
    os.chdir(tmp_path)
    with open("todos.json", "w") as f:
        json.dump([{"id": 1, "title": "Test"}], f)
    tasks = load_tasks()
    assert len(tasks) == 1
    assert tasks[0]["id"] == 1

def test_load_tasks_corrupted(tmp_path):
    os.chdir(tmp_path)
    with open("todos.json", "w") as f:
        f.write("{invalid json")
    with pytest.raises(StorageError, match="Corrupted"):
        load_tasks()
```

#### 1.2.3: Implement `save_tasks()` (1 hour)
- [ ] Function signature: `def save_tasks(tasks: List[Dict[str, Any]]) -> bool:`
- [ ] Add comprehensive docstring
- [ ] Validate input is a list
- [ ] Create temp file: "todos.json.tmp"
- [ ] Open temp file for writing
- [ ] Write JSON with `json.dump(tasks, f, indent=2, ensure_ascii=False)`
- [ ] Flush: `f.flush()`
- [ ] Sync to disk: `os.fsync(f.fileno())`
- [ ] Close file
- [ ] Atomic rename: `os.replace(temp_file, TODOS_FILE)`
- [ ] Implement try-except-finally:
  - [ ] Catch PermissionError → raise StorageError
  - [ ] Catch OSError → raise StorageError
  - [ ] Finally: clean up temp file if exists
- [ ] Return True

**Test Cases:**
```python
def test_save_tasks_creates_file(tmp_path):
    os.chdir(tmp_path)
    tasks = [{"id": 1, "title": "Test"}]
    result = save_tasks(tasks)
    assert result == True
    assert os.path.exists("todos.json")

def test_save_tasks_atomic(tmp_path):
    os.chdir(tmp_path)
    # Write initial data
    save_tasks([{"id": 1}])
    # Verify temp file not left behind
    assert not os.path.exists("todos.json.tmp")

def test_save_tasks_pretty_print(tmp_path):
    os.chdir(tmp_path)
    save_tasks([{"id": 1, "title": "Test"}])
    with open("todos.json") as f:
        content = f.read()
    assert "\n" in content  # Pretty printed
```

#### 1.2.4: Implement Helper Functions (1.5 hours)
- [ ] `get_next_id() -> int`:
  - [ ] Load tasks
  - [ ] Return 1 if empty
  - [ ] Return max(task['id']) + 1

- [ ] `backup_tasks() -> str`:
  - [ ] Check if todos.json exists → return "" if not
  - [ ] Generate timestamp: `datetime.now().strftime("%Y%m%d-%H%M%S")`
  - [ ] Create backup filename: `f"{BACKUP_PREFIX}.{timestamp}.json"`
  - [ ] Copy file using shutil.copy2()
  - [ ] Return backup path
  - [ ] Catch exceptions → log warning, return ""

- [ ] `find_task_by_id(task_id: int) -> Optional[Dict[str, Any]]`:
  - [ ] Load tasks
  - [ ] Search for task with matching ID
  - [ ] Return task dict or None

- [ ] `update_task(task_id: int, updates: Dict[str, Any]) -> bool`:
  - [ ] Load tasks
  - [ ] Find task with matching ID
  - [ ] Return False if not found
  - [ ] Update specified fields
  - [ ] Set updated_at timestamp
  - [ ] Save tasks
  - [ ] Return True

- [ ] `delete_task(task_id: int) -> bool`:
  - [ ] Load tasks
  - [ ] Filter out task with matching ID
  - [ ] Check if list changed (was task found?)
  - [ ] Return False if no change
  - [ ] Save filtered list
  - [ ] Return True

**Test Cases:**
```python
def test_get_next_id_empty():
    assert get_next_id() == 1

def test_get_next_id_existing(tmp_path):
    os.chdir(tmp_path)
    save_tasks([{"id": 1}, {"id": 3}, {"id": 2}])
    assert get_next_id() == 4

def test_find_task_by_id():
    # Test found and not found

def test_update_task():
    # Test success and not found

def test_delete_task():
    # Test success and not found

def test_backup_tasks(tmp_path):
    os.chdir(tmp_path)
    save_tasks([{"id": 1}])
    backup_path = backup_tasks()
    assert os.path.exists(backup_path)
    assert "todos.backup." in backup_path
```

#### 1.2.5: Write Unit Tests (1 hour)
- [ ] Create `tests/test_storage.py`
- [ ] Set up tmp_path fixture for isolated testing
- [ ] Test load_tasks() with missing file
- [ ] Test load_tasks() with valid file
- [ ] Test load_tasks() with corrupted JSON
- [ ] Test save_tasks() creates file
- [ ] Test save_tasks() atomic behavior (no temp file left)
- [ ] Test save_tasks() pretty printing
- [ ] Test get_next_id() with empty list
- [ ] Test get_next_id() with existing tasks
- [ ] Test get_next_id() with gaps in IDs
- [ ] Test backup_tasks() creates timestamped file
- [ ] Test backup_tasks() with missing source file
- [ ] Test find_task_by_id() found case
- [ ] Test find_task_by_id() not found case
- [ ] Test update_task() success
- [ ] Test update_task() not found
- [ ] Test delete_task() success
- [ ] Test delete_task() not found

- [ ] Run tests: `pytest tests/test_storage.py -v`
- [ ] Check coverage: `pytest tests/test_storage.py --cov=utils.storage --cov-report=term-missing`
- [ ] Verify >90% coverage

**Acceptance Criteria:**
- [ ] All tests pass
- [ ] Coverage >90%
- [ ] Atomic writes verified (no temp files left)
- [ ] All error cases handled
- [ ] No linting errors
- [ ] Type checking passes

---

### Task 1.3: Update `utils/__init__.py`
**Priority:** HIGH
**Estimated Time:** 30 minutes
**Dependencies:** utils/models.py, utils/storage.py

#### 1.3.1: Create Public API (30 min)
- [ ] Open `utils/__init__.py`
- [ ] Add module docstring
- [ ] Import all public APIs from models:
  ```python
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
  ```

- [ ] Import all public APIs from storage:
  ```python
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
  ```

- [ ] Define `__all__` list with all exports

**Test:**
```python
# Test clean imports work
from utils import Task, load_tasks, Priority
```

**Acceptance Criteria:**
- [ ] All public APIs importable from utils package
- [ ] No internal functions exposed
- [ ] `__all__` defines explicit exports
- [ ] Test imports work: `python -c "from utils import Task, load_tasks"`

---

## PHASE 2: Skill Layer

### Task 2.1: Implement `skills/add_skill.py`
**Priority:** HIGH
**Estimated Time:** 2-3 hours
**Dependencies:** utils layer complete
**Specification:** `skills/add_skill.md`

#### Files to Create
- [ ] `skills/add_skill.py`
- [ ] `tests/test_add_skill.py`

#### 2.1.1: Create Structure (30 min)
- [ ] Create file: `touch skills/add_skill.py`
- [ ] Add file docstring
- [ ] Add imports:
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

#### 2.1.2: Implement `add_task()` (1.5 hours)
- [ ] Function signature:
  ```python
  def add_task(
      title: str,
      priority: str = "medium",
      category: str = "general",
      due_date: Optional[str] = None
  ) -> OperationResult:
  ```
- [ ] Add comprehensive docstring (Google style)
- [ ] Main try-except block
- [ ] **Validation phase:**
  - [ ] Validate title using validate_title()
  - [ ] Parse priority using Priority.from_string()
  - [ ] Validate category using validate_category()
  - [ ] Validate due_date if provided using validate_due_date()
- [ ] **Task creation phase:**
  - [ ] Get next ID: `task_id = get_next_id()`
  - [ ] Create timestamp: `created_at = datetime.utcnow().isoformat() + "Z"`
  - [ ] Create Task object with all fields
- [ ] **Persistence phase:**
  - [ ] Load existing tasks: `tasks = load_tasks()`
  - [ ] Convert task to dict: `task_dict = task.to_dict()`
  - [ ] Append to list: `tasks.append(task_dict)`
  - [ ] Save: `save_tasks(tasks)`
- [ ] **Success response:**
  - [ ] Return `OperationResult.success_result(f"Task #{task.id} added successfully", task.to_dict())`
- [ ] **Error handling:**
  - [ ] Catch ValueError → `error_result(str(e), ERROR_CODES["VALIDATION_ERROR"])`
  - [ ] Catch StorageError → `error_result(str(e), ERROR_CODES["STORAGE_ERROR"])`
  - [ ] Catch Exception → `error_result(str(e), "UNKNOWN_ERROR")`

#### 2.1.3: Write Unit Tests (1 hour)
- [ ] Create `tests/test_add_skill.py`
- [ ] Mock storage functions (load_tasks, save_tasks, get_next_id)
- [ ] Test successful addition with minimal params
- [ ] Test with all optional params (priority, category, due_date)
- [ ] Test empty title validation failure
- [ ] Test title too long validation failure
- [ ] Test invalid priority validation failure
- [ ] Test category validation
- [ ] Test due_date validation
- [ ] Test storage error handling (StorageError raised)
- [ ] Verify save_tasks called with correct data
- [ ] Verify task ID generated correctly

**Acceptance Criteria:**
- [ ] Function returns OperationResult in all cases
- [ ] Never raises exceptions (all caught)
- [ ] Success includes task data
- [ ] Error messages are clear and actionable
- [ ] All tests pass
- [ ] Coverage >90%

---

### Task 2.2: Implement `skills/list_skill.py`
**Priority:** HIGH
**Estimated Time:** 3-4 hours
**Dependencies:** utils layer complete
**Specification:** `skills/list_skill.md`

#### Files to Create
- [ ] `skills/list_skill.py`
- [ ] `tests/test_list_skill.py`

#### Implementation Summary
- [ ] Implement helper functions (_filter_tasks, _sort_tasks, _create_rich_table)
- [ ] Implement main list_tasks() function with all filter/sort options
- [ ] Handle table, json, simple output formats
- [ ] Write comprehensive tests for filters, sorting, formats

**Time Estimate:** 3-4 hours

---

### Task 2.3: Implement `skills/update_skill.py`
**Priority:** MEDIUM
**Estimated Time:** 2-3 hours
**Dependencies:** utils layer complete
**Specification:** `skills/update_skill.md`

#### Files to Create
- [ ] `skills/update_skill.py`
- [ ] `tests/test_update_skill.py`

**Time Estimate:** 2-3 hours

---

### Task 2.4: Implement `skills/complete_skill.py`
**Priority:** MEDIUM
**Estimated Time:** 1.5-2 hours
**Dependencies:** utils layer complete
**Specification:** `skills/complete_skill.md`

#### Files to Create
- [ ] `skills/complete_skill.py`
- [ ] `tests/test_complete_skill.py`

**Time Estimate:** 1.5-2 hours

---

### Task 2.5: Implement `skills/delete_skill.py`
**Priority:** MEDIUM
**Estimated Time:** 1.5-2 hours
**Dependencies:** utils layer complete
**Specification:** `skills/delete_skill.md`

#### Files to Create
- [ ] `skills/delete_skill.py`
- [ ] `tests/test_delete_skill.py`

**Time Estimate:** 1.5-2 hours

---

### Task 2.6: Implement `skills/scheduler_skill.py`
**Priority:** LOW
**Estimated Time:** 3-4 hours
**Dependencies:** utils layer complete
**Specification:** `skills/scheduler_skill.md`

#### Files to Create
- [ ] `skills/scheduler_skill.py`
- [ ] `tests/test_scheduler_skill.py`

**Time Estimate:** 3-4 hours

---

## PHASE 3: Integration Layer (CLI)

### Task 3.1: Implement `main.py`
**Priority:** CRITICAL
**Estimated Time:** 5-6 hours
**Dependencies:** All skills implemented
**Specification:** `specs/integration/main-cli-spec.md`

#### Files to Create
- [ ] `main.py`
- [ ] `tests/test_main.py`

#### 3.1.1: Create Structure (30 min)
- [ ] Create `main.py` file: `touch main.py`
- [ ] Add imports (typer, rich, all skills)
- [ ] Initialize typer app
- [ ] Initialize rich Console
- [ ] Define constants (APP_VERSION, etc.)

#### 3.1.2: Implement Helper Functions (30 min)
- [ ] `handle_skill_response(response: OperationResult)`
- [ ] `display_task(task: Dict[str, Any])`

#### 3.1.3: Implement CLI Commands (3-4 hours)
- [ ] Implement `add` command with all options
- [ ] Implement `list` command with filters/sorting
- [ ] Implement `update` command
- [ ] Implement `delete` command with confirmation
- [ ] Implement `complete` command
- [ ] Implement `show` command
- [ ] Implement `schedule` command
- [ ] Implement `overdue` command

#### 3.1.4: Write CLI Tests (1 hour)
- [ ] Use typer.testing.CliRunner
- [ ] Test each command
- [ ] Test help text
- [ ] Test error cases

**Time Estimate:** 5-6 hours

---

### Task 3.2: Configure Entry Point
**Priority:** HIGH
**Estimated Time:** 30 minutes
**Dependencies:** main.py complete

#### 3.2.1: Create `pyproject.toml`
- [ ] Create file: `touch pyproject.toml`
- [ ] Add project metadata:
  ```toml
  [project]
  name = "todo-app"
  version = "1.0.0"
  description = "Phase 1 Console Todo Application"
  requires-python = ">=3.12"
  dependencies = [
      "typer[all]>=0.9.0",
      "rich>=13.0.0",
  ]

  [project.scripts]
  todo = "main:app"

  [build-system]
  requires = ["setuptools>=68.0"]
  build-backend = "setuptools.build_meta"
  ```

#### 3.2.2: Install in Development Mode
- [ ] Run: `pip install -e .`
- [ ] Test: `todo --help` should work
- [ ] Test: `which todo` should show installed location

**Acceptance Criteria:**
- [ ] `todo` command available from shell
- [ ] `todo --help` displays help text
- [ ] All commands accessible

---

## PHASE 4: Testing & Validation

### Task 4.1: Integration Testing
**Estimated Time:** 2-3 hours

#### 4.1.1: Create Integration Tests
- [ ] Create `tests/test_integration.py`
- [ ] Test full workflow: add → list → update → complete → delete
- [ ] Test with empty data
- [ ] Test with populated data
- [ ] Test error scenarios

#### 4.1.2: Run Full Test Suite
- [ ] Run: `pytest -v`
- [ ] Run with coverage: `pytest --cov=. --cov-report=html`
- [ ] Open coverage report: `htmlcov/index.html`
- [ ] Verify coverage >80%

**Acceptance Criteria:**
- [ ] All tests pass
- [ ] Coverage >80%
- [ ] No test failures

---

### Task 4.2: Manual Testing
**Estimated Time:** 1-2 hours

#### Manual Test Checklist
- [ ] Install: `pip install -e .`
- [ ] Test `todo --help`
- [ ] Test `todo add "Buy groceries"`
- [ ] Test `todo list`
- [ ] Test `todo add "Submit report" --priority high --category work`
- [ ] Test `todo list --priority high`
- [ ] Test `todo update 1 --priority high`
- [ ] Test `todo complete 1`
- [ ] Test `todo list --status completed`
- [ ] Test `todo delete 1`
- [ ] Test `todo schedule --upcoming`
- [ ] Test `todo overdue`
- [ ] Test invalid inputs
- [ ] Test colors display correctly in terminal
- [ ] Test table formatting

**Acceptance Criteria:**
- [ ] All commands work as expected
- [ ] Colors and formatting correct
- [ ] Error messages clear
- [ ] No crashes

---

### Task 4.3: Code Quality Checks
**Estimated Time:** 1-2 hours

#### 4.3.1: Run Linters
- [ ] Format code: `black .`
- [ ] Run mypy: `mypy utils/ skills/ main.py`
- [ ] Run pylint: `pylint utils/ skills/ main.py`
- [ ] Fix any issues

#### 4.3.2: Verify Constitution Compliance
- [ ] All functions have type hints ✓
- [ ] All functions have docstrings (Google style) ✓
- [ ] All functions have try-except blocks ✓
- [ ] No circular imports ✓
- [ ] All specs followed exactly ✓

**Acceptance Criteria:**
- [ ] No linting errors
- [ ] Type checking passes
- [ ] Constitution compliant

---

## PHASE 5: Documentation

### Task 5.1: Create User Documentation
**Estimated Time:** 1-2 hours

#### 5.1.1: Update README.md
- [ ] Add project description
- [ ] Add installation instructions
- [ ] Add usage examples
- [ ] Add features list
- [ ] Add development setup
- [ ] Add testing instructions

**Acceptance Criteria:**
- [ ] README complete and accurate
- [ ] Examples work
- [ ] Installation instructions tested

---

## Summary Checklist

### Dependencies Installed
- [ ] Python 3.12+ verified
- [ ] Virtual environment created
- [ ] typer[all] installed
- [ ] rich installed
- [ ] pytest installed
- [ ] pytest-cov installed
- [ ] requirements.txt created

### Files Created (Total: 21 files)
**Utils Layer:**
- [ ] utils/__init__.py
- [ ] utils/models.py
- [ ] utils/storage.py
- [ ] tests/test_models.py
- [ ] tests/test_storage.py

**Skills Layer:**
- [ ] skills/add_skill.py
- [ ] skills/list_skill.py
- [ ] skills/update_skill.py
- [ ] skills/complete_skill.py
- [ ] skills/delete_skill.py
- [ ] skills/scheduler_skill.py
- [ ] tests/test_add_skill.py
- [ ] tests/test_list_skill.py
- [ ] tests/test_update_skill.py
- [ ] tests/test_complete_skill.py
- [ ] tests/test_delete_skill.py
- [ ] tests/test_scheduler_skill.py

**CLI Layer:**
- [ ] main.py
- [ ] pyproject.toml
- [ ] tests/test_main.py
- [ ] tests/test_integration.py

### Testing Complete
- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] Coverage >80%
- [ ] Manual testing complete

### Quality Checks
- [ ] Code formatted (black)
- [ ] Type checking passes (mypy)
- [ ] Linting passes (pylint)
- [ ] Constitution compliant

### Ready to Ship
- [ ] All features working
- [ ] Documentation complete
- [ ] No known bugs
- [ ] Ready for use

---

**Total Files to Create:** 21 Python files + 4 config files
**Total Test Files:** 11
**Total Estimated Time:** 37-52 hours
