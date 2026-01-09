# Phase 1 Console Todo App - Integration Architecture

## Document Purpose
This document defines how all components of the Phase 1 Console Todo App integrate together: CLI commands, skill implementations, storage layer, and data models.

## System Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         User (CLI)                          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                     main.py (Typer App)                     │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────┐  │
│  │   add    │   list   │  update  │  delete  │ complete │  │
│  └──────────┴──────────┴──────────┴──────────┴──────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Skill Layer (skills/)                    │
│  ┌────────────┬────────────┬────────────┬────────────────┐  │
│  │ add_skill  │ list_skill │update_skill│  complete_...  │  │
│  └────────────┴────────────┴────────────┴────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   Utility Layer (utils/)                    │
│  ┌──────────────────────┬───────────────────────────────┐   │
│  │   storage.py         │         models.py             │   │
│  │ (File I/O, CRUD)     │  (Types, Enums, Validation)   │   │
│  └──────────────────────┴───────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
                  ┌─────────────┐
                  │ todos.json  │
                  └─────────────┘
```

---

## Component Responsibilities

### Layer 1: CLI Interface (`main.py`)
**Responsibilities:**
- Parse command-line arguments using typer
- Route commands to appropriate skill functions
- Format output using rich library
- Handle user confirmations and prompts
- Display errors in user-friendly format
- Manage application lifecycle (exit codes)

**Does NOT:**
- Perform business logic
- Access storage directly
- Validate data (beyond CLI argument parsing)

---

### Layer 2: Skill Implementations (`skills/*.py`)
**Responsibilities:**
- Implement business logic per specification
- Validate inputs according to skill spec
- Coordinate between storage and models
- Return standardized OperationResult objects
- Handle skill-specific error scenarios

**Does NOT:**
- Handle CLI argument parsing
- Format output for display (returns data)
- Implement storage operations directly

---

### Layer 3: Storage Layer (`utils/storage.py`)
**Responsibilities:**
- Read/write todos.json atomically
- Generate unique task IDs
- Provide CRUD operations (find, update, delete)
- Create backups before destructive operations
- Handle file system errors

**Does NOT:**
- Validate business logic
- Format data for display
- Implement skill-specific behavior

---

### Layer 4: Data Models (`utils/models.py`)
**Responsibilities:**
- Define type-safe data structures (Task, enums)
- Validate data constraints (title length, etc.)
- Provide serialization (to_dict/from_dict)
- Define constants and error codes
- Format data for rich output (colors, icons)

**Does NOT:**
- Perform I/O operations
- Implement business logic
- Handle CLI concerns

---

## Data Flow Examples

### Example 1: Adding a Task

```
1. User runs: todo add "Buy groceries" --priority high --category shopping

2. main.py:add() receives arguments:
   - title="Buy groceries"
   - priority="high"
   - category="shopping"

3. main.py calls: add_task(title, priority, category)

4. skills/add_skill.py:add_task():
   a. Validates title using validate_title()
   b. Converts priority string to Priority enum
   c. Creates Task object with generated ID
   d. Calls storage.load_tasks() to get existing tasks
   e. Appends new task dict to list
   f. Calls storage.save_tasks() to persist
   g. Returns OperationResult with success and task data

5. main.py receives OperationResult:
   - Checks result.success
   - If success: displays formatted success message with task details
   - If error: displays error in red and exits with code 1

6. User sees:
   ✓ Task #5 added successfully
     Title:    Buy groceries
     Priority: high
     Category: shopping
```

### Example 2: Listing Tasks with Filters

```
1. User runs: todo list --status pending --priority high

2. main.py:list_tasks() receives:
   - status="pending"
   - priority="high"
   - (other filters at defaults)

3. main.py calls: list_tasks_skill(filters)

4. skills/list_skill.py:list_tasks():
   a. Calls storage.load_tasks() to get all tasks
   b. Converts dicts to Task objects
   c. Creates TaskFilter with specified criteria
   d. Filters tasks using TaskFilter.matches()
   e. Sorts tasks by specified field
   f. Returns OperationResult with filtered task list

5. main.py receives task list:
   - Creates rich Table
   - Iterates through tasks
   - Adds rows with color-coded priorities
   - Displays table
   - Shows count summary

6. User sees formatted table with filtered results
```

### Example 3: Updating a Task

```
1. User runs: todo update 5 --priority high --status in_progress

2. main.py:update() receives:
   - task_id=5
   - priority="high"
   - status="in_progress"

3. main.py builds updates dict:
   updates = {"priority": "high", "status": "in_progress"}

4. main.py calls: update_task(task_id, updates)

5. skills/update_skill.py:update_task():
   a. Calls storage.find_task_by_id(5)
   b. If not found, returns error OperationResult
   c. Converts update values to proper types (enums)
   d. Creates Task object from existing data
   e. Calls task.update_fields(**updates)
   f. Calls storage.update_task() to persist
   g. Returns success OperationResult with updated task

6. main.py displays:
   ✓ Task #5 updated successfully
   Changes:
     Priority: medium → high
     Status:   pending → in_progress
```

---

## File Organization

```
phase-1-console/
│
├── main.py                          # CLI entry point (Layer 1)
│
├── skills/                          # Skill specifications & implementations (Layer 2)
│   ├── add_skill.md                # Spec: Add task
│   ├── add_skill.py                # Impl: Add task
│   ├── list_skill.md
│   ├── list_skill.py
│   ├── update_skill.md
│   ├── update_skill.py
│   ├── delete_skill.md
│   ├── delete_skill.py
│   ├── complete_skill.md
│   ├── complete_skill.py
│   ├── scheduler_skill.md
│   └── scheduler_skill.py
│
├── utils/                           # Utility layer (Layers 3 & 4)
│   ├── __init__.py                 # Public API exports
│   ├── storage.py                  # Storage operations (Layer 3)
│   └── models.py                   # Data models, types (Layer 4)
│
├── tests/                           # Test files mirror structure
│   ├── test_main.py
│   ├── test_add_skill.py
│   ├── test_list_skill.py
│   ├── test_storage.py
│   └── test_models.py
│
├── specs/                           # Integration specifications
│   └── integration/
│       ├── storage-spec.md
│       ├── main-cli-spec.md
│       ├── models-spec.md
│       └── architecture.md         # This document
│
├── todos.json                       # Data file (gitignored)
├── pyproject.toml                   # Dependencies
├── README.md                        # Project documentation
└── .specify/                        # Spec-driven development artifacts
    └── memory/
        └── constitution.md          # Project constitution
```

---

## Import Dependencies

### Dependency Graph
```
main.py
  ↓ imports
skills/*.py
  ↓ imports
utils/models.py  ←──┐
  ↓ imports         │
utils/storage.py  ──┘ (can import models for type hints)
```

### Rules
1. **No circular imports**: Storage can import models, but models cannot import storage
2. **Upward dependencies**: Lower layers (utils) never import from upper layers (skills, main)
3. **Skill independence**: Skills don't import from each other
4. **Explicit over implicit**: Always use explicit imports, not `import *`

---

## Skill Function Signatures

All skill functions follow a consistent pattern:

### Input Parameters
- Use primitive types (str, int, bool) or model types (Priority, Status)
- Required parameters first, optional with defaults
- Use type hints for all parameters

### Return Type
- Always return `OperationResult` or `Dict[str, Any]`
- Include `success` boolean
- Include `message` for user display
- Include `data` for operation output
- Include `error` and `error_code` on failure

### Error Handling
- Catch all exceptions within skill function
- Never let exceptions bubble to CLI layer
- Return error OperationResult with details

### Example Signature
```python
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
        priority: Priority level (high/medium/low)
        category: Task category
        due_date: Optional due date (ISO 8601)

    Returns:
        OperationResult with success status and task data
    """
    try:
        # Implementation
        return OperationResult.success_result(...)
    except Exception as e:
        return OperationResult.error_result(...)
```

---

## Error Handling Strategy

### Error Flow

```
Error occurs in:
  Storage Layer → Raises StorageError
        ↓
  Skill Layer → Catches, wraps in OperationResult.error_result()
        ↓
  CLI Layer → Displays formatted error, exits with code 1
```

### Error Types

| Layer | Error Type | Handling |
|-------|-----------|----------|
| Storage | `StorageError` | Raised for file I/O issues |
| Models | `ValueError` | Raised for validation failures |
| Skills | None (returns OperationResult) | Catch all, return error result |
| CLI | None | Display errors, manage exit codes |

### Error Response Format
```python
{
    "success": False,
    "message": "Operation failed: Title cannot be empty",
    "error": "Title cannot be empty",
    "error_code": "VALIDATION_ERROR",
    "data": None
}
```

---

## Testing Strategy

### Unit Tests
- **Storage**: Test CRUD operations, atomic writes, error handling
- **Models**: Test validation, serialization, enum conversions
- **Skills**: Test business logic with mocked storage
- **CLI**: Test commands with typer.testing.CliRunner

### Integration Tests
- **End-to-end workflows**: Add → List → Update → Complete → Delete
- **Error scenarios**: Invalid inputs, missing files, corrupted data
- **Filter combinations**: Complex queries across multiple criteria

### Test Data
- Use factory functions from models.py
- Mock storage layer in skill tests
- Use temp directories for integration tests

---

## Configuration Management

### Constants Location
- **Storage paths**: `utils/storage.py`
- **Data formats**: `utils/models.py`
- **CLI defaults**: `main.py`
- **Validation limits**: `utils/models.py`

### Environment Variables (Future)
- `TODO_DATA_DIR`: Custom data directory
- `TODO_DATE_FORMAT`: Preferred date format
- `TODO_COLOR_SCHEME`: Color theme

---

## Performance Considerations

### Current Scale (Phase 1)
- Target: Up to 1000 tasks
- File size: < 1MB JSON
- Load time: < 100ms

### Optimization Opportunities
1. **Caching**: In-memory cache for repeated reads
2. **Lazy loading**: Load tasks only when needed
3. **Partial updates**: Update specific fields without full rewrite
4. **Indexing**: Add ID index for faster lookups (Phase 2)

---

## Security Considerations

### Phase 1 Security
- No authentication required (local single-user)
- No sensitive data stored
- File permissions: User read/write only
- No network access

### Input Validation
- Title length limits prevent DoS
- Category length limits
- Date format validation prevents injection
- No eval() or exec() usage

---

## Future Extensions (Phase 2+)

### Database Migration
- SQLite for better performance at scale
- Migration script: JSON → SQLite
- Backward compatibility for JSON format

### Multi-User Support
- User authentication
- Task ownership
- Shared task lists
- Conflict resolution

### Advanced Features
- Natural language date parsing
- Recurring tasks
- Reminders and notifications
- Task attachments
- Search with full-text indexing

---

## Development Workflow

### Adding a New Skill

1. **Create specification**: `skills/<name>_skill.md`
2. **Define function signature**: Follow skill signature pattern
3. **Implement skill**: `skills/<name>_skill.py`
4. **Add CLI command**: Update `main.py` with new command
5. **Write tests**: `tests/test_<name>_skill.py`
6. **Update integration docs**: Add to this architecture document

### Modifying Existing Components

1. **Update spec first**: Modify `.md` specification
2. **Update implementation**: Follow spec changes
3. **Update tests**: Reflect new behavior
4. **Run full test suite**: Ensure no regressions
5. **Update architecture docs**: If integration changes

---

## Acceptance Criteria

### Integration Layer
- [ ] All skills import from utils correctly
- [ ] No circular dependencies exist
- [ ] All skill functions return OperationResult
- [ ] CLI commands handle all skill responses
- [ ] Storage layer used by all skills
- [ ] Models used consistently across layers

### Error Handling
- [ ] All errors wrapped in OperationResult
- [ ] StorageError raised for I/O failures
- [ ] ValueError raised for validation failures
- [ ] CLI displays all errors clearly
- [ ] Exit codes: 0 (success), 1 (error)

### Testing
- [ ] Unit tests for each layer
- [ ] Integration tests for workflows
- [ ] Test coverage > 80%
- [ ] All tests pass

### Documentation
- [ ] All functions have docstrings
- [ ] All specifications up to date
- [ ] Architecture document complete
- [ ] README includes setup instructions

---

## Quick Reference

### Adding a Task (Code Flow)
```
CLI: todo add "title" --priority high
  → main.py:add()
    → skills/add_skill.py:add_task()
      → utils/models.py:validate_title()
      → utils/models.py:Task(...)
      → utils/storage.py:load_tasks()
      → utils/storage.py:save_tasks()
    ← OperationResult
  ← Display formatted output
```

### Listing Tasks (Code Flow)
```
CLI: todo list --priority high
  → main.py:list_tasks()
    → skills/list_skill.py:list_tasks()
      → utils/storage.py:load_tasks()
      → utils/models.py:TaskFilter.matches()
    ← OperationResult with task list
  ← Rich table display
```

### Error Handling (Code Flow)
```
Error in storage.py
  → Raises StorageError
Caught in skill function
  → Returns OperationResult.error_result()
Received in main.py
  → Display error in red
  → Exit with code 1
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-25 | Initial architecture specification |
