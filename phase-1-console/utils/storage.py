"""
Storage layer for Todo App.

Provides atomic, reliable file I/O operations for the todos.json data store.
All file system operations are centralized here to ensure data integrity
and consistent error handling.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional


# ==================== Custom Exception ====================

class StorageError(Exception):
    """Raised when storage operations fail."""
    pass


# ==================== Constants ====================

TODOS_FILE = "todos.json"
BACKUP_PREFIX = "todos.backup"
DEFAULT_PRIORITY = "medium"
DEFAULT_CATEGORY = "general"
DEFAULT_STATUS = "pending"


# ==================== Core Storage Functions ====================

def load_tasks() -> List[Dict[str, Any]]:
    """
    Load all tasks from todos.json file.

    Returns:
        List of task dictionaries. Returns empty list if file doesn't exist.

    Raises:
        StorageError: If file is corrupted or cannot be read.
    """
    try:
        if not os.path.exists(TODOS_FILE):
            return []

        with open(TODOS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Validate structure
        if not isinstance(data, list):
            raise StorageError(f"Corrupted {TODOS_FILE}: expected list, got {type(data).__name__}")

        return data

    except FileNotFoundError:
        return []
    except json.JSONDecodeError as e:
        raise StorageError(f"Corrupted {TODOS_FILE}: {e}")
    except PermissionError:
        raise StorageError(f"Permission denied reading {TODOS_FILE}")
    except Exception as e:
        raise StorageError(f"Failed to load tasks: {e}")


def save_tasks(tasks: List[Dict[str, Any]]) -> bool:
    """
    Save tasks to todos.json using atomic write operation.

    Args:
        tasks: Complete list of tasks to save.

    Returns:
        True on success.

    Raises:
        StorageError: If save operation fails.
    """
    temp_file = f"{TODOS_FILE}.tmp"

    try:
        # Validate input
        if not isinstance(tasks, list):
            raise StorageError(f"Invalid input: expected list, got {type(tasks).__name__}")

        # Write to temporary file
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, indent=2, ensure_ascii=False)
            f.flush()
            os.fsync(f.fileno())  # Force write to disk

        # Atomic rename
        os.replace(temp_file, TODOS_FILE)
        return True

    except PermissionError:
        raise StorageError(f"Permission denied writing {TODOS_FILE}")
    except OSError as e:
        raise StorageError(f"Disk error: {e}")
    except Exception as e:
        raise StorageError(f"Failed to save tasks: {e}")
    finally:
        # Clean up temp file if it exists
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except:
                pass  # Best effort cleanup


def get_next_id() -> int:
    """
    Generate the next available task ID.

    Returns:
        Next ID (max current ID + 1, or 1 if no tasks).

    Raises:
        StorageError: If tasks cannot be loaded.
    """
    try:
        tasks = load_tasks()
        if not tasks:
            return 1

        max_id = max(task.get('id', 0) for task in tasks)
        return max_id + 1

    except Exception as e:
        raise StorageError(f"Failed to generate next ID: {e}")


def backup_tasks() -> str:
    """
    Create a timestamped backup of todos.json.

    Returns:
        Path to backup file, or empty string if source doesn't exist.
    """
    try:
        if not os.path.exists(TODOS_FILE):
            return ""

        # Generate timestamp
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_path = f"{BACKUP_PREFIX}.{timestamp}.json"

        # Copy file
        with open(TODOS_FILE, 'r', encoding='utf-8') as src:
            content = src.read()

        with open(backup_path, 'w', encoding='utf-8') as dst:
            dst.write(content)

        return backup_path

    except Exception as e:
        # Log warning but don't fail operation
        print(f"Warning: Could not create backup: {e}")
        return ""


def find_task_by_id(task_id: int) -> Optional[Dict[str, Any]]:
    """
    Retrieve a single task by ID.

    Args:
        task_id: The task ID to find.

    Returns:
        Task dictionary if found, None if not found.

    Raises:
        StorageError: If tasks cannot be loaded.
    """
    try:
        tasks = load_tasks()
        for task in tasks:
            if task.get('id') == task_id:
                return task
        return None

    except Exception as e:
        raise StorageError(f"Failed to find task: {e}")


def update_task(task_id: int, updates: Dict[str, Any]) -> bool:
    """
    Update specific fields of a task.

    Args:
        task_id: ID of task to update.
        updates: Fields to update.

    Returns:
        True if updated, False if task not found.

    Raises:
        StorageError: If update operation fails.
    """
    try:
        tasks = load_tasks()

        # Find task
        task_found = False
        for task in tasks:
            if task.get('id') == task_id:
                task_found = True
                # Update fields
                for key, value in updates.items():
                    task[key] = value
                # Set updated_at timestamp
                task['updated_at'] = datetime.utcnow().isoformat() + "Z"
                break

        if not task_found:
            return False

        # Save updated tasks
        save_tasks(tasks)
        return True

    except Exception as e:
        raise StorageError(f"Failed to update task: {e}")


def delete_task(task_id: int) -> bool:
    """
    Remove a task by ID.

    Args:
        task_id: ID of task to delete.

    Returns:
        True if deleted, False if task not found.

    Raises:
        StorageError: If delete operation fails.
    """
    try:
        tasks = load_tasks()
        original_length = len(tasks)

        # Filter out task with matching ID
        filtered_tasks = [task for task in tasks if task.get('id') != task_id]

        # Check if anything was removed
        if len(filtered_tasks) == original_length:
            return False

        # Save filtered list
        save_tasks(filtered_tasks)
        return True

    except Exception as e:
        raise StorageError(f"Failed to delete task: {e}")
