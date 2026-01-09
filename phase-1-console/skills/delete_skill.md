# Delete Task Skill Specification

## Overview
Capability to permanently remove a task from the system by its ID.

## Purpose
Allow users to delete tasks that are no longer needed, completed long ago, or created by mistake.

## Inputs

### Required
- **task_id** (integer or list): The ID(s) of task(s) to delete
  - Single ID: positive integer
  - Multiple IDs: comma-separated list (e.g., `1,3,5`)
  - Must exist in storage

### Optional
- **force** (boolean): Skip confirmation prompt
  - Default: `false`
  - Useful for scripting/automation

- **completed_only** (boolean): Only delete completed tasks
  - Default: `false`
  - Safety feature to prevent accidental deletion of active tasks

## Processing Logic

1. **Validation**
   - Parse task_id(s) input
   - Validate all IDs are positive integers
   - Check all tasks exist in storage

2. **Confirmation** (if force=false)
   - Display task(s) to be deleted with details
   - Prompt user: "Are you sure you want to delete X task(s)? (y/N)"
   - Abort if user declines

3. **Pre-Delete Checks**
   - If `completed_only` is true, verify all tasks are completed
   - Create backup (optional safety feature)

4. **Deletion**
   - Remove task(s) from storage via storage-agent
   - Handle partial failures for bulk deletes
   - Update task ID sequencing if needed

5. **Cleanup**
   - Notify todo-scheduler to remove scheduled reminders
   - Log deletion for audit trail (optional)

6. **Post-Delete Actions**
   - Return list of successfully deleted task IDs
   - Return list of failed deletions with reasons

## Expected Outputs

### Success Response - Single Delete
```json
{
  "success": true,
  "deleted": [
    {
      "id": 1,
      "title": "Buy groceries",
      "completed": true
    }
  ],
  "message": "Task #1 deleted successfully",
  "count": 1
}
```

### Success Response - Bulk Delete
```json
{
  "success": true,
  "deleted": [
    {"id": 1, "title": "Task 1"},
    {"id": 3, "title": "Task 3"},
    {"id": 5, "title": "Task 5"}
  ],
  "message": "3 tasks deleted successfully",
  "count": 3
}
```

### Partial Success Response
```json
{
  "success": false,
  "deleted": [
    {"id": 1, "title": "Task 1"}
  ],
  "failed": [
    {
      "id": 99,
      "error": "Task not found"
    },
    {
      "id": 2,
      "error": "Task is not completed (use --force to override)"
    }
  ],
  "message": "1 task deleted, 2 failed",
  "count": 1
}
```

### Error Response - Task Not Found
```json
{
  "success": false,
  "error": "Task with ID 99 not found",
  "code": "NOT_FOUND"
}
```

### Error Response - User Cancelled
```json
{
  "success": false,
  "error": "Deletion cancelled by user",
  "code": "CANCELLED"
}
```

### Error Response - Protected Task
```json
{
  "success": false,
  "error": "Cannot delete active task #2 (use --force to override)",
  "code": "PROTECTED"
}
```

## Side Effects
- Task permanently removed from storage
- Storage file modified
- Scheduler updated (reminders removed)
- Backup created (optional)

## Error Scenarios

1. **Task Not Found**: Return 404-style error
2. **Invalid ID Format**: Validation error
3. **Storage Failure**: Storage error with rollback
4. **User Cancellation**: Abort gracefully
5. **Partial Bulk Failure**: Return detailed status for each ID
6. **Protected Task**: Prevent deletion without force flag

## CLI Interface Example
```bash
# Delete single task (with confirmation)
todo delete 1

# Delete single task (force, no confirmation)
todo delete 1 --force

# Delete multiple tasks
todo delete 1,3,5

# Delete with confirmation showing task details
todo delete 1
# Output:
# Task to delete:
#   ID: 1
#   Title: Buy groceries
#   Status: completed
#   Created: 2025-12-20
# Are you sure? (y/N): y
# Task #1 deleted successfully

# Delete all completed tasks
todo delete --completed-only

# Delete by filter (advanced)
todo delete --category shopping --completed-only --force
```

## Confirmation Prompt Design

### Single Task
```
⚠ Delete task?

  ID:       1
  Title:    Buy groceries
  Status:   completed
  Created:  2025-12-20

This action cannot be undone.
Delete this task? (y/N):
```

### Multiple Tasks
```
⚠ Delete 3 tasks?

  #1: Buy groceries (completed)
  #3: Submit report (pending)
  #5: Dentist appointment (completed)

This action cannot be undone.
Delete these tasks? (y/N):
```

## Safety Features

### Soft Delete (Optional Enhancement)
- Move to "trash" instead of immediate deletion
- Auto-purge after 30 days
- Restore command available

### Backup Before Delete
- Create timestamped backup: `todos.backup.YYYYMMDD-HHMMSS.json`
- Keep last N backups
- Restore command available

### Protected Task Types
- Recurring tasks (require --force)
- Tasks with future due dates (warn but allow)
- Tasks in "in_progress" status (require --force)

## Advanced Features (Optional)

### Bulk Delete by Criteria
```bash
# Delete all completed tasks
todo delete --filter "completed:true" --force

# Delete old tasks (completed > 30 days ago)
todo delete --filter "completed:true age:>30d" --force

# Delete by category
todo delete --category "shopping" --completed-only
```

### Interactive Selection
```bash
# Launch interactive mode
todo delete --interactive

# Shows list with checkboxes:
# [ ] 1. Buy groceries (completed)
# [x] 2. Submit report (pending)
# [ ] 3. Dentist appointment (completed)
#
# Press Space to select, Enter to confirm, q to quit
```

### Undo Last Delete (Optional)
```bash
# Restore most recently deleted task
todo undelete

# Restore specific backup
todo restore --backup todos.backup.20251225-153000.json
```

## Integration Points
- **storage-agent**: Fetch and remove task data
- **todo-scheduler**: Remove scheduled reminders/due dates
- **todo-operations**: Core deletion logic delegation

## Acceptance Criteria
- [ ] Task can be deleted by ID
- [ ] Non-existent task IDs return clear error
- [ ] Confirmation prompt shown by default
- [ ] Force flag skips confirmation
- [ ] Multiple tasks can be deleted at once
- [ ] Deleted tasks are removed from storage
- [ ] Success message shows deleted task details
- [ ] Scheduler is notified to clean up reminders
- [ ] Partial failures in bulk delete are reported clearly
- [ ] User cancellation is handled gracefully
- [ ] Completed-only filter works correctly
