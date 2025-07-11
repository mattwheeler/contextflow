# ContextFlow Security Demo

This demonstrates the secure credential management features in ContextFlow.

## Before: Insecure Plaintext Storage

**OLD WAY (INSECURE):**
```yaml
# contextflow.yaml - DON'T DO THIS!
integrations:
  github:
    enabled: true
    repository: "user/repo"
    token: "ghp_xxxxxxxxxxxxxxxxxxxx"  # EXPOSED!

  jira:
    enabled: true
    base_url: "https://company.atlassian.net"
    username: "user@company.com"
    api_token: "ATATT3xFfGF0xxxxxxxxxxxxx"  # EXPOSED!
```

**Problems:**
- Credentials visible in config files
- Risk of accidental commits to version control
- Shared config files expose everyone's tokens
- No way to rotate credentials easily

## After: Secure Keyring Storage

**NEW WAY (SECURE):**
```yaml
# contextflow.yaml - Safe to commit!
integrations:
  github:
    enabled: true
    repository: "user/repo"
    # No credentials here!

  jira:
    enabled: true
    base_url: "https://company.atlassian.net"
    project_key: "PROJ"
    # No credentials here!
```

**Setup credentials securely:**
```bash
# One-time setup per integration
contextflow setup github
# Prompts: Enter GitHub personal access token: [hidden input]

contextflow setup jira
# Prompts: Enter JIRA username/email: user@company.com
# Prompts: Enter JIRA API token: [hidden input]
```

## Security Features Demo

### 1. Secure Storage
```bash
# Credentials stored in system keyring
# macOS: Keychain Access
# Windows: Credential Manager
# Linux: GNOME Keyring/KWallet

# View what's stored (no actual credentials shown)
contextflow credentials
```

### 2. Safe Configuration
```bash
# Config file is safe to share/commit
cat contextflow.yaml
# No secrets visible!

# Git status shows clean config
git add contextflow.yaml  # Safe!
```

### 3. Easy Management
```bash
# List stored credentials
contextflow credentials

# Remove credentials when done
contextflow remove-credentials github

# Re-setup when needed
contextflow setup github
```

### 4. Integration Security
```bash
# Each integration gets credentials securely
contextflow update "Fixed authentication bug in PROJ-123"
# Credentials retrieved from keyring automatically
# No plaintext exposure in memory or logs
```

## Migration from Plaintext

If you have existing plaintext credentials:

```bash
# 1. Remove from config file
# Edit contextflow.yaml and remove token/password lines

# 2. Setup secure storage
contextflow setup github
contextflow setup jira

# 3. Verify
contextflow credentials
# Shows: github: token, jira: username, api_token

# 4. Test
contextflow status
# Should work with secure credentials
```

## Security Benefits

### For Individuals
- **No accidental exposure** in config files
- **Safe to backup** configuration files
- **Easy credential rotation** without editing files
- **System-level security** using OS keyring

### For Teams
- **Shared configs** without shared credentials
- **Individual responsibility** for credential management
- **No credential conflicts** between team members
- **Audit trail** of who has access

### For Organizations
- **Compliance friendly** - no plaintext storage
- **Centralized policies** can control keyring access
- **Credential lifecycle** management
- **Reduced attack surface** for credential theft

## Technical Implementation

### Keyring Integration
```python
import keyring

# Store credential
keyring.set_password("contextflow", "github_token", token)

# Retrieve credential
token = keyring.get_password("contextflow", "github_token")

# Delete credential
keyring.delete_password("contextflow", "github_token")
```

### Supported Backends
- **macOS**: Keychain Services
- **Windows**: Windows Credential Manager
- **Linux**: Secret Service (freedesktop.org standard)
- **Fallback**: Encrypted file storage

### Zero-Trust Approach
- Credentials retrieved only when needed
- No caching in memory longer than necessary
- No logging of credential values
- Secure deletion from memory after use

---

**Result: Enterprise-grade security for personal productivity tools!**