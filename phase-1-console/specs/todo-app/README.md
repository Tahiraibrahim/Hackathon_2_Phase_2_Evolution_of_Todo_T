# Todo App Implementation - Quick Start Guide

## Overview
This directory contains the implementation plan for the Phase 1 Console Todo App.

## Document

### [plan.md](./plan.md) - Complete Implementation Plan
Comprehensive step-by-step guide with:
- 5 implementation phases
- Detailed task breakdowns with checklists
- Acceptance criteria for each component
- Time estimates (37-52 hours total)
- Testing strategy
- Risk mitigation
- 4-week timeline

## Quick Navigation

### By Phase

**Phase 1: Foundation Layer (9-11.5 hours)**
- Step 1.1: utils/models.py (4-6h)
- Step 1.2: utils/storage.py (4-5h)
- Step 1.3: utils/__init__.py (0.5h)

**Phase 2: Skill Layer (18-23 hours)**
- Step 2.1: add_skill.py (2-3h)
- Step 2.2: list_skill.py (3-4h)
- Step 2.3: update_skill.py (2-3h)
- Step 2.4: complete_skill.py (1.5-2h)
- Step 2.5: delete_skill.py (1.5-2h)
- Step 2.6: scheduler_skill.py (3-4h)

**Phase 3: Integration Layer (5.5-6.5 hours)**
- Step 3.1: main.py (5-6h)
- Step 3.2: Entry point (0.5h)

**Phase 4: Testing & Validation (6-10 hours)**
- Integration testing
- Manual testing
- Acceptance verification
- Code quality checks

**Phase 5: Documentation (2-4 hours)**
- README creation
- Examples and tutorials
- Final review

## Implementation Order (Critical!)

```
1. utils/models.py      ← No dependencies, required by everything
2. utils/storage.py     ← Depends on models (type hints only)
3. utils/__init__.py    ← Exports public APIs
4. add_skill.py         ← Simplest skill, foundational
5. list_skill.py        ← Read-only, good second step
6. update_skill.py      ← Builds on add concepts
7. complete_skill.py    ← Specialized update
8. delete_skill.py      ← With backup logic
9. scheduler_skill.py   ← Most complex (dates)
10. main.py             ← Ties everything together
```

**DO NOT skip steps or change order** - dependencies matter!

## Key Principles

### 1. Specification-Driven
- Read the `.md` spec file first
- Implement exactly what spec describes
- Don't add features not in spec
- Update spec if requirements change

### 2. Test-First
- Write tests before or alongside implementation
- Aim for >80% coverage
- Run tests continuously
- Fix failures immediately

### 3. Error Handling
- Every function has try-except
- Return OperationResult (never raise to CLI)
- Clear, actionable error messages
- Log for debugging

### 4. Type Safety
- All functions have type hints
- Use enums for constrained values
- Dataclasses for structured data
- Validate at boundaries

## Quick Start

### 1. Set Up Environment
```bash
cd /home/tahiraibrahim7/Evolution-of-Todo/phase-1-console
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt  # Create this with: typer, rich, pytest
```

### 2. Start with Phase 1
```bash
# Read the spec
cat specs/integration/models-spec.md

# Create the file
mkdir -p utils
touch utils/__init__.py
touch utils/models.py

# Start implementing following plan.md Step 1.1
```

### 3. Test As You Go
```bash
# Create test file
mkdir -p tests
touch tests/test_models.py

# Write tests, run continuously
pytest tests/test_models.py -v
pytest --cov=utils tests/
```

### 4. Move to Next Phase
Only after:
- ✅ All tasks in current phase completed
- ✅ All tests passing
- ✅ Acceptance criteria met
- ✅ Code reviewed against spec

## Reference Documents

### Specifications
- **Constitution**: `../../.specify/memory/constitution.md`
- **Integration Architecture**: `../../specs/integration/architecture.md`
- **Storage Spec**: `../../specs/integration/storage-spec.md`
- **Models Spec**: `../../specs/integration/models-spec.md`
- **Main CLI Spec**: `../../specs/integration/main-cli-spec.md`
- **Skill Specs**: `../../skills/*_skill.md`

