# ContextFlow

**AI Session Context & Workflow Automation**

*Never lose context between AI sessions again*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## What is ContextFlow?

ContextFlow is a personal automation tool that keeps your AI coding sessions connected. If you're tired of re-explaining your project to ChatGPT, Claude, or other AI assistants every time you start a new conversation, ContextFlow solves that problem.

It automatically captures what you're working on, saves session notes, and gives you ready-to-paste context for your next AI session.

### Key Features

- **AI Context Preservation** - Automatically extract and format project context for new AI sessions
- **Session Documentation** - Auto-update project management tools (JIRA, GitHub, Confluence)
- **Workflow Automation** - Keep consistent notes and documentation
- **Session Tracking** - Complete history of all your work with searchable logs
- **Multi-Platform Integration** - Works with Confluence, JIRA, GitHub, Notion, and more
- **Project Templates** - Pre-configured setups for different project types
- **Secure Credential Management** - No plaintext passwords, uses system keyring
- **Personal & Team Friendly** - Works great solo or with small teams

## Recent Improvements

### v1.0.0 - January 2025
- **🔧 Fixed Keyring Access Issue**: Resolved credential retrieval problems that prevented JIRA/Confluence integration
- **📦 Proper Module Installation**: Added `__main__.py` and console script entry points for easy execution
- **🚀 Multiple Execution Methods**: Run via command, Python module, or direct import
- **✅ Verified Integrations**: JIRA and Confluence integrations now working properly
- **🛡️ Enhanced Security**: Improved credential handling with system keyring integration

## Quick Start

### Installation

#### Option 1: Development Installation (Recommended)
```bash
# Clone the repository
git clone https://github.com/mattwheeler/contextflow.git
cd contextflow

# Install in development mode
pip install --user -e .
```

#### Option 2: Direct Installation
```bash
# Install from source
pip install --user git+https://github.com/mattwheeler/contextflow.git
```

### Running ContextFlow

After installation, you have multiple ways to run ContextFlow:

#### Option 1: Direct Command (if Python bin is in PATH)
```bash
contextflow --help
```

#### Option 2: Full Path to Command
```bash
# macOS/Linux (adjust path for your system)
/Users/yourusername/Library/Python/3.9/bin/contextflow --help
```

#### Option 3: Python Module
```bash
python3 -m contextflow --help
```

### Basic Usage

```bash
# Initialize a new project
contextflow init --template software-development

# Setup secure credentials (one-time)
contextflow setup jira
contextflow setup confluence
contextflow setup github

# Start a new AI session with context
contextflow context --quick

# End session with documentation update
contextflow update "Implemented user authentication, updated API docs, fixed PROJ-123"

# Check project status
contextflow status

# View stored credentials
contextflow credentials
```

## Use Cases

### Software Development
- Maintain context across coding sessions
- Auto-update JIRA stories and GitHub issues
- Track technical decisions and architecture changes
- Keep notes on code reviews and bug fixes

### Research Projects
- Document research findings and methodology
- Track literature review progress
- Maintain experiment logs and results
- Keep track of hypothesis changes

### Side Projects
- Keep context when working on personal projects
- Track progress across sporadic work sessions
- Maintain notes on what you were thinking
- Document decisions for future reference

### Content Creation
- Manage content ideas and drafts
- Track writing progress and feedback
- Maintain notes on content strategy
- Document creative decisions

## Architecture

```
ContextFlow Engine
├── Session Documentation
│   ├── Intelligent summary parsing
│   ├── Multi-platform updates
│   ├── Automated categorization
│   └── Progress tracking
├── AI Context Management
│   ├── Documentation extraction
│   ├── Context formatting
│   ├── Quick-reference generation
│   └── Auto-refresh capabilities
├── Session Tracking
│   ├── Timestamped logs
│   ├── Change tracking
│   ├── Searchable history
│   └── Complete work history
└── Workflow Automation
    ├── Consistent updates
    ├── Quality validation
    ├── Optional notifications
    └── Progress tracking
```

## Project Templates

ContextFlow includes pre-configured templates for common project types:

- **Software Development** - JIRA, GitHub, technical documentation
- **Research Project** - Literature tracking, experiment logs, findings
- **Side Project** - Simple tracking for personal projects
- **Content Creation** - Editorial calendars, progress tracking
- **Consulting** - Client deliverables, meeting notes
- **Academic Research** - Paper writing, citation management

