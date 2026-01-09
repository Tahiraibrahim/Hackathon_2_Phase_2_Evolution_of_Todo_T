# Integration Specifications - Quick Reference

## Overview
This directory contains the integration layer specifications that connect all components of the Phase 1 Console Todo App.

## Specification Files

### 1. [architecture.md](./architecture.md)
**Purpose:** High-level system architecture and integration patterns

**Key Sections:**
- System overview with layer diagrams
- Component responsibilities
- Data flow examples (add/list/update)
- File organization
- Import dependencies
- Error handling strategy
- Testing approach
- Development workflow

**Read this first** to understand how all pieces fit together.

---

### 2. [storage-spec.md](./storage-spec.md)
**Purpose:** Specification for `utils/storage.py` - the data persistence layer

**Core Functions:**
- `load_tasks()` - Load from todos.json
- `save_tasks()` - Atomic write operations
- `get_next_id()` - ID generation
- `backup_tasks()` - Create backups
- `find_task_by_id()` - Retrieve single task
- `update_task()` - Modify task fields
- `delete_task()` - Remove tasks

**Key Features:**
- Atomic writes (temp file + rename)
- Custom `StorageError` exception
- JSON schema validation
- Error handling for all file operations

**Implements:** Layer 3 (Storage Layer)

---

### 3. [models-spec.md](./models-spec.md)
**Purpose:** Specification for `utils/models.py` - data types and validation

**Core Types:**
- `Priority` enum (high/medium/low)
- `Status` enum (pending/in_progress/completed)
- `Task` dataclass (main data structure)
- `TaskFilter` dataclass (for queries)
- `OperationResult` dataclass (standardized responses)

**Utilities:**
- Validation functions (title, category, dates)
- Format functions (colors, icons for rich)
- Constants (error codes, color mappings)
- Factory functions for testing

**Implements:** Layer 4 (Data Models)

---

### 4. [main-cli-spec.md](./main-cli-spec.md)
**Purpose:** Specification for `main.py` - the CLI entry point

**CLI Commands:**
- `add` - Add new task
- `list` - Display tasks with filters
- `update` - Modify task
- `delete` - Remove task
- `complete` - Mark as done
- `show` - Display single task
- `schedule` - Manage due dates
- `overdue` - Show overdue tasks

**Features:**
- Typer app configuration
- Rich console integration
- Command aliases (ls, rm, done)
- Error handling and exit codes
- Confirmation prompts

**Implements:** Layer 1 (CLI Interface)

---

## Implementation Order

### Recommended Sequence:

1. **Start with Models** (`utils/models.py`)
   - No external dependencies
   - Defines types used everywhere
   - Easy to test independently
   - File: [models-spec.md](./models-spec.md)

2. **Then Storage** (`utils/storage.py`)
   - Depends on models for type hints
   - Can be tested with temp files
   - Critical for data integrity
   - File: [storage-spec.md](./storage-spec.md)

3. **Then Skills** (`skills/*.py`)
   - Depends on models and storage
   - Implements business logic
   - Each skill can be done independently
   - Files: `../../skills/*_skill.md`

4. **Finally CLI** (`main.py`)
   - Depends on all skills
   - Ties everything together
   - User-facing interface
   - File: [main-cli-spec.md](./main-cli-spec.md)

---

## Layer Architecture

```
┌─────────────────────────────────────────┐
│  Layer 1: CLI (main.py)                 │  ← User interaction
│  - Command parsing                      │
│  - Output formatting                    │
│  - Error display                        │
└──────────────┬──────────────────────────┘
               │ calls
┌──────────────▼──────────────────────────┐
│  Layer 2: Skills (skills/*.py)          │  ← Business logic
│  - Validation                           │
│  - Coordination                         │
│  - Error handling                       │
└──────────────┬──────────────────────────┘
               │ uses
┌──────────────▼──────────────────────────┐
│  Layer 3: Storage (utils/storage.py)    │  ← Data persistence
│  - CRUD operations                      │
│  - Atomic writes                        │
│  - File I/O                             │
└──────────────┬──────────────────────────┘
               │ uses
┌──────────────▼──────────────────────────┐
│  Layer 4: Models (utils/models.py)      │  ← Type system
│  - Data types                           │
│  - Validation                           │
│  - Constants                            │
└──────────────┬──────────────────────────┘
               │ persists to
        ┌──────▼──────┐
        │ todos.json  │
        └─────────────┘
```

---

## Quick Navigation

### By Use Case:

**I want to understand the system:**
→ Read [architecture.md](./architecture.md)

**I'm implementing storage:**
→ Read [storage-spec.md](./storage-spec.md)

**I'm implementing data models:**
→ Read [models-spec.md](./models-spec.md)

**I'm implementing the CLI:**
→ Read [main-cli-spec.md](./main-cli-spec.md)

**I'm implementing a skill:**
→ Read `../../skills/<skill-name>_skill.md` + [architecture.md](./architecture.md) for integration patterns

---

## Key Concepts

### Atomic Writes
All file writes use temp file + atomic rename to prevent corruption:
```python
write to todos.json.tmp
flush + fsync
os.replace(temp, actual)  # Atomic on POSIX
```

### Standardized Responses
All skill functions return `OperationResult`:
```python
{
    "success": bool,
    "message": str,
    "data": Any,
    "error": Optional[str],
    "error_code": Optional[str]
}
```

### Error Flow
```
Error in Storage → StorageError
  ↓
Caught in Skill → OperationResult.error_result()
  ↓
Received in CLI → Display in red + exit(1)
```

### Type Safety
- All functions have type hints
- Enums for constrained values (Priority, Status)
- Dataclasses for structured data (Task)
- Validation at model layer

---

## Testing Strategy

### Unit Tests
- **Models**: Validation, serialization, enum conversions
- **Storage**: CRUD operations, atomic writes, error handling
- **Skills**: Business logic with mocked storage
- **CLI**: Commands with typer.testing.CliRunner

### Integration Tests
- End-to-end workflows
- Error scenarios
- Filter combinations

### Test Files
```
tests/
├── test_models.py      # Layer 4
├── test_storage.py     # Layer 3
├── test_*_skill.py     # Layer 2
└── test_main.py        # Layer 1
```

---

## Common Patterns

### Adding a New Command

1. Define skill function in `skills/<name>_skill.py`
2. Add command in `main.py`:
   ```python
   @app.command()
   def command_name(...) -> None:
       result = skill_function(...)
       handle_skill_response(result)
   ```
3. Write tests in `tests/test_<name>_skill.py`
4. Update this documentation

### Handling Errors

**In Skills:**
```python
try:
    # business logic
    return OperationResult.success_result(...)
except StorageError as e:
    return OperationResult.error_result(str(e), "STORAGE_ERROR")
except ValueError as e:
    return OperationResult.error_result(str(e), "VALIDATION_ERROR")
```

**In CLI:**
```python
result = skill_function(...)
if result.success:
    console.print(result.message, style="green")
else:
    console.print(f"✗ {result.error}", style="red")
    raise typer.Exit(code=1)
```

---

## Related Documents

- **Constitution**: `../../.specify/memory/constitution.md` - Project principles
- **Skill Specs**: `../../skills/*.md` - Individual feature specifications
- **README**: `../../README.md` - Project overview and setup

---

## Version History

| Version | Date | Description |
|---------|------|-------------|
| 1.0.0 | 2025-12-25 | Initial integration specifications |

---

## Questions?

If anything is unclear:
1. Check [architecture.md](./architecture.md) for high-level overview
2. Check specific spec files for detailed interfaces
3. Refer to constitution for guiding principles
4. Look at skill specs for business requirements
