# Main CLI Integration Specification

## Overview
The `main.py` file serves as the CLI entry point, using `typer` to create user-facing commands that orchestrate skill functions.

## Purpose
Provide a clean, intuitive command-line interface that routes user commands to appropriate skill implementations while handling errors, formatting output, and managing the application lifecycle.

## File Location
`main.py` (project root)

---

## Architecture Overview

```
User Input (CLI)
      ↓
   main.py (typer app)
      ↓
   Command Handlers
      ↓
   Skill Functions (skills/*.py)
      ↓
   Storage Layer (utils/storage.py)
      ↓
   todos.json
```

---

## Typer Application Setup

### App Initialization
```python
import typer
from rich.console import Console

app = typer.Typer(
    name="todo",
    help="Phase 1 Console Todo Application",
    add_completion=False  # Disable shell completion for Phase 1
)
console = Console()
```

### Application Entry Point
```python
if __name__ == "__main__":
    app()
```

---

## Command Specifications

### 1. `add` - Add New Task

#### Command Signature
```python
@app.command()
def add(
    title: str = typer.Argument(..., help="Task title"),
    priority: str = typer.Option("medium", "--priority", "-p",
                                  help="Priority: high, medium, low"),
    category: str = typer.Option("general", "--category", "-c",
                                  help="Task category"),
    due: Optional[str] = typer.Option(None, "--due", "-d",
                                       help="Due date (YYYY-MM-DD)")
) -> None:
    """Add a new task to your todo list."""
```

#### Implementation Flow
1. Import `add_task()` from `skills.add_skill`
2. Call skill function with parameters
3. Handle response:
   - Success: Display formatted confirmation with task details
   - Error: Display error message in red
4. Exit with appropriate code (0 success, 1 error)

#### Example Output
```
✓ Task #5 added successfully

  Title:    Buy groceries
  Priority: high
  Category: shopping
  Due:      2025-12-30
```

#### CLI Usage
```bash
todo add "Buy groceries"
todo add "Submit report" --priority high --category work
todo add "Pay bills" --due 2025-12-31 -p high
```

---

### 2. `list` - Display Tasks

#### Command Signature
```python
@app.command(name="list")
def list_tasks(
    status: str = typer.Option("all", "--status", "-s",
                                help="Filter by status: pending, in_progress, completed, all"),
    priority: str = typer.Option("all", "--priority", "-p",
                                  help="Filter by priority: high, medium, low, all"),
    category: Optional[str] = typer.Option(None, "--category", "-c",
                                            help="Filter by category"),
    sort_by: str = typer.Option("id", "--sort-by",
                                 help="Sort by: id, title, priority, created_at, due_date"),
    sort_order: str = typer.Option("asc", "--sort-order",
                                    help="Sort order: asc, desc"),
    limit: Optional[int] = typer.Option(None, "--limit", "-n",
                                         help="Limit number of results"),
    format: str = typer.Option("table", "--format", "-f",
                                help="Output format: table, json, simple")
) -> None:
    """List tasks with optional filters and sorting."""
```

#### Implementation Flow
1. Import `list_tasks()` from `skills.list_skill`
2. Build filter dict from options
3. Call skill function
4. Display output using rich library (table/json/simple)
5. Show summary: "Showing X tasks"

#### Example Output (Table Format)
```
┏━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ ID ┃ Title           ┃ Priority ┃ Category ┃ Status    ┃ Due Date   ┃
┡━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━┩
│ 1  │ Buy groceries   │ high     │ shopping │ pending   │ 2025-12-30 │
│ 2  │ Submit report   │ medium   │ work     │ completed │ -          │
└────┴─────────────────┴──────────┴──────────┴───────────┴────────────┘

Showing 2 tasks
```

#### CLI Usage
```bash
todo list
todo list --status pending
todo list --priority high --sort-by due_date
todo list --category work --format json
```

---

### 3. `update` - Modify Task

#### Command Signature
```python
@app.command()
def update(
    task_id: int = typer.Argument(..., help="Task ID to update"),
    title: Optional[str] = typer.Option(None, "--title", "-t",
                                         help="New title"),
    priority: Optional[str] = typer.Option(None, "--priority", "-p",
                                            help="New priority"),
    category: Optional[str] = typer.Option(None, "--category", "-c",
                                            help="New category"),
    status: Optional[str] = typer.Option(None, "--status", "-s",
                                          help="New status"),
    due: Optional[str] = typer.Option(None, "--due", "-d",
                                       help="New due date")
) -> None:
    """Update an existing task."""
```

