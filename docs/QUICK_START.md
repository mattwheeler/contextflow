# ContextFlow Quick Start Guide

Get up and running with ContextFlow in under 5 minutes!

## Installation

```bash
# Clone the repository
git clone https://github.com/mattwheeler/contextflow.git
cd contextflow

# Install dependencies
pip install -r requirements.txt

# Install ContextFlow
pip install -e .
```

## Initialize Your First Project

```bash
# Initialize with a template
contextflow init --template software-development --name "My Project" --description "My side project"

# Or use interactive mode
contextflow init
```

**Available Templates:**
- `software-development` - JIRA, GitHub, technical documentation
- `research-project` - Research notes, literature tracking
- `side-project` - Simple tracking for personal projects
- `content-creation` - Editorial calendars, content workflows
- `consulting` - Client deliverables, meeting management
- `academic-research` - Paper writing, citation management
- `minimal` - Basic session tracking only

## Configure Integrations

Edit the generated `contextflow.yaml` file:

```yaml
integrations:
  jira:
    enabled: true
    base_url: "https://your-company.atlassian.net"
    project_key: "PROJ"
    username: "your-email@company.com"
    api_token: "your-api-token"

  github:
    enabled: true
    repository: "your-org/your-repo"
    token: "your-github-token"
```

### Getting API Tokens

**JIRA/Confluence:**
1. Go to [Atlassian Account Settings](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Create API token
3. Use your email as username

**GitHub:**
1. Go to GitHub Settings > Developer settings > Personal access tokens
2. Generate new token with `repo` and `issues` permissions

## Your First AI Session

### 1. Get Context for New AI Session

```bash
# Get quick context (copy-paste ready)
contextflow context --quick
```

Copy the output and paste into your AI session with:
```
"Here's my project context: [paste content]"
```

### 2. Work on Your Project

Use your AI assistant as normal with full project context!

### 3. End Session

```bash
contextflow update "Implemented user authentication system, updated API documentation, fixed issue PROJ-123"
```

**Include in your summary:**
- Work items referenced (PROJ-123, #456, issue-789)
- Files created or modified
- Features added or bugs fixed
- Architecture or design changes

## Monitor Your Progress

```bash
# Check project status
contextflow status

# View recent session logs
contextflow logs --recent

# Refresh AI context
contextflow context --refresh
```

## Best Practices

### Do This
- **Start every AI session** with `contextflow context --quick`
- **End every session** with `contextflow update "[detailed summary]"`
- **Include work item references** in your summaries
- **Be specific** about files and changes made
- **Refresh context** after major project changes

### Avoid This
- Skipping session updates
- Vague summaries like "fixed some bugs"
- Missing work item references
- Forgetting to refresh context

## Typical Workflow

```bash
# 1. Start new AI session
contextflow context --quick
# Copy output to AI session

# 2. Work with AI assistant
# (AI has full project context)

# 3. End session with update
contextflow update "Implemented login component in src/components/Login.tsx, added authentication API endpoints, updated user stories PROJ-45 and PROJ-46, fixed responsive design issues"

# 4. Check status (optional)
contextflow status
```

## Success!

You're now using ContextFlow! Your AI sessions will have perfect continuity, and your project documentation will stay current automatically.

## Need Help?

- **Configuration issues:** Check `docs/configuration.md`
- **Integration setup:** Check `docs/integrations.md`
- **Troubleshooting:** Check `docs/troubleshooting.md`
- **Examples:** Check `examples/` directory

## Next Steps

1. **Customize your workflow** in `contextflow.yaml`
2. **Set up integrations** if working with teams
3. **Explore advanced features** in the documentation
4. **Share ContextFlow** with friends!

---

**Remember:** The key to ContextFlow success is consistency. Make session updates a habit, and you'll never lose context again!
