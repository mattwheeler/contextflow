# ContextFlow Security

ContextFlow takes security seriously and implements secure credential management to protect your sensitive information.

## Secure Credential Storage

### System Keyring Integration

ContextFlow uses your operating system's secure keyring to store credentials:

- **macOS**: Keychain Access
- **Windows**: Windows Credential Manager
- **Linux**: Secret Service (GNOME Keyring, KWallet, etc.)

### No Plaintext Storage

- **No credentials in config files**: API tokens, passwords, and other sensitive data are never stored in plain text
- **No environment variables**: Credentials are not stored in environment variables that could be accidentally exposed
- **Secure retrieval**: Credentials are only retrieved when needed and kept in memory briefly

## Setting Up Credentials

### Interactive Setup

Use the secure setup command for each integration:

```bash
# Setup Confluence credentials
contextflow setup confluence

# Setup JIRA credentials  
contextflow setup jira

# Setup GitHub credentials
contextflow setup github

# Setup Notion credentials
contextflow setup notion

# Setup Slack credentials
contextflow setup slack
```

### What Gets Stored

**Confluence/JIRA:**
- Username/email
- API token (not password)

**GitHub:**
- Personal access token

**Notion:**
- Integration token

**Slack:**
- Bot token

### Credential Management Commands

```bash
# List stored credentials
contextflow credentials

# Remove credentials for an integration
contextflow remove-credentials confluence

# Remove with confirmation
contextflow remove-credentials github --confirm
```

## API Token Security

### Best Practices

1. **Use API tokens, not passwords**: All integrations use API tokens or OAuth tokens, never passwords
2. **Minimal permissions**: Grant only the permissions needed for ContextFlow functionality
3. **Regular rotation**: Rotate API tokens periodically
4. **Revoke unused tokens**: Remove tokens for integrations you no longer use

### Required Permissions

**GitHub Personal Access Token:**
- `repo` - Access to repositories
- `issues` - Read and write issues

**Atlassian API Token:**
- Confluence space read/write access
- JIRA project read/write access

**Notion Integration Token:**
- Database read/write access

**Slack Bot Token:**
- `chat:write` - Send messages
- `channels:read` - Read channel information

## Configuration File Security

### What's Safe to Store

The `contextflow.yaml` file contains only non-sensitive configuration:

```yaml
project:
  name: "My Project"
  description: "Project description"

integrations:
  github:
    enabled: true
    repository: "user/repo"  # Public information
    # No tokens stored here!
```

### What's Never Stored

- API tokens
- Passwords
- OAuth secrets
- Personal access tokens

## Migration from Plaintext

If you have an existing configuration with plaintext credentials:

1. **Remove credentials from config file**:
   ```yaml
   github:
     enabled: true
     repository: "user/repo"
     # Remove this line: token: "your-token-here"
   ```

2. **Setup secure credentials**:
   ```bash
   contextflow setup github
   ```

3. **Verify setup**:
   ```bash
   contextflow credentials
   ```

## Security Considerations

### Local Machine Security

- **Keyring access**: Anyone with access to your user account can access stored credentials
- **Screen lock**: Always lock your screen when away from your computer
- **Shared computers**: Don't use ContextFlow on shared or public computers

### Network Security

- **HTTPS only**: All API communications use HTTPS
- **No credential transmission**: Credentials are never transmitted in URLs or logs
- **Token validation**: Invalid tokens are rejected without retry

### Backup and Sync

- **Config file backup**: Safe to backup `contextflow.yaml` (no secrets)
- **Credential backup**: Credentials are tied to your local keyring
- **Team sharing**: Each team member must setup their own credentials

## Troubleshooting

### Keyring Issues

**Linux without keyring service:**
```bash
# Install keyring service
sudo apt-get install gnome-keyring  # Ubuntu/Debian
sudo dnf install gnome-keyring      # Fedora
```

**Permission denied errors:**
```bash
# Check keyring access
python3 -c "import keyring; print(keyring.get_keyring())"
```

**Reset credentials:**
```bash
# Remove all credentials for fresh start
contextflow remove-credentials confluence --confirm
contextflow remove-credentials jira --confirm
contextflow remove-credentials github --confirm
```

### Integration Failures

**"Credentials not configured" errors:**
1. Run `contextflow credentials` to check what's stored
2. Run `contextflow setup <integration>` to add missing credentials
3. Verify API token permissions in the service's settings

**Authentication failures:**
1. Check if API token is still valid
2. Verify token permissions
3. Re-run setup to update credentials

## Reporting Security Issues

If you discover a security vulnerability in ContextFlow:

1. **Do not** create a public GitHub issue
2. Email security concerns to: security@contextflow.dev
3. Include detailed information about the vulnerability
4. Allow time for investigation and fix before public disclosure

## Security Updates

- Monitor ContextFlow releases for security updates
- Update dependencies regularly: `pip install --upgrade contextflow`
- Review credential permissions periodically
- Rotate API tokens according to your organization's security policy

---

**Remember**: Security is a shared responsibility. ContextFlow provides secure storage, but you must follow best practices for API token management and local machine security.