#### Implementation Flow
1. Validate at least one field provided
2. Import `update_task()` from `skills.update_skill`
3. Build updates dict (only non-None values)
4. Call skill function
5. Display success/error with changes summary

#### Example Output
```
✓ Task #1 updated successfully

Changes:
  Priority: medium → high
  Status:   pending → in_progress
```

#### CLI Usage
```bash
todo update 1 --priority high
todo update 1 --title "New title" --status in_progress
todo update 1 --due 2025-12-31
```

---

### 4. `delete` - Remove Task

#### Command Signature
```python
@app.command()
def delete(
    task_id: int = typer.Argument(..., help="Task ID to delete"),
    force: bool = typer.Option(False, "--force", "-f",
                                help="Skip confirmation prompt")
) -> None:
    """Delete a task by ID."""
```

#### Implementation Flow
1. Import `delete_task()` from `skills.delete_skill`
2. If not force, show task details and confirm
3. Call skill function
4. Display success/error message

#### Confirmation Prompt
```
⚠ Delete task?

  ID:       1
  Title:    Buy groceries
  Status:   completed
  Created:  2025-12-20

This action cannot be undone.
Delete this task? [y/N]:
```

#### CLI Usage
```bash
todo delete 1
todo delete 1 --force
```

---

### 5. `complete` - Mark Task Complete

#### Command Signature
```python
@app.command()
def complete(
    task_id: int = typer.Argument(..., help="Task ID to complete"),
    uncomplete: bool = typer.Option(False, "--uncomplete", "-u",
                                     help="Mark as incomplete instead")
) -> None:
    """Mark a task as completed (or incomplete)."""
```

#### Implementation Flow
1. Import `complete_task()` from `skills.complete_skill`
2. Call skill function with task_id and uncomplete flag
3. Display success message with task details

#### Example Output
```
✓ Task #1 marked as completed
  "Buy groceries"
```

#### CLI Usage
```bash
todo complete 1
todo complete 1 --uncomplete
```

---

### 6. `show` - Display Single Task

#### Command Signature
```python
@app.command()
def show(
    task_id: int = typer.Argument(..., help="Task ID to display")
) -> None:
    """Show detailed information for a specific task."""
```

#### Implementation Flow
1. Import `find_task_by_id()` from `utils.storage`
2. Fetch task
3. Display all fields in formatted output

#### Example Output
```
Task #1

  Title:        Buy groceries
  Priority:     high
  Category:     shopping
  Status:       pending
  Completed:    No
  Created:      2025-12-25 10:30:00
  Updated:      2025-12-25 15:45:00
  Due:          2025-12-30
```

#### CLI Usage
```bash
todo show 1
```

---

### 7. `schedule` - Manage Due Dates

#### Command Signature
```python
@app.command()
def schedule(
    task_id: Optional[int] = typer.Argument(None, help="Task ID to schedule"),
    due: Optional[str] = typer.Option(None, "--due", "-d",
                                       help="Due date"),
    upcoming: bool = typer.Option(False, "--upcoming", "-u",
                                   help="Show upcoming tasks"),
    days: int = typer.Option(7, "--days", "-n",
                              help="Days to look ahead")
) -> None:
    """Manage task due dates and view upcoming tasks."""
```

#### Implementation Flow
1. If `upcoming` flag: show upcoming tasks
2. Else: update task due date
3. Import from `skills.scheduler_skill`

#### CLI Usage
```bash
todo schedule 1 --due 2025-12-31
todo schedule --upcoming
todo schedule --upcoming --days 14
```

---

### 8. `overdue` - Show Overdue Tasks

#### Command Signature
```python
@app.command()
def overdue() -> None:
    """Show all overdue tasks."""
```

#### Implementation Flow
1. Import `get_overdue_tasks()` from `skills.scheduler_skill`
2. Display tasks in red with days overdue
3. Show helpful actions

#### Example Output
```
⚠ You have 2 overdue tasks:

  #1 [HIGH] Buy groceries
     Due: Dec 20 (5 days ago)

  #3 [MED] Submit report
     Due: Dec 23 (2 days ago)
```

#### CLI Usage
```bash
todo overdue
```

---

## Global Options

