# Todo App - Quick Start Implementation Guide

## 🚀 Start Here

This guide gets you from zero to first working code in 30 minutes.

---

## Step 1: Environment Setup (10 minutes)

```bash
# Navigate to project
cd /home/tahiraibrahim7/Evolution-of-Todo/phase-1-console

# Verify Python version
python --version  # Must be 3.12+

# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # Linux/Mac
# OR: venv\Scripts\activate  # Windows

# Verify activation
which python  # Should show: .../venv/bin/python
```

---

## Step 2: Install Dependencies (5 minutes)

```bash
# Install core dependencies
pip install "typer[all]" rich pytest pytest-cov pytest-mock

# Optional: Quality tools
pip install black mypy pylint

# Create requirements file
cat > requirements.txt << EOF
typer[all]>=0.9.0
rich>=13.0.0
EOF

cat > requirements-dev.txt << EOF
-r requirements.txt
pytest>=7.0.0
pytest-cov>=4.0.0
pytest-mock>=3.10.0
black>=23.0.0
mypy>=1.0.0
pylint>=2.17.0
EOF

# Verify installation
python -c "import typer, rich; print('✓ Dependencies installed')"
```

---

## Step 3: Create Project Structure (5 minutes)

```bash
# Create directories
mkdir -p utils skills tests

# Create .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
venv/

# Testing
.pytest_cache/
.coverage
htmlcov/

# Data
todos.json
todos.backup.*.json

# IDE
.vscode/
.idea/
EOF

# Verify structure
tree -L 1 -a
# Should show: utils/, skills/, tests/, .gitignore
```

---

## Step 4: First File - `utils/models.py` (10 minutes)

```bash
# Create initial files
touch utils/__init__.py
touch utils/models.py
touch tests/test_models.py

# Open utils/models.py and paste:
```

```python
"""Data models and type definitions for Todo App."""

from enum import Enum
from typing import Optional

class Priority(str, Enum):
    """Task priority levels."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

    @classmethod
    def default(cls) -> "Priority":
        """Return default priority."""
        return cls.MEDIUM

    @classmethod
    def from_string(cls, value: str) -> "Priority":
        """Parse priority from string (case-insensitive)."""
        try:
            return cls(value.lower())
        except ValueError:
            valid = ", ".join([p.value for p in cls])
            raise ValueError(f"Invalid priority: {value}. Must be one of: {valid}")

# Test it works
if __name__ == "__main__":
    print(f"✓ Priority.HIGH = {Priority.HIGH.value}")
    print(f"✓ Priority.default() = {Priority.default().value}")
    print(f"✓ Priority.from_string('HIGH') = {Priority.from_string('HIGH').value}")
```

```bash
# Test it works
python utils/models.py
# Should print:
# ✓ Priority.HIGH = high
# ✓ Priority.default() = medium
# ✓ Priority.from_string('HIGH') = high
```

---

## Step 5: First Test (5 minutes)

Open `tests/test_models.py` and paste:

```python
"""Tests for utils.models module."""

import pytest
from utils.models import Priority

def test_priority_values():
    """Test priority enum values."""
    assert Priority.HIGH.value == "high"
    assert Priority.MEDIUM.value == "medium"
    assert Priority.LOW.value == "low"

def test_priority_default():
    """Test default priority."""
    assert Priority.default() == Priority.MEDIUM

def test_priority_from_string():
    """Test case-insensitive parsing."""
    assert Priority.from_string("high") == Priority.HIGH
    assert Priority.from_string("HIGH") == Priority.HIGH
    assert Priority.from_string("HiGh") == Priority.HIGH

def test_priority_from_string_invalid():
    """Test invalid priority raises ValueError."""
    with pytest.raises(ValueError, match="Invalid priority"):
        Priority.from_string("invalid")
```

Run the tests:

```bash
pytest tests/test_models.py -v

# Should show:
# test_models.py::test_priority_values PASSED
# test_models.py::test_priority_default PASSED
# test_models.py::test_priority_from_string PASSED
# test_models.py::test_priority_from_string_invalid PASSED
# ====== 4 passed in 0.XX s ======
```

---

## 🎉 Success!

You now have:
- ✅ Environment configured
- ✅ Dependencies installed
- ✅ Project structure created
- ✅ First module implemented (Priority enum)
- ✅ First tests passing

---

## Next Steps

### Option 1: Continue with models.py (Recommended)
Follow the detailed checklist in `specs/todo-app/tasks.md` → Task 1.1

**Next enum to implement:** `Status` (PENDING, IN_PROGRESS, COMPLETED)

### Option 2: View Full Plan
- **Tasks Checklist**: `specs/todo-app/tasks.md` (detailed step-by-step)
- **Implementation Plan**: `specs/todo-app/plan.md` (overview)
- **Quick Reference**: `specs/todo-app/README.md` (navigation)

---

## Reference: Task Order

```
Phase 1: Foundation
  1.1 utils/models.py ←── YOU ARE HERE
  1.2 utils/storage.py
  1.3 utils/__init__.py

Phase 2: Skills
  2.1 add_skill.py
  2.2 list_skill.py
  2.3 update_skill.py
  2.4 complete_skill.py
  2.5 delete_skill.py
  2.6 scheduler_skill.py

Phase 3: CLI
  3.1 main.py
  3.2 Entry point (pyproject.toml)

Phase 4: Testing
  4.1 Integration tests
  4.2 Manual testing
  4.3 Quality checks

Phase 5: Documentation
  5.1 README.md
```

---

## Useful Commands

```bash
# Run tests
pytest -v

# Run with coverage
pytest --cov=utils --cov-report=term-missing

# Format code
black utils/ skills/ tests/

# Type check
mypy utils/ skills/

# Lint code
pylint utils/ skills/

# View task checklist
cat specs/todo-app/tasks.md | less

# View current todos
grep -E "^\- \[ \]" specs/todo-app/tasks.md | head -10
```

---

## Troubleshooting

**Import errors?**
- Verify venv activated: `which python`
- Reinstall dependencies: `pip install -r requirements-dev.txt`

**Tests failing?**
- Check you're in project root
- Verify file created: `ls -l utils/models.py`
- Check imports work: `python -c "from utils.models import Priority"`

**pytest not found?**
- Verify venv activated
- Install: `pip install pytest`

---

## Constitution Reminder

Every function you write must have:
1. ✅ Type hints
2. ✅ Docstring (Google style)
3. ✅ try-except error handling
4. ✅ Return OperationResult (for skills)

---

**Ready to continue?** Open `specs/todo-app/tasks.md` and follow Task 1.1! 🚀
