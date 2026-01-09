# Scheduler Skill Specification

## Overview
Capability to manage time-sensitive aspects of tasks including due dates, reminders, recurring tasks, and overdue detection.

## Purpose
Provide temporal intelligence to the todo system, helping users stay on top of deadlines and maintain regular habits through scheduled tasks and proactive notifications.

## Core Capabilities

### 1. Due Date Management
### 2. Reminder System
### 3. Recurring Tasks
### 4. Overdue Detection
### 5. Upcoming Task Alerts

---

## 1. Due Date Management

### Inputs
- **task_id** (integer): Task to set due date for
- **due_date** (string): Due date in natural or ISO format
  - Natural: `today`, `tomorrow`, `next monday`, `in 3 days`, `2025-12-31`
  - ISO 8601: `2025-12-31T23:59:59Z`
  - Time optional: defaults to end of day (23:59:59)

- **due_time** (string): Optional time component
  - Format: `HH:MM` or `HH:MM:SS`
  - Examples: `14:30`, `9:00 AM`

### Processing Logic
1. Parse natural language date/time
2. Convert to ISO 8601 format
3. Validate date is in the future (warn if past)
4. Store with task via storage-agent
5. Register in scheduler's internal calendar

### Outputs
```json
{
  "success": true,
  "task_id": 1,
  "due_date": "2025-12-31T23:59:59Z",
  "human_readable": "December 31, 2025 at 11:59 PM",
  "days_until": 6,
  "message": "Due date set for task #1"
}
```

---

## 2. Reminder System

### Inputs
- **task_id** (integer): Task to set reminder for
- **remind_at** (string): When to send reminder
  - Relative to due date: `1 day before`, `2 hours before`, `at due time`
  - Absolute: `2025-12-30T10:00:00Z`, `tomorrow at 9am`

- **reminder_type** (enum): How to deliver reminder
  - Values: `console`, `notification`, `email` (future)
  - Default: `console`

- **repeat** (boolean): Repeat reminder if not completed
  - Default: `false`
  - Interval: every 1 hour until completed

### Processing Logic
1. Calculate reminder timestamp
2. Store reminder configuration with task
3. Register reminder in scheduler queue
4. At reminder time:
   - Check if task still pending
   - Display notification via configured method
   - If repeat enabled, reschedule next reminder

### Outputs

#### Setting Reminder
```json
{
  "success": true,
  "task_id": 1,
  "reminder_at": "2025-12-30T10:00:00Z",
  "message": "Reminder set for 1 day before due date"
}
```

#### Reminder Notification
```
🔔 REMINDER

Task #1: Buy groceries
Due: Tomorrow at 11:59 PM (in 1 day)
Priority: high

View: todo show 1
Complete: todo complete 1
```

---

## 3. Recurring Tasks

### Inputs
- **task_id** (integer): Template task for recurrence
- **recurrence_pattern** (string): How often to repeat
  - Simple: `daily`, `weekly`, `monthly`, `yearly`
  - Specific: `every monday`, `every 2 weeks`, `every 1st of month`
  - Custom: `every weekday`, `every monday,wednesday,friday`

- **recurrence_end** (string): When to stop recurring
  - Date: `2026-12-31`
  - Count: `after 10 occurrences`
  - Never: `never` or `null`

- **auto_create** (boolean): Create next occurrence when completed
  - Default: `true`
  - If false, require manual creation

### Processing Logic
1. Parse recurrence pattern
2. Calculate next occurrence date
3. Store pattern with task metadata
4. On task completion:
   - If auto_create enabled, create next occurrence
   - Calculate due date based on pattern
   - Copy task details (title, priority, category)
   - Reset status to pending

### Outputs

#### Setting Recurrence
```json
{
  "success": true,
  "task_id": 1,
  "recurrence": "weekly",
  "next_occurrence": "2026-01-01T00:00:00Z",
  "message": "Task will recur every week"
}
```

#### After Completion
```json
{
  "success": true,
  "completed_task_id": 1,
  "new_task_id": 15,
  "new_due_date": "2026-01-01T00:00:00Z",
  "message": "✓ Task completed. Next occurrence created as task #15"
}
```

### Recurrence Patterns

#### Simple Patterns
- `daily` - Every day at same time
- `weekly` - Every week on same day
- `monthly` - Every month on same date
- `yearly` - Every year on same date

#### Specific Patterns
- `every monday` - Weekly on Mondays
- `every 2 weeks` - Bi-weekly
- `every 15th` - Monthly on 15th day
- `every 1st monday` - First Monday of each month

#### Advanced Patterns
- `every weekday` - Monday through Friday
- `every weekend` - Saturday and Sunday
- `every monday,friday` - Specific days of week
- `every quarter` - Every 3 months

---

## 4. Overdue Detection

### Inputs
None (runs automatically or on-demand)

### Processing Logic
1. Fetch all tasks with due dates
2. Compare due_date with current time
3. Filter tasks where:
   - `due_date < current_time`
   - `completed = false`
4. Sort by priority and overdue duration
5. Return overdue task list

### Outputs