### Version
```python
@app.callback()
def main(
    version: bool = typer.Option(False, "--version", "-v",
                                  help="Show version and exit")
) -> None:
    """Phase 1 Console Todo Application"""
    if version:
        console.print("Todo App v1.0.0")
        raise typer.Exit()
```

### Help
Automatically provided by typer:
```bash
todo --help
todo add --help
```

---

## Error Handling Strategy

### Skill Function Response Pattern
```python
def handle_skill_response(response: Dict[str, Any]) -> None:
    """Handle standardized skill function responses."""
    if response.get("success"):
        console.print(response.get("message", "Success"), style="green")
    else:
        console.print(f"✗ {response.get('error')}", style="red")
        raise typer.Exit(code=1)
```

### Exception Handling
```python
try:
    result = skill_function(...)
    handle_skill_response(result)
except StorageError as e:
    console.print(f"✗ Storage error: {e}", style="red")
    raise typer.Exit(code=1)
except Exception as e:
    console.print(f"✗ Unexpected error: {e}", style="red")
    raise typer.Exit(code=1)
```

---

## Rich Console Integration

### Color Coding
- **Success**: Green (✓)
- **Error**: Red (✗)
- **Warning**: Yellow (⚠)
- **Info**: Blue (ℹ)

### Formatting Helpers
```python
def format_priority(priority: str) -> str:
    """Return colored priority string."""
    colors = {"high": "red", "medium": "yellow", "low": "green"}
    return f"[{colors.get(priority, 'white')}]{priority}[/]"

def format_date(date_str: Optional[str]) -> str:
    """Format date for display."""
    if not date_str:
        return "-"
    # Parse and format
    return formatted_date
```

---

## Import Structure

```python
# Standard library
import sys
from datetime import datetime
from typing import Optional, Dict, Any, List

# Third-party
import typer
from rich.console import Console
from rich.table import Table

# Local skills
from skills.add_skill import add_task
from skills.list_skill import list_tasks as list_tasks_skill
from skills.update_skill import update_task
from skills.delete_skill import delete_task
from skills.complete_skill import complete_task
from skills.scheduler_skill import (
    get_upcoming_tasks,
    get_overdue_tasks,
    set_due_date
)

# Utilities
from utils.storage import StorageError, find_task_by_id
```

---

## Configuration Constants

```python
APP_NAME = "todo"
APP_VERSION = "1.0.0"
DEFAULT_PRIORITY = "medium"
DEFAULT_CATEGORY = "general"
DEFAULT_STATUS = "pending"
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
```

---

## Testing Strategy

### Unit Tests (`tests/test_main.py`)
Use `typer.testing.CliRunner` to test commands:

```python
from typer.testing import CliRunner
from main import app

runner = CliRunner()

def test_add_command():
    result = runner.invoke(app, ["add", "Test task"])
    assert result.exit_code == 0
    assert "✓" in result.stdout
```

### Integration Tests
1. **test_full_workflow**: Add → List → Update → Complete → Delete
2. **test_error_handling**: Invalid inputs, missing tasks
3. **test_filters**: Complex filter combinations

---

## Command Aliases

### Optional Shortcuts
```python
@app.command(name="ls")
def ls_alias(*args, **kwargs):
    """Alias for 'list' command."""
    return list_tasks(*args, **kwargs)

@app.command(name="rm")
def rm_alias(*args, **kwargs):
    """Alias for 'delete' command."""
    return delete(*args, **kwargs)

@app.command(name="done")
def done_alias(*args, **kwargs):
    """Alias for 'complete' command."""
    return complete(*args, **kwargs)
```

#### Usage
```bash
todo ls              # Same as: todo list
todo rm 1            # Same as: todo delete 1
todo done 1          # Same as: todo complete 1
```

---

## Acceptance Criteria

- [ ] All commands have type hints
- [ ] All commands have help text
- [ ] Typer app properly configured
- [ ] Rich console used for all output
- [ ] Color coding consistent across commands
- [ ] Error messages are clear and actionable
- [ ] Success messages include relevant details
- [ ] All skill functions imported correctly
- [ ] Storage errors handled gracefully
- [ ] Exit codes: 0 (success), 1 (error)
- [ ] Confirmation prompts for destructive actions
- [ ] `--help` works for all commands
- [ ] Optional aliases provided for common commands
- [ ] Unit tests for all commands using CliRunner
- [ ] Integration tests verify end-to-end workflows
