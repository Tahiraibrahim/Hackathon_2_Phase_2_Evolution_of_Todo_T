# Phase 1 Console Todo App Constitution

<!--
Sync Impact Report:
- Version change: initial → 1.0.0
- New constitution created for Phase 1 Console Todo App
- Added 6 core principles for Python architecture
- Added 3 supplementary sections (Tech Stack, Data Management, Code Organization)
- Templates status: ✅ No dependent templates require updates (initial constitution)
- Follow-up TODOs: None
-->

## Core Principles

### I. Specification-Driven Development
**All implementation MUST follow specification files as the single source of truth.**

- Every feature starts with a `.md` specification file in the `skills/` directory
- Specifications define: purpose, inputs, outputs, processing logic, error scenarios, acceptance criteria
- Implementation files (`.py`) MUST NOT deviate from their corresponding specification
- Read the spec first, implement second - never assume behavior
- Specifications are living documents - update spec when requirements change, then update code

**Rationale:** Prevents drift between design and implementation; ensures team alignment; facilitates code reviews and onboarding.

### II. Modular Architecture
**Every skill is self-contained with clear boundaries and minimal coupling.**

- Each skill has paired files: `skills/<name>_skill.md` (spec) and `skills/<name>_skill.py` (implementation)
- Skills expose public functions that agents can invoke
- Skills handle their own validation, error handling, and data transformation
- Inter-skill communication goes through well-defined interfaces (function parameters and return values)
- No circular dependencies between skills

**Rationale:** Enables independent testing, parallel development, and easy replacement/upgrading of individual components.

### III. Comprehensive Error Handling (NON-NEGOTIABLE)
**Every function MUST include try-except blocks with meaningful error messages.**

- All file I/O operations wrapped in try-except with specific error types
- All user input validated before processing
- Errors return structured responses: `{"success": false, "error": "message", "code": "ERROR_CODE"}`
- Never let exceptions bubble to user without context
- Log errors for debugging while showing user-friendly messages

**Rationale:** Robustness is critical for CLI tools; cryptic errors destroy user trust; structured error responses enable automated error handling.

### IV. Test-First Development
**Tests written and approved before implementation begins.**

- Follow Red-Green-Refactor cycle: Write failing test → Implement → Refactor
- Each skill must have corresponding test file: `tests/test_<name>_skill.py`
- Test coverage includes: happy path, edge cases, error scenarios, validation failures
- Integration tests verify agent-skill-storage interactions
- All tests must pass before merging

**Rationale:** Prevents regression; documents expected behavior; enables confident refactoring; catches edge cases early.

### V. Rich User Experience
**CLI output MUST be visually clear, informative, and use the rich library for formatting.**

- Use `rich.table.Table` for list/tabular data with color coding
- Use `rich.console.Console` for formatted output
- Priority levels have distinct colors: High (red), Medium (yellow), Low (green)
- Success messages use ✓ symbol; errors use ⚠ or ✗
- Provide helpful context in all messages (task IDs, titles, counts)

**Rationale:** Terminal UX matters; color and formatting improve scannability; visual hierarchy reduces cognitive load.

### VI. Type Safety and Documentation
**All functions MUST have type hints and docstrings.**

- Use Python 3.12+ type hints for all function parameters and return values
- Include Optional, Union, List, Dict types where applicable
- Docstrings follow Google style: summary, Args, Returns, Raises
- Public functions document all parameters, return values, and exceptions
- Private functions (prefixed with `_`) still need brief docstrings

**Rationale:** Type hints catch bugs at development time; docstrings serve as inline specification; IDE support improves dramatically.

## Technology Stack

### Required Dependencies
- **Python**: 3.12 or higher (for modern type hints and performance)
- **typer**: CLI framework with automatic help generation
- **rich**: Terminal formatting and tables
- **datetime**: Built-in for timestamp and date handling
- **json**: Built-in for data persistence
- **pathlib**: Built-in for cross-platform file paths

### Optional Dependencies (Phase 2+)
- **pytest**: Testing framework
- **pydantic**: Data validation and settings management
- **python-dateutil**: Advanced date parsing for natural language dates

### Constraints
- No external database dependencies (use `todos.json`)
- No web frameworks or HTTP dependencies
- Keep dependencies minimal to reduce attack surface and installation friction

## Data Management

### Storage Format
- **File**: `todos.json` in project root
- **Format**: JSON array of task objects
- **Schema**: Defined by skill specifications
- **Backup**: Create `.backup` files before destructive operations

### Data Integrity Rules
- Atomic writes: write to temp file, then rename (prevents corruption)
- Validate JSON structure before reading
- Handle missing file gracefully (create with empty array)
- Never store sensitive data (no passwords, tokens, etc.)
- Task IDs are auto-incrementing integers starting from 1

### Schema Evolution
- Add new fields with default values (backward compatible)
- Never remove fields without migration plan
- Version schema if breaking changes needed: `{"schema_version": 1, "tasks": [...]}`

## Code Organization

### Directory Structure
```
phase-1-console/
├── skills/                    # Specifications and implementations
│   ├── add_skill.md          # Specification files
│   ├── add_skill.py          # Implementation files
│   ├── list_skill.md
│   ├── list_skill.py
│   └── ...
├── tests/                     # Test files mirror skills/
│   ├── test_add_skill.py
│   ├── test_list_skill.py
│   └── ...
├── .claude/                   # Agent configurations
│   └── agents/
├── main.py                    # CLI entry point (typer app)
├── todos.json                 # Data file (gitignored)
└── pyproject.toml            # Dependencies and project metadata
```

### Naming Conventions
- **Files**: `snake_case_skill.py`, `test_snake_case.py`
- **Functions**: `snake_case_function()`
- **Classes**: `PascalCase` (if needed)
- **Constants**: `UPPER_SNAKE_CASE`
- **Private functions**: `_leading_underscore()`

### Import Organization
1. Standard library imports
2. Third-party imports (typer, rich)
3. Local application imports
4. One blank line between groups
5. Alphabetical within groups

## Governance

### Constitution Authority
- This constitution supersedes all other practices and guidelines
- All code reviews MUST verify compliance with these principles
- Deviations require explicit justification and architecture decision record (ADR)

### Amendment Process
1. Propose change via issue/discussion
2. Document rationale and impact
3. Update constitution with version bump
4. Update affected code to comply
5. Get approval before merging

### Version Semantics
- **MAJOR**: Breaking changes to principles (e.g., removing required error handling)
- **MINOR**: New principles added or existing principles expanded
- **PATCH**: Clarifications, typo fixes, non-semantic improvements

### Compliance Verification
- Pre-commit hooks check for type hints and docstrings
- CI/CD pipeline runs all tests
- Code reviews verify specification adherence
- Regular audits of error handling patterns

**Version**: 1.0.0 | **Ratified**: 2025-12-25 | **Last Amended**: 2025-12-25
