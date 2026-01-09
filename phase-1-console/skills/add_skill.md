# Add Task Skill Specification

## Overview
Capability to add a new todo task to the system with customizable attributes.

## Purpose
Allow users to create tasks with structured metadata including title, priority, and category for better organization and tracking.

## Inputs

### Required
- **title** (string): The task description or name
  - Min length: 1 character
  - Max length: 200 characters
  - Must not be empty or whitespace-only

### Optional
- **priority** (enum): Task urgency level
  - Values: `high`, `medium`, `low`
  - Default: `medium`
  - Case-insensitive input accepted

- **category** (string): Task classification/grouping
  - Examples: `work`, `personal`, `shopping`, `health`
  - Default: `general`
  - Max length: 50 characters

- **due_date** (ISO 8601 string): Optional deadline
  - Format: `YYYY-MM-DD` or `YYYY-MM-DDTHH:MM:SS`
  - Must be a future date
  - Default: `null`

## Processing Logic

1. **Validation**
   - Trim whitespace from title
   - Validate title is not empty
   - Normalize priority to lowercase
   - Validate priority is one of allowed values
   - Sanitize category input

2. **Task Creation**
   - Generate unique task ID (auto-increment or UUID)
   - Set creation timestamp (ISO 8601 format)
   - Set initial status as `pending`
   - Set completion status as `false`

3. **Persistence**
   - Delegate to storage-agent for saving to `todos.json`
   - Handle storage errors gracefully

## Expected Outputs

### Success Response
```json
{
  "success": true,
  "task": {
    "id": 1,
    "title": "Buy groceries",
    "priority": "high",
    "category": "shopping",
    "status": "pending",
    "completed": false,
    "created_at": "2025-12-25T10:30:00Z",
    "due_date": null
  },
  "message": "Task added successfully"
}
```

### Error Response
```json
{
  "success": false,
  "error": "Invalid input: title cannot be empty",
  "code": "VALIDATION_ERROR"
}
```

## Side Effects
- New entry added to storage
- Task ID counter incremented
- Storage file modified

## Error Scenarios

1. **Empty Title**: Return validation error
2. **Invalid Priority**: Return validation error with allowed values
3. **Storage Failure**: Return storage error with retry suggestion
4. **Duplicate Detection**: (Optional) Warn if similar task exists

## CLI Interface Example
```bash
# Basic usage
todo add "Buy groceries"

# With priority
todo add "Submit report" --priority high

# With category and priority
todo add "Dentist appointment" --priority high --category health

# With due date
todo add "Pay bills" --due 2025-12-31
```

## Integration Points
- **storage-agent**: Persist task data
- **todo-scheduler**: Handle due date registration if provided

## Acceptance Criteria
- [ ] Task can be created with only a title
- [ ] Priority defaults to medium if not specified
- [ ] Category defaults to general if not specified
- [ ] Invalid priority values are rejected
- [ ] Empty titles are rejected
- [ ] Unique ID is generated for each task
- [ ] Task is persisted to storage
- [ ] Success confirmation is displayed to user
