# Phase 1 Console Todo Application

A fully functional, specification-driven console-based todo application built with Python 3.12+, Typer, and Rich.

## ✅ Implementation Complete

All components have been implemented following the specifications in `skills/*.md` and `specs/integration/*.md`.

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Add your first task
python main.py add "Buy groceries"

# 3. List tasks
python main.py list

# 4. Get help
python main.py --help
```

## 📖 Usage Examples

```bash
# Add tasks
python main.py add "Submit report" --priority high --category work --due 2025-12-31

# List with filters
python main.py list --priority high --status pending

# Complete a task
python main.py complete 1

# View upcoming tasks
python main.py schedule --upcoming

# View overdue tasks
python main.py overdue

# Show task details
python main.py show 1

# Update task
python main.py update 1 --priority high --status in_progress

# Delete task (with confirmation)
python main.py delete 1
```

## ✨ Features

- ✅ Add, list, update, complete, delete tasks
- ✅ Filter by status, priority, category
- ✅ Sort by any field
- ✅ Due dates and overdue detection
- ✅ Rich formatted tables with colors
- ✅ Atomic file writes (data integrity)
- ✅ Comprehensive error handling
- ✅ Type-safe with Python 3.12+ hints

## 📁 Project Structure

```
phase-1-console/
├── main.py              # CLI entry point
├── utils/               # Models & storage
│   ├── models.py       # Data types & validation
│   └── storage.py      # File I/O operations
├── skills/              # Business logic
│   ├── add_skill.py
│   ├── list_skill.py
│   ├── update_skill.py
│   ├── complete_skill.py
│   ├── delete_skill.py
│   └── scheduler_skill.py
└── todos.json          # Data file (created on first use)
```

## 📚 Full Documentation

See the complete documentation in the project files:
- Installation & usage details above
- Specifications: `skills/*.md`
- Architecture: `specs/integration/architecture.md`
- Implementation plan: `specs/todo-app/plan.md`

---

**Version:** 1.0.0 | **Status:** ✅ Complete and Ready for Use