### Related
- **Skills Specs**: `../../skills/` (6 skill specification files)
- **Integration README**: `../../specs/integration/README.md`

## Common Patterns

### Function Structure
```python
def skill_function(param: str, optional: str = "default") -> OperationResult:
    """
    Brief description.

    Args:
        param: Description
        optional: Description

    Returns:
        OperationResult with success status and data
    """
    try:
        # 1. Validation
        validated = validate_input(param)

        # 2. Business logic
        result = do_work(validated)

        # 3. Persistence
        save_data(result)

        # 4. Success response
        return OperationResult.success_result(
            message="Operation succeeded",
            data=result
        )

    except ValueError as e:
        return OperationResult.error_result(str(e), "VALIDATION_ERROR")
    except StorageError as e:
        return OperationResult.error_result(str(e), "STORAGE_ERROR")
    except Exception as e:
        return OperationResult.error_result(str(e), "UNKNOWN_ERROR")
```

### Test Structure
```python
def test_success_case():
    """Test the happy path."""
    result = skill_function("valid input")
    assert result.success
    assert result.data is not None
    assert "succeeded" in result.message.lower()

def test_validation_error():
    """Test validation failure."""
    result = skill_function("")
    assert not result.success
    assert result.error_code == "VALIDATION_ERROR"
    assert "invalid" in result.error.lower()
```

## Checkpoints

### After Phase 1
- [ ] utils/models.py complete and tested
- [ ] utils/storage.py complete and tested
- [ ] utils/__init__.py exports working
- [ ] Can create Task objects
- [ ] Can save/load from JSON
- [ ] All tests passing

### After Phase 2
- [ ] All 6 skills implemented
- [ ] All skill tests passing
- [ ] Can add, list, update, complete, delete tasks
- [ ] Scheduler functions work
- [ ] No skill imports from main.py yet

### After Phase 3
- [ ] main.py complete
- [ ] All CLI commands work
- [ ] Can run `todo --help`
- [ ] Rich output displays correctly
- [ ] End-to-end workflows function

### After Phase 4
- [ ] Integration tests pass
- [ ] Manual testing complete
- [ ] Coverage >80%
- [ ] All acceptance criteria met
- [ ] No known bugs

### After Phase 5
- [ ] README complete
- [ ] Examples provided
- [ ] Code reviewed
- [ ] Ready to ship

## Troubleshooting

### Import Errors
- Check you're in venv: `which python`
- Check dependencies: `pip list`
- Check PYTHONPATH includes project root
- Check for circular imports

### Test Failures
- Read error message carefully
- Check test is testing correct behavior
- Verify mock setup is correct
- Check file paths in tests
- Ensure temp directories cleaned up

### Spec Confusion
- Re-read the specification file
- Check integration architecture doc
- Look at examples in spec
- Refer to constitution for principles

## Timeline

### Week 1: Foundation
- Mon-Tue: models.py
- Wed-Thu: storage.py
- Fri: __init__.py + review

### Week 2: Skills Part 1
- Mon: add_skill
- Tue: list_skill
- Wed: update_skill
- Thu: complete_skill
- Fri: delete_skill

### Week 3: Skills Part 2 + CLI
- Mon: scheduler_skill
- Tue-Thu: main.py
- Fri: Entry point + testing

### Week 4: Polish
- Mon-Tue: Integration tests
- Wed: Manual testing + fixes
- Thu: Acceptance verification
- Fri: Documentation + review

## Questions?

1. Check [plan.md](./plan.md) for detailed steps
2. Check spec files for component details
3. Check constitution for principles
4. Refer to integration architecture for patterns

## Success Metrics

- ✅ All features working as specified
- ✅ Test coverage >80%
- ✅ No critical bugs
- ✅ Clean, readable code
- ✅ Comprehensive error handling
- ✅ Rich CLI output
- ✅ Fast response times (<100ms)
- ✅ Data integrity (atomic writes)
- ✅ Constitution compliant

---

**Ready to begin?** Start with Phase 1.1 in [plan.md](./plan.md)!