#### Overdue Task List
```json
{
  "success": true,
  "overdue_count": 3,
  "tasks": [
    {
      "id": 1,
      "title": "Buy groceries",
      "priority": "high",
      "due_date": "2025-12-20T23:59:59Z",
      "days_overdue": 5,
      "status": "pending"
    },
    {
      "id": 3,
      "title": "Submit report",
      "priority": "medium",
      "due_date": "2025-12-23T17:00:00Z",
      "hours_overdue": 50,
      "status": "in_progress"
    }
  ]
}
```

#### Console Display
```
⚠ You have 3 overdue tasks:

  #1 [HIGH] Buy groceries
     Due: Dec 20 (5 days ago)

  #3 [MED] Submit report
     Due: Dec 23 at 5:00 PM (2 days ago)

  #7 [LOW] Review notes
     Due: Dec 24 (1 day ago)

View details: todo show <id>
Complete: todo complete <id>
Reschedule: todo update <id> --due <new-date>
```

---

## 5. Upcoming Task Alerts

### Inputs
- **lookahead_days** (integer): How many days to look ahead
  - Default: 7
  - Range: 1-30

- **priority_filter** (enum): Filter by priority
  - Values: `all`, `high`, `medium`, `low`
  - Default: `all`

### Processing Logic
1. Fetch tasks with due dates
2. Filter where:
   - `due_date > current_time`
   - `due_date <= current_time + lookahead_days`
   - `completed = false`
3. Group by date
4. Sort by due date, then priority

### Outputs
```json
{
  "success": true,
  "upcoming_count": 5,
  "date_range": "2025-12-25 to 2026-01-01",
  "tasks_by_date": {
    "2025-12-26": [
      {
        "id": 2,
        "title": "Dentist appointment",
        "priority": "high",
        "due_time": "14:00"
      }
    ],
    "2025-12-28": [
      {
        "id": 4,
        "title": "Submit expense report",
        "priority": "medium"
      }
    ]
  }
}
```

---

## CLI Interface Examples

### Due Dates
```bash
# Set due date
todo schedule 1 --due tomorrow
todo schedule 1 --due "next monday at 2pm"
todo schedule 1 --due 2025-12-31

# Remove due date
todo schedule 1 --no-due

# Show tasks due this week
todo schedule --upcoming
todo schedule --upcoming 14  # next 14 days
```

### Reminders
```bash
# Set reminder
todo remind 1 --at "1 day before"
todo remind 1 --at "2025-12-30 10:00"

# Set repeating reminder
todo remind 1 --at "1 hour before" --repeat

# List all reminders
todo remind --list

# Remove reminder
todo remind 1 --cancel
```

### Recurring Tasks
```bash
# Set recurrence
todo recur 1 --pattern daily
todo recur 1 --pattern "every monday"
todo recur 1 --pattern weekly --until 2026-12-31

# List recurring tasks
todo recur --list

# Stop recurrence
todo recur 1 --stop
```

### Overdue & Upcoming
```bash
# Show overdue tasks
todo overdue

# Show upcoming tasks
todo upcoming
todo upcoming 14  # next 14 days
todo upcoming --priority high
```

---

## Integration Points

- **storage-agent**: Persist scheduler metadata
- **todo-operations**: Update tasks with schedule info
- **todo-analytics-agent**: Query tasks by date ranges
- **System cron/scheduler**: Background reminder checks

---

## Data Model

### Task Schedule Metadata
```json
{
  "task_id": 1,
  "due_date": "2025-12-31T23:59:59Z",
  "reminders": [
    {
      "remind_at": "2025-12-30T10:00:00Z",
      "type": "console",
      "repeat": false,
      "sent": false
    }
  ],
  "recurrence": {
    "pattern": "weekly",
    "next_date": "2026-01-01T00:00:00Z",
    "end_date": null,
    "auto_create": true
  }
}
```

---

## Background Processes

### Reminder Checker (runs every minute)
1. Fetch all unsent reminders where `remind_at <= now`
2. Display notification for each
3. Mark as sent
4. If repeating, schedule next reminder

### Overdue Monitor (runs daily)
1. Check for newly overdue tasks
2. Send daily digest of overdue tasks (optional)
3. Update overdue statistics

### Recurrence Manager (runs on task completion)
1. Check if task has recurrence pattern
2. Calculate next occurrence date
3. Create new task with updated due date
4. Link tasks in recurrence chain

---

## Error Scenarios

1. **Invalid Date**: Return parsing error with examples
2. **Past Due Date**: Warn but allow (user may be backdating)
3. **Invalid Recurrence Pattern**: Return validation error
4. **Task Not Found**: Return 404-style error
5. **Reminder in Past**: Reject with error

---

## Acceptance Criteria

- [ ] Due dates can be set using natural language
- [ ] Due dates can be set using ISO format
- [ ] Reminders are displayed at specified time
- [ ] Recurring tasks auto-create next occurrence
- [ ] Overdue tasks are correctly identified
- [ ] Upcoming tasks can be queried by date range
- [ ] All scheduler data persists across restarts
- [ ] Time zones are handled consistently
- [ ] Background processes run reliably
- [ ] Visual indicators for overdue/upcoming tasks
