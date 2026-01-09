"""
Delete Task Skill

Capability to permanently remove a task from the system by its ID.
"""

from utils import (
    OperationResult,
    find_task_by_id,
    delete_task as storage_delete_task,
    backup_tasks,
    StorageError,
    ERROR_CODES
)


def delete_task(
    task_id: int,
    force: bool = False
) -> OperationResult:
    """
    Delete a task by ID.

    Args:
        task_id: ID of task to delete
        force: Skip confirmation prompt

    Returns:
        OperationResult with success status
    """
    try:
        # Find task
        task_dict = find_task_by_id(task_id)
        if not task_dict:
            return OperationResult.error_result(
                error=f"Task with ID {task_id} not found",
                code=ERROR_CODES["NOT_FOUND"]
            )

        # If not force, return with confirmation required flag
        if not force:
            return OperationResult(
                success=True,
                message="Confirmation required",
                data={"task": task_dict, "confirmation_required": True}
            )

        # Create backup before deletion
        backup_path = backup_tasks()
        if backup_path:
            print(f"Backup created: {backup_path}")

        # Delete task
        success = storage_delete_task(task_id)

        if success:
            return OperationResult.success_result(
                message=f"Task #{task_id} deleted: \"{task_dict['title']}\"",
                data={"deleted_task": task_dict}
            )
        else:
            return OperationResult.error_result(
                error=f"Failed to delete task #{task_id}",
                code=ERROR_CODES["STORAGE_ERROR"]
            )

    except StorageError as e:
        return OperationResult.error_result(
            error=str(e),
            code=ERROR_CODES["STORAGE_ERROR"]
        )
    except Exception as e:
        return OperationResult.error_result(
            error=f"Unexpected error: {e}",
            code="UNKNOWN_ERROR"
        )
