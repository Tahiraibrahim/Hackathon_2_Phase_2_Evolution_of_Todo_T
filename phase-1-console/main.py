"""
Phase 1 Console Todo Application

Interactive CLI with user-friendly menu-based interface.
"""

import sys
import os
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich import box

# Import all skill functions
from skills.add_skill import add_task
from skills.list_skill import list_tasks as list_tasks_skill
from skills.update_skill import update_task as update_task_skill
from skills.complete_skill import complete_task as complete_task_skill
from skills.delete_skill import delete_task as delete_task_skill
from skills.scheduler_skill import (
    set_due_date,
    get_upcoming_tasks,
    get_overdue_tasks
)

# Import utilities
from utils import (
    StorageError,
    find_task_by_id,
    Task,
    format_priority,
    format_status,
    format_date_display
)

# Initialize Rich console
console = Console()

# Constants
APP_VERSION = "1.0.0"


# ==================== Helper Functions ====================

def clear_screen():
    """Clear the console screen."""
    os.system('clear' if os.name != 'nt' else 'cls')


def handle_skill_response(response, show_exit: bool = True) -> None:
    """Handle standardized skill function responses."""
    if response.success:
        console.print(f"\n✓ {response.message}", style="bold green")
        if isinstance(response.data, dict) and response.data.get("format") == "table":
            display_tasks_table(response.data.get("tasks", []))
        elif isinstance(response.data, str):
            console.print(response.data)
    else:
        console.print(f"\n✗ {response.error}", style="bold red")

    if show_exit:
        console.print()  # Add blank line for spacing


def display_tasks_table(tasks) -> None:
    """Display tasks in a rich table format."""
    if not tasks:
        console.print("No tasks found.", style="dim")
        return

    table = Table(show_header=True, header_style="bold")
    table.add_column("ID", justify="right", width=4)
    table.add_column("Title", width=30)
    table.add_column("Priority", justify="center", width=10)
    table.add_column("Category", width=12)
    table.add_column("Status", justify="center", width=12)
    table.add_column("Due Date", justify="right", width=12)

    for task in tasks:
        table.add_row(
            str(task.id),
            task.title[:27] + "..." if len(task.title) > 30 else task.title,
            format_priority(task.priority),
            task.category,
            format_status(task.status),
            format_date_display(task.due_date)
        )

    console.print(table)


def show_menu():
    """Display the main menu with available commands."""
    menu_text = """
[bold cyan]Available Commands:[/bold cyan]
  [green]add[/green]      - Create a new task
  [green]list[/green]     - View all tasks
  [green]update[/green]   - Edit an existing task
  [green]delete[/green]   - Remove a task
  [green]complete[/green] - Mark a task as done
  [green]exit[/green]     - Close the application
"""
    console.print(Panel(menu_text, box=box.ROUNDED, border_style="cyan"))


# ==================== Interactive Command Handlers ====================

def handle_add():
    """Interactive handler for adding a new task."""
    console.print("\n[bold cyan]Create New Task[/bold cyan]")
    console.print("[dim]Press Ctrl+C to cancel[/dim]\n")

    try:
        title = Prompt.ask("Task title")
        if not title.strip():
            console.print("[yellow]Task title cannot be empty[/yellow]")
            return

        priority = Prompt.ask(
            "Priority",
            choices=["high", "medium", "low"],
            default="medium"
        )

        category = Prompt.ask("Category", default="general")

        due_input = Prompt.ask(
            "Due date (YYYY-MM-DD)",
            default="",
            show_default=False
        )
        due_date = due_input if due_input.strip() else None

        result = add_task(title, priority, category, due_date)
        handle_skill_response(result)

        if result.success and result.data:
            console.print(f"\n[dim]Task Details:[/dim]")
            console.print(f"  Title:    {result.data['title']}")
            console.print(f"  Priority: {result.data['priority']}")
            console.print(f"  Category: {result.data['category']}")
            if result.data.get('due_date'):
                console.print(f"  Due:      {result.data['due_date']}")

    except KeyboardInterrupt:
        console.print("\n[yellow]Cancelled[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")


def handle_list():
    """Interactive handler for listing tasks."""
    try:
        result = list_tasks_skill(
            status="all",
            priority="all",
            category=None,
            sort_by="id",
            sort_order="asc",
            limit=None,
            output_format="table"
        )
        handle_skill_response(result, show_exit=False)
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")


