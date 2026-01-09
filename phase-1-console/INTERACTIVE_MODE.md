# Interactive Mode - User Guide

## Overview

The Todo Application has been refactored to provide a **user-friendly interactive mode** with full command names and a continuous loop that keeps running until you exit.

## Running the Application

```bash
# Navigate to project directory
cd /home/tahiraibrahim7/Evolution-of-Todo/phase-1-console

# Run the interactive application
python3 main.py
```

## Features

### 1. Continuous Loop
- The application keeps running until you type `exit`
- No need to restart after each command
- Automatic task list refresh after modifications

### 2. Clear Menu System
Instead of single-letter commands, the app uses intuitive **full command names**:

```
Available Commands:
  add      - Create a new task
  list     - View all tasks
  update   - Edit an existing task
  delete   - Remove a task
  complete - Mark a task as done
  exit     - Close the application
```

### 3. Interactive Workflow

Each command follows a consistent workflow:

1. **Clear screen** (at startup)
2. **Show current task table**
3. **Display menu with available commands**
4. **Prompt**: "What would you like to do?"
5. **Accept full command** (e.g., user types "add" or "delete")
6. **Interactive follow-up** for details
7. **Refresh task list** after modifications

### 4. Rich UI

The application uses the `rich` library for professional-looking interface:
- Colored output and formatted tables
- Bordered panels for menus
- Clear status messages
- Visual feedback for success/errors

## Command Details

### `add` - Create a New Task

**Interactive prompts:**
1. Task title (required)
2. Priority (high/medium/low, default: medium)
3. Category (default: general)
4. Due date (YYYY-MM-DD format, optional)

**Example:**
```
What would you like to do? add

Create New Task
Press Ctrl+C to cancel

Task title: Buy groceries
Priority [medium]: high
Category [general]: personal
Due date (YYYY-MM-DD): 2025-12-30

✓ Task created successfully

Task Details:
  Title:    Buy groceries
  Priority: high
  Category: personal
  Due:      2025-12-30
```

### `list` - View All Tasks

Displays all tasks in a formatted table with:
- ID
- Title
- Priority
- Category
- Status
- Due Date

### `update` - Edit an Existing Task

**Interactive prompts:**
1. Task ID to update
2. New title (leave blank to keep current)
3. New priority (leave blank to keep current)
4. New category (leave blank to keep current)
5. New status (leave blank to keep current)
6. New due date (leave blank to keep current)

**Example:**
```
What would you like to do? update

Update Task
Press Ctrl+C to cancel

Task ID to update: 1

Current task: Buy groceries
Leave blank to keep current value

New title:
New priority (high/medium/low): medium
New category:
New status (pending/in-progress/completed):
New due date (YYYY-MM-DD):

✓ Task updated successfully
```

### `delete` - Remove a Task

**Interactive prompts:**
1. Task ID to delete
2. Confirmation (yes/no)

**Safety features:**
- Shows task details before deletion
- Requires explicit confirmation
- Cannot be undone warning

**Example:**
```
What would you like to do? delete

Delete Task
Press Ctrl+C to cancel

Task ID to delete: 3

⚠ Delete task?
  ID:       3
  Title:    Old task
  Status:   completed

This action cannot be undone.

Delete this task? [no]: yes

✓ Task deleted successfully
```

### `complete` - Mark a Task as Done

**Interactive prompts:**
1. Task ID to complete

**Example:**
```
What would you like to do? complete

Complete Task
Press Ctrl+C to cancel

Task ID to complete: 1

✓ Task marked as completed
```

### `exit` - Close the Application

Gracefully exits the application with a goodbye message.

**Example:**
```
What would you like to do? exit

Goodbye! Your tasks have been saved.
```

## Error Handling

### Invalid Commands
```
What would you like to do? help

Unknown command: 'help'
Please use one of the available commands
```

### Empty Input
```
What would you like to do?

Please enter a command
```

### Keyboard Interrupt (Ctrl+C)
- **During command input**: Shows reminder to use 'exit' command
- **During interactive prompts**: Cancels current operation and returns to menu
- **At main menu**: Shows message about using 'exit' command

### Invalid Task IDs
```
Task ID to update: abc

Invalid task ID. Must be a number.
```

### Non-existent Tasks
```
Task ID to update: 999

Task with ID 999 not found
```

## Tips

1. **Navigation**: Press Enter after typing each command
2. **Cancellation**: Press Ctrl+C during any prompt to cancel the current operation
3. **Defaults**: Press Enter without input to accept default values
4. **Case-insensitive**: Commands work in lowercase (recommended) or uppercase
5. **Task list**: The task list refreshes automatically after add/update/delete/complete operations

## Technical Details

### Implementation Changes

The refactored `main.py` includes:

1. **Removed Typer CLI** - No longer using command-line arguments
2. **Added interactive loop** - `interactive_mode()` function with while loop
3. **Rich Prompt** - Using `rich.prompt.Prompt` for user input
4. **Command handlers** - Separate functions for each command:
   - `handle_add()`
   - `handle_list()`
   - `handle_update()`
   - `handle_delete()`
   - `handle_complete()`
5. **Screen management** - `clear_screen()` for better UX
6. **Menu display** - `show_menu()` with formatted panel

### File Structure
```
main.py
├── Imports (rich, skills, utils)
├── Helper Functions
│   ├── clear_screen()
│   ├── handle_skill_response()
│   ├── display_tasks_table()
│   └── show_menu()
├── Interactive Command Handlers
│   ├── handle_add()
│   ├── handle_list()
│   ├── handle_update()
│   ├── handle_delete()
│   └── handle_complete()
└── Main Loop
    └── interactive_mode()
```

## Keyboard Shortcuts

- **Enter**: Submit input/command
- **Ctrl+C**: Cancel current operation
- Type `exit` and press Enter to quit the application

## Future Enhancements

Potential improvements for the interactive mode:
- [ ] Arrow key navigation
- [ ] Command history
- [ ] Auto-completion
- [ ] Bulk operations
- [ ] Search and filter in interactive mode
- [ ] Task detail view
- [ ] Color themes

## Troubleshooting

### Application won't start
```bash
# Check Python version
python3 --version

# Verify dependencies
python3 -c "import rich; print('Rich library OK')"

# Check syntax
python3 -m py_compile main.py
```

### Rich formatting not working
```bash
# Reinstall rich
pip install --upgrade rich
```

### Clear screen not working
The `clear_screen()` function uses:
- `clear` command on Linux/Mac
- `cls` command on Windows

If it doesn't work, it's a cosmetic issue and won't affect functionality.

## Support

For issues or questions:
1. Check this documentation
2. Verify all dependencies are installed
3. Review error messages carefully
4. Check the task table shows correctly with `list` command

---

**Enjoy your new interactive Todo Application!** 🚀
