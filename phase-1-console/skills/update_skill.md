# Update Task Skill Specification

## Overview
Capability to modify existing task attributes including title, priority, category, status, and due date.

## Purpose
Allow users to update task details as requirements change, without needing to delete and recreate tasks.

## Inputs

### Required
- **task_id** (integer): The ID of the task to update
  - Must exist in storage
  - Must be a positive integer

### Optional (at least one required)
- **title** (string): New task title
  - Min length: 1 character
  - Max length: 200 characters
  - Must not be empty or whitespace-only

- **priority** (enum): New priority level
  - Values: `high`, `medium`, `low`
  - Case-insensitive

- **category** (string): New category
  - Max length: 50 characters

- **status** (enum): New task status
  - Values: `pending`, `in_progress`, `completed`

- **due_date** (ISO 8601 string): New due date
  - Format: `YYYY-MM-DD` or `YYYY-MM-DDTHH:MM:SS`
  - Can be set to `null` to remove due date

- **completed** (boolean): Mark as completed/incomplete
  - Values: `true`, `false`
  - Auto-updates status to `completed` if true

## Processing Logic

1. **Validation**
   - Check task_id exists in storage
   - At least one field to update must be provided
   - Validate each provided field follows constraints
   - Trim whitespace from string fields

2. **Data Retrieval**
   - Fetch existing task from storage via storage-agent
   - Return error if task not found

3. **Update Logic**
   - Create updated task object with modified fields
   - Preserve unchanged fields from original task
   - Update `updated_at` timestamp
   - If `completed` set to true, auto-set status to `completed`
   - If status set to `completed`, auto-set completed to true

4. **Persistence**
   - Delegate to storage-agent for updating task
   - Handle storage errors gracefully

5. **Notification**
   - If due date changed, notify todo-scheduler agent
   - Log update action for audit trail (optional)

## Expected Outputs

### Success Response
```json
{
  "success": true,
  "task": {
    "id": 1,
    "title": "Buy groceries and cook dinner",
    "priority": "high",
    "category": "personal",
    "status": "in_progress",
    "completed": false,
    "created_at": "2025-12-25T10:30:00Z",
    "updated_at": "2025-12-25T15:45:00Z",
    "due_date": "2025-12-26"
  },
  "message": "Task #1 updated successfully",
  "changes": {
    "title": "Changed",
    "priority": "Unchanged",
    "status": "Changed"
  }
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

### Error Response - Validation
```json
{
  "success": false,
  "error": "Invalid priority: superhigh. Must be one of: high, medium, low",
  "code": "VALIDATION_ERROR"
}
```

### Error Response - No Changes
```json
{
  "success": false,
  "error": "No fields to update. Please specify at least one field.",
  "code": "NO_CHANGES"
}
```

## Side Effects
- Task data modified in storage
- `updated_at` timestamp changed
- Scheduler notified if due date changed
- Storage file modified

## Error Scenarios

1. **Task Not Found**: Return 404-style error
2. **No Update Fields**: Error requiring at least one field
3. **Invalid Field Values**: Validation error with details
4. **Storage Failure**: Storage error with retry suggestion
5. **Concurrent Modification**: (Optional) Warn about potential conflicts

## CLI Interface Example
```bash
# Update title
todo update 1 --title "New task description"

# Update priority
todo update 1 --priority high

# Update multiple fields
todo update 1 --title "Updated task" --priority high --category work

# Change status
todo update 1 --status in_progress

# Set due date
todo update 1 --due 2025-12-31

# Remove due date
todo update 1 --due none

# Mark as completed (shorthand)
todo update 1 --completed

# Unmark as completed
todo update 1 --no-completed

# Update by searching (optional enhancement)
todo update "Buy groceries" --priority high
```

## Advanced Features (Optional)

### Bulk Update
Update multiple tasks matching criteria:
```bash
# Update all pending high-priority tasks
todo update --filter "status:pending priority:high" --status in_progress
```

### Interactive Update
```bash
# Launch interactive mode
todo update 1 --interactive

# Prompts:
# Current title: Buy groceries
# New title (or press Enter to skip): Buy groceries and cook
# Current priority: medium
# New priority (high/medium/low or press Enter to skip): high
# ...
```

## Integration Points
- **storage-agent**: Fetch and persist task data
- **todo-scheduler**: Update schedule if due date changes
- **todo-operations**: Core update logic delegation

## Validation Rules

### Field-Specific
- **title**: Non-empty after trimming
- **priority**: One of allowed enum values
- **category**: Max 50 chars, alphanumeric with spaces/hyphens
- **status**: One of allowed enum values
- **due_date**: Valid ISO date, future date preferred
- **completed**: Boolean conversion from various inputs (true/false/yes/no/1/0)

### Business Rules
- Cannot update completed tasks (optional constraint)
- Cannot set due date in the past (warning only)
- Status transitions follow valid flow (optional)

## Acceptance Criteria
- [ ] Task can be updated by ID
- [ ] At least one field must be specified
- [ ] Non-existent task IDs return clear error
- [ ] Invalid field values are rejected with helpful messages
- [ ] Unchanged fields remain preserved
- [ ] updated_at timestamp is set
- [ ] Success message shows what changed
- [ ] Storage is updated atomically
- [ ] Scheduler is notified of due date changes
- [ ] Completed flag auto-updates status and vice versa