def handle_update():
    """Interactive handler for updating a task."""
    console.print("\n[bold cyan]Update Task[/bold cyan]")
    console.print("[dim]Press Ctrl+C to cancel[/dim]\n")

    try:
        task_id_str = Prompt.ask("Task ID to update")
        try:
            task_id = int(task_id_str)
        except ValueError:
            console.print("[red]Invalid task ID. Must be a number.[/red]")
            return

        # Check if task exists
        task_dict = find_task_by_id(task_id)
        if not task_dict:
            console.print(f"[red]Task with ID {task_id} not found[/red]")
            return

        console.print(f"\n[dim]Current task: {task_dict['title']}[/dim]")
        console.print("[dim]Leave blank to keep current value[/dim]\n")

        title = Prompt.ask("New title", default="")
        priority = Prompt.ask(
            "New priority (high/medium/low)",
            default=""
        )
        category = Prompt.ask("New category", default="")
        status = Prompt.ask(
            "New status (pending/in-progress/completed)",
            default=""
        )
        due = Prompt.ask("New due date (YYYY-MM-DD)", default="")

        # Convert empty strings to None
        title = title if title.strip() else None
        priority = priority if priority.strip() else None
        category = category if category.strip() else None
        status = status if status.strip() else None
        due = due if due.strip() else None

        result = update_task_skill(task_id, title, priority, category, status, due)
        handle_skill_response(result)

    except KeyboardInterrupt:
        console.print("\n[yellow]Cancelled[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")


def handle_delete():
    """Interactive handler for deleting a task."""
    console.print("\n[bold cyan]Delete Task[/bold cyan]")
    console.print("[dim]Press Ctrl+C to cancel[/dim]\n")

    try:
        task_id_str = Prompt.ask("Task ID to delete")
        try:
            task_id = int(task_id_str)
        except ValueError:
            console.print("[red]Invalid task ID. Must be a number.[/red]")
            return

        # First, get task info for confirmation
        result = delete_task_skill(task_id, force=False)

        if result.success and result.data and result.data.get("confirmation_required"):
            task = result.data["task"]
            console.print("\n[yellow]⚠ Delete task?[/yellow]")
            console.print(f"  ID:       {task['id']}")
            console.print(f"  Title:    {task['title']}")
            console.print(f"  Status:   {task['status']}")
            console.print("\n[dim]This action cannot be undone.[/dim]\n")

            confirm = Prompt.ask(
                "Delete this task?",
                choices=["yes", "no"],
                default="no"
            )

            if confirm.lower() == "yes":
                result = delete_task_skill(task_id, force=True)
                handle_skill_response(result)
            else:
                console.print("[yellow]Cancelled[/yellow]")
        else:
            handle_skill_response(result)

    except KeyboardInterrupt:
        console.print("\n[yellow]Cancelled[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")


def handle_complete():
    """Interactive handler for completing a task."""
    console.print("\n[bold cyan]Complete Task[/bold cyan]")
    console.print("[dim]Press Ctrl+C to cancel[/dim]\n")

    try:
        task_id_str = Prompt.ask("Task ID to complete")
        try:
            task_id = int(task_id_str)
        except ValueError:
            console.print("[red]Invalid task ID. Must be a number.[/red]")
            return

        result = complete_task_skill(task_id, uncomplete=False)
        handle_skill_response(result)

    except KeyboardInterrupt:
        console.print("\n[yellow]Cancelled[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")


# ==================== Main Interactive Loop ====================

def interactive_mode():
    """Run the application in interactive mode."""
    clear_screen()
    console.print(Panel(
        f"[bold cyan]Todo Application v{APP_VERSION}[/bold cyan]\n"
        "[dim]User-Friendly Interactive Mode[/dim]",
        box=box.DOUBLE,
        border_style="cyan"
    ))

    # Show initial task list
    handle_list()

    while True:
        try:
            show_menu()
            command = Prompt.ask(
                "\n[bold]What would you like to do?[/bold]",
                default=""
            ).strip().lower()

            if command == "exit":
                console.print("\n[cyan]Goodbye! Your tasks have been saved.[/cyan]\n")
                break
            elif command == "add":
                handle_add()
                console.print("\n[dim]Refreshing task list...[/dim]")
                handle_list()
            elif command == "list":
                handle_list()
            elif command == "update":
                handle_update()
                console.print("\n[dim]Refreshing task list...[/dim]")
                handle_list()
            elif command == "delete":
                handle_delete()
                console.print("\n[dim]Refreshing task list...[/dim]")
                handle_list()
            elif command == "complete":
                handle_complete()
                console.print("\n[dim]Refreshing task list...[/dim]")
                handle_list()
            elif command == "":
                console.print("[yellow]Please enter a command[/yellow]")
            else:
                console.print(f"[red]Unknown command: '{command}'[/red]")
                console.print("[yellow]Please use one of the available commands[/yellow]")

        except KeyboardInterrupt:
            console.print("\n\n[yellow]Use 'exit' command to quit[/yellow]\n")
        except Exception as e:
            console.print(f"\n[red]Unexpected error: {e}[/red]\n")


if __name__ == "__main__":
    try:
        interactive_mode()
    except KeyboardInterrupt:
        console.print("\n\n[cyan]Application terminated[/cyan]\n")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[red]Fatal error: {e}[/red]\n")
        sys.exit(1)
