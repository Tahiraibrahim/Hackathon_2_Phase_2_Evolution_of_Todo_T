# Evolution of Todo

A modern, full-stack task management application with a Dark Cyberpunk theme.

## Features

### Completed Features
- [x] **User Authentication** - Secure login/register with JWT tokens
- [x] **Task Management** - Create, read, update, delete tasks with priorities
- [x] **Dark Cyberpunk Theme** - Glass-morphism UI with smooth animations
- [x] **Notifications System** - Real-time toast notifications with bell icon
- [x] **User Profile Display** - Personalized greeting with user name
- [x] **Search Functionality** - Real-time task filtering by title, description, or category
- [x] **Analytics Dashboard** - Comprehensive productivity insights including:
  - Total tasks, completed, and pending counts
  - Completion rate with animated progress bar
  - Priority breakdown (High/Medium/Low) with individual progress
  - Dynamic productivity messages based on performance
- [x] **Profile Page** - User profile card with:
  - Avatar with user initial
  - Name, email, and Pro User badge
  - Member since date and account type
  - Edit Profile button (visual)
  - Account overview stats
- [x] **Settings Page** - Preferences panel with:
  - Email Notifications toggle (On/Off)
  - Compact Mode toggle (On/Off)
  - Danger Zone with Delete Account button
  - Version and theme info

### Upcoming Features
- [ ] Recurring Tasks
- [ ] Task Categories Management
- [ ] Dark/Light Theme Toggle
- [ ] Export Tasks to CSV

---

## Python Virtual Environment Setup

### Automatic Activation in VS Code

This project is configured to automatically activate the Python virtual environment (`.venv`) when you open a new terminal in VS Code.

**Requirements:**
- VS Code with the Python extension installed
- A `.venv` folder in the project root

**How it works:**
The `.vscode/settings.json` file contains:
```json
{
    "python.terminal.activateEnvironment": true,
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python"
}
```

When you open a new terminal, VS Code will automatically run the activation script.

### Creating the Virtual Environment

If you haven't created the virtual environment yet:

```bash
# Create the virtual environment
python3 -m venv .venv

# Activate it manually (first time only)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Manual Activation (if needed)

If auto-activation doesn't work, you can manually activate:

```bash
source .venv/bin/activate
```

### Optional: Auto-activate in any terminal (via .bashrc)

To automatically activate the venv whenever you `cd` into this project directory (works outside VS Code too), add this to your `~/.bashrc`:

```bash
# Auto-activate Python venv when entering project directory
cd() {
    builtin cd "$@" || return
    if [[ -f ".venv/bin/activate" ]]; then
        source .venv/bin/activate
    fi
}
```

Then reload your shell:
```bash
source ~/.bashrc
```

**Alternative:** Add a direct activation line for this specific project:
```bash
# Add to ~/.bashrc
alias todo-env="cd /home/tahiraibrahim7/Evolution-of-Todo && source .venv/bin/activate"
```

Then just type `todo-env` to navigate and activate in one command.
