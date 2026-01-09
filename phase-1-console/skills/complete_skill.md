# Complete Task Skill Specification

## Overview
Capability to mark a task as completed or toggle its completion status.

## Purpose
Provide a quick, dedicated command for marking tasks as done, separate from the general update operation. This is one of the most common operations in a todo system.

## Inputs

### Required
- **task_id** (integer or list): The ID(s) of task(s) to mark as complete
  - Single ID: positive integer
  - Multiple IDs: comma-separated list (e.g., `1,3,5`)
  - Must exist in storage

### Optional
- **uncomplete** (boolean): Mark task as incomplete instead
  - Default: `false`
  - Allows reopening completed tasks

- **toggle** (boolean): Toggle completion status
  - Default: `false`
  - If task is completed, mark incomplete; if incomplete, mark completed

## Processing Logic

1. **Validation**
   - Parse task_id(s) input
   - Validate all IDs are positive integers
   - Check all tasks exist in storage

2. **Data Retrieval**
   - Fetch task(s) from storage via storage-agent
   - Return error if any task not found

3. **Completion Logic**
   - If `toggle=true`: flip current completion status
   - If `uncomplete=true`: set completed to false
   - Otherwise: set completed to true

4. **Status Update**
   - If marking complete: set status to `completed`
   - If marking incomplete: set status to `pending` (or restore previous status)
   - Set `completed_at` timestamp when completing
   - Clear `completed_at` timestamp when uncompleting

5. **Persistence**
   - Update task(s) via storage-agent
   - Handle partial failures for bulk operations

6. **Notification**
   - Optionally show completion celebration (emoji, message)
   - Update scheduler if task had reminders

## Expected Outputs

### Success Response - Single Complete
```json
{
  "success": true,
  "task": {
    "id": 1,
    "title": "Buy groceries",
    "priority": "high",
    "category": "shopping",
    "status": "completed",
    "completed": true,
    "created_at": "2025-12-25T10:30:00Z",
    "completed_at": "2025-12-25T16:20:00Z",
    "due_date": null
  },
  "message": "✓ Task #1 marked as completed"
}
```

### Success Response - Bulk Complete
```json
{
  "success": true,
  "completed": [
    {"id": 1, "title": "Buy groceries"},
    {"id": 3, "title": "Submit report"},
    {"id": 5, "title": "Call dentist"}
  ],
  "message": "✓ 3 tasks marked as completed",
  "count": 3
}
```

### Success Response - Uncomplete
```json
{
  "success": true,
  "task": {
    "id": 1,
    "title": "Buy groceries",
    "status": "pending",
    "completed": false,
    "completed_at": null
  },
  "message": "Task #1 reopened"
}
```

### Success Response - Toggle
```json
{
  "success": true,
  "task": {
    "id": 1,
    "title": "Buy groceries",
    "completed": true
  },
  "message": "✓ Task #1 toggled to completed"
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

### Partial Success Response
```json
{
  "success": false,
  "completed": [
    {"id": 1, "title": "Task 1"}
  ],
  "failed": [
    {
      "id": 99,
      "error": "Task not found"
    }
  ],
  "message": "1 task completed, 1 failed",
  "count": 1
}
```

## Side Effects
- Task completion status changed in storage
- Task status field updated
- `completed_at` timestamp set/cleared
- Storage file modified
- Scheduler notified (optional)

## Error Scenarios

1. **Task Not Found**: Return 404-style error
2. **Invalid ID Format**: Validation error
3. **Storage Failure**: Storage error with retry suggestion
4. **Already Completed**: Warning message (not error) if task already completed
5. **Partial Bulk Failure**: Return detailed status for each ID

## CLI Interface Example
```bash
# Mark task as complete
todo complete 1

# Mark multiple tasks as complete
todo complete 1,3,5

# Mark as incomplete (reopen)
todo complete 1 --uncomplete
# or
todo uncomplete 1

# Toggle completion status
todo complete 1 --toggle

# Shorthand alias
todo done 1

# Mark all tasks in category as complete (advanced)
todo complete --category shopping --all
```

## Visual Feedback

### Success Message
```
✓ Task #1 marked as completed
  "Buy groceries"
```

### Bulk Success
```
✓ Completed 3 tasks:
  #1: Buy groceries
  #3: Submit report
  #5: Call dentist
```

### Toggle Feedback
```
✓ Task #1 "Buy groceries" → completed
○ Task #2 "Submit report" → reopened
```

### Celebration Mode (Optional)
```
 🎉 Task completed!

  "Buy groceries" ✓

  You have 2 tasks remaining.
```

## Advanced Features (Optional)

### Auto-Archive
- Automatically move to archive after completion
- Clean up from main list

### Completion Stats
```bash
todo complete 1

# Output:
✓ Task #1 completed
📊 Stats:
   - Completed today: 5
   - Completion streak: 7 days
   - Total completed: 127
```

### Recurring Task Handling
```bash
todo complete 5

# Output:
✓ Task #5 "Weekly review" completed
🔄 Created next occurrence: Task #15 (due 2026-01-01)
```

### Batch Operations
```bash
# Complete all pending tasks in category
todo complete --category work --filter "status:pending"

# Complete all tasks due today
todo complete --due today

# Complete all high-priority pending tasks
todo complete --priority high --filter "status:pending"
```

### Undo Complete
```bash
# Undo last completion
todo undo

# Output:
↩ Undid completion of task #1 "Buy groceries"
```

## Integration Points
- **storage-agent**: Fetch and persist task data
- **todo-scheduler**: Update/remove reminders
- **todo-operations**: Core completion logic delegation
- **todo-analytics-agent**: Update completion statistics

## Business Rules

### Completion Timestamp
- Set `completed_at` to current timestamp when completing
- Clear `completed_at` when uncompleting
- Preserve original `created_at`

### Status Transitions
- `pending` → `completed`: allowed
- `in_progress` → `completed`: allowed
- `completed` → `pending`: allowed (when uncompleting)
- Default uncomplete status: `pending`

### Idempotency
- Completing an already-completed task: show info message, don't error
- Uncompleting an already-pending task: show info message, don't error

## Acceptance Criteria
- [ ] Task can be marked complete by ID
- [ ] Non-existent task IDs return clear error
- [ ] Multiple tasks can be completed at once
- [ ] Completion updates status to "completed"
- [ ] completed_at timestamp is set
- [ ] Uncomplete flag reopens tasks
- [ ] Toggle flag switches completion status
- [ ] Success message shows task details
- [ ] Storage is updated atomically
- [ ] Scheduler is notified
- [ ] Bulk operations handle partial failures gracefully
- [ ] Already-completed tasks don't cause errors
- [ ] Visual feedback is clear and positive
