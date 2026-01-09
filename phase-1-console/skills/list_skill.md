# List Tasks Skill Specification

## Overview
Capability to display todos in a formatted table with filtering and sorting options using the `rich` library.

## Purpose
Provide users with a clear, visually organized view of their tasks with ability to filter by status, priority, category, and sort by various criteria.

## Inputs

### Optional Filters
- **status** (enum): Filter by task status
  - Values: `pending`, `in_progress`, `completed`, `all`
  - Default: `all`

- **priority** (enum): Filter by priority level
  - Values: `high`, `medium`, `low`, `all`
  - Default: `all`

- **category** (string): Filter by specific category
  - Default: `all` (show all categories)

- **completed** (boolean): Filter by completion status
  - Values: `true`, `false`, `all`
  - Default: `all`

- **overdue** (boolean): Show only overdue tasks
  - Default: `false`

### Optional Sorting
- **sort_by** (enum): Sort field
  - Values: `id`, `title`, `priority`, `created_at`, `due_date`
  - Default: `id`

- **sort_order** (enum): Sort direction
  - Values: `asc`, `desc`
  - Default: `asc`

### Display Options
- **limit** (integer): Max number of tasks to show
  - Default: `null` (show all)
  - Min: 1

- **format** (enum): Output format
  - Values: `table`, `json`, `simple`
  - Default: `table`

## Processing Logic

1. **Data Retrieval**
   - Fetch all tasks from storage via storage-agent
   - Handle empty task list gracefully

2. **Filtering**
   - Apply status filter if specified
   - Apply priority filter if specified
   - Apply category filter if specified
   - Apply completion filter if specified
   - Check for overdue tasks (current_date > due_date)

3. **Sorting**
   - Sort by specified field and order
   - Handle null values in sort field (push to end)

4. **Formatting**
   - Use `rich.table.Table` for table format
   - Apply color coding:
     - High priority: Red
     - Medium priority: Yellow
     - Low priority: Green
     - Completed tasks: Strikethrough or dim
     - Overdue tasks: Red background or bold red

5. **Pagination** (optional)
   - Apply limit if specified
   - Show count: "Showing X of Y tasks"

## Expected Outputs

### Table Format (using rich)
```
┏━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ ID ┃ Title              ┃ Priority ┃ Category ┃ Status    ┃ Due Date   ┃
┡━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━┩
│ 1  │ Buy groceries      │ high     │ shopping │ pending   │ 2025-12-30 │
│ 2  │ Submit report      │ medium   │ work     │ completed │ -          │
│ 3  │ Dentist appt       │ high     │ health   │ pending   │ 2025-12-28 │
└────┴────────────────────┴──────────┴──────────┴───────────┴────────────┘

Showing 3 tasks
```

### JSON Format
```json
{
  "total": 3,
  "filtered": 3,
  "tasks": [
    {
      "id": 1,
      "title": "Buy groceries",
      "priority": "high",
      "category": "shopping",
      "status": "pending",
      "completed": false,
      "created_at": "2025-12-25T10:30:00Z",
      "due_date": "2025-12-30"
    }
  ]
}
```

### Simple Format
```
1. [HIGH] Buy groceries (shopping) - Due: 2025-12-30
2. [DONE] Submit report (work)
3. [HIGH] Dentist appt (health) - Due: 2025-12-28 ⚠ OVERDUE
```

### Empty List
```
No tasks found.

Use 'todo add "task name"' to create your first task.
```

## Side Effects
None (read-only operation)

## Error Scenarios

1. **Storage Read Failure**: Display error message
2. **Invalid Filter Values**: Return validation error
3. **Corrupted Data**: Skip malformed entries, warn user

## CLI Interface Example
```bash
# List all tasks
todo list

# Filter by status
todo list --status pending

# Filter by priority
todo list --priority high

# Filter by category
todo list --category work

# Combine filters
todo list --status pending --priority high

# Sort by due date
todo list --sort-by due_date --sort-order asc

# Show only overdue
todo list --overdue

# Limit results
todo list --limit 10

# JSON output
todo list --format json

# Show completed tasks
todo list --completed true
```

## Visual Design Requirements

### Rich Table Styling
- **Header**: Bold, centered
- **Borders**: Rounded corners
- **Row Colors**: Alternate subtle background
- **Priority Colors**:
  - High: `[red]` or `[bold red]`
  - Medium: `[yellow]`
  - Low: `[green]`
- **Status Icons**:
  - Pending: `○`
  - In Progress: `◐`
  - Completed: `✓`
- **Overdue Indicator**: `⚠` symbol in red

### Column Specifications
1. **ID**: Right-aligned, width 4
2. **Title**: Left-aligned, width 30, truncate with ellipsis
3. **Priority**: Center-aligned, width 10, colored
4. **Category**: Left-aligned, width 12
5. **Status**: Center-aligned, width 12, with icon
6. **Due Date**: Right-aligned, width 12, highlight if overdue

## Integration Points
- **storage-agent**: Fetch task data
- **todo-scheduler**: Get overdue task information
- **todo-analytics-agent**: May delegate complex filtering logic

## Acceptance Criteria
- [ ] All tasks displayed by default
- [ ] Table uses rich library with colors
- [ ] Filters work independently and in combination
- [ ] Sorting works for all specified fields
- [ ] Overdue tasks are visually highlighted
- [ ] Empty list shows helpful message
- [ ] Completed tasks are visually distinct
- [ ] Priority levels have distinct colors
- [ ] JSON format available for scripting
- [ ] Column widths prevent layout breaking