## Configuration

Create a `contextflow.yaml` in your project root:

```yaml
project:
  name: "My Project"
  description: "My side project description"
  type: "software-development"

integrations:
  confluence:
    enabled: true
    base_url: "https://mycompany.atlassian.net"
    space_key: "PROJ"
  jira:
    enabled: true
    project_key: "PROJ"
  github:
    enabled: true
    repository: "myorg/myproject"

ai_context:
  quick_context_file: "QUICK_CONTEXT.txt"
  full_context_file: "PROJECT_CONTEXT.md"
  auto_refresh: true

workflow:
  mandatory_session_updates: true
  require_work_item_references: false
  session_log_retention_days: 90
  team_notifications: false
```

## Documentation

- [Installation Guide](docs/installation.md)
- [Configuration Reference](docs/configuration.md)
- [Usage Examples](docs/usage.md)
- [Integration Setup](docs/integrations.md)
- [Project Templates](docs/templates.md)

## Contributing

Contributions welcome! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## Troubleshooting

### Installation Issues

#### "contextflow command not found"
If the `contextflow` command isn't found after installation:

1. **Check if Python bin directory is in PATH:**
   ```bash
   echo $PATH | grep -o '/Users/[^/]*/Library/Python/[^/]*/bin'
   ```

2. **Add Python bin to PATH (macOS):**
   ```bash
   echo 'export PATH="$HOME/Library/Python/3.9/bin:$PATH"' >> ~/.zshrc
   source ~/.zshrc
   ```

3. **Use full path instead:**
   ```bash
   /Users/yourusername/Library/Python/3.9/bin/contextflow --help
   ```

#### "No module named contextflow"
If you get import errors:

1. **Reinstall in development mode:**
   ```bash
   cd contextflow
   pip install --user -e .
   ```

2. **Check Python path:**
   ```bash
   python3 -c "import sys; print('\n'.join(sys.path))"
   ```

### Integration Issues

#### "JIRA/Confluence credentials not configured"
This was a known issue that has been fixed. If you still see this:

1. **Verify credentials are stored:**
   ```bash
   contextflow credentials
   ```

2. **Re-setup credentials if needed:**
   ```bash
   contextflow setup jira
   contextflow setup confluence
   ```

3. **Test the connection:**
   ```bash
   contextflow status
   ```

#### Keyring Access Issues
If you get keyring-related errors:

1. **macOS**: Ensure Keychain Access is working
2. **Linux**: Install `python3-keyring` package
3. **Windows**: Ensure Windows Credential Manager is accessible

### Common Issues

#### SSL/TLS Warnings
The urllib3 SSL warnings are harmless and don't affect functionality. They occur due to macOS system Python configuration.

#### Permission Errors
If you get permission errors during installation:
```bash
# Use --user flag to install in user directory
pip install --user -e .
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Why ContextFlow?

### The Problem
- Context loss between AI sessions wastes time and reduces productivity
- Inconsistent notes and documentation across work sessions
- Manual project management updates are forgotten
- Hard to remember what you were working on last time
- Difficulty picking up where you left off

### The Solution
ContextFlow automates context preservation and documentation, ensuring:
- **Zero Context Loss** - Every AI session starts with complete project understanding
- **Consistent Documentation** - Automated updates ensure nothing is missed
- **Easy Continuity** - Seamless pickup where you left off
- **Quick Onboarding** - New collaborators get up to speed immediately
- **Complete History** - Full record of all your work and decisions

## Success Stories

> "ContextFlow reduced my AI session startup time from 10 minutes to 30 seconds. My productivity increased significantly." - *Indie Developer*

> "As a consultant, ContextFlow helps me maintain perfect context across multiple client projects. Game changer!" - *Independent Consultant*

> "I can finally keep track of my side projects without losing momentum between sessions." - *Weekend Hacker*

## Get Started

Perfect for:
- Individual developers and creators
- Small teams and collaborators
- Consultants and freelancers
- Researchers and students
- Anyone working with AI assistants

[Download ContextFlow](https://github.com/mattwheeler/contextflow) and never lose context again!

---

**Made with ❤️ for the AI-assisted future**
