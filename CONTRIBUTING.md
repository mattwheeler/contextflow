# Contributing to ContextFlow

Thanks for your interest in contributing to ContextFlow! This guide will help you get started.

## Development Workflow

### Branch Structure

- **`main`** - Production-ready code, protected branch
- **`develop`** - Integration branch for new features
- **`feature/*`** - Feature development branches
- **`bugfix/*`** - Bug fix branches
- **`hotfix/*`** - Critical fixes for production

### Getting Started

1. **Fork the repository**
   ```bash
   # Fork on GitHub, then clone your fork
   git clone https://github.com/YOUR-USERNAME/contextflow.git
   cd contextflow
   ```

2. **Set up development environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   pip install -e .
   ```

3. **Create feature branch from develop**
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/your-feature-name
   ```

### Making Changes

1. **Write code**
   - Follow existing code style
   - Add docstrings to new functions/classes
   - Keep functions focused and small

2. **Test your changes**
   ```bash
   # Run the demo to test basic functionality
   python demo.py
   
   # Test CLI commands
   contextflow --help
   contextflow init --template minimal
   ```

3. **Update documentation**
   - Update README.md if needed
   - Add/update docstrings
   - Update examples if behavior changes

### Submitting Changes

1. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add feature: brief description
   
   - Detailed change 1
   - Detailed change 2
   - Fixes #issue-number (if applicable)"
   ```

2. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create Pull Request**
   - Target the `develop` branch (not `main`)
   - Fill out the PR template
   - Link any related issues

## Code Style

### Python Style
- Follow PEP 8
- Use type hints where helpful
- Maximum line length: 100 characters
- Use descriptive variable names

### Documentation Style
- Use clear, concise language
- Include examples for complex features
- Keep README.md up to date
- Document security considerations

### Commit Messages
```
Type: Brief description (50 chars max)

Detailed explanation of what changed and why.
- Use bullet points for multiple changes
- Reference issues with #123
- Explain the reasoning behind changes

Fixes #123
```

**Types:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (no logic changes)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

## Security Guidelines

### Credential Handling
- **Never commit credentials** in any form
- Use keyring for secure storage
- Test credential setup/removal flows
- Document security implications

### Code Security
- Validate all user inputs
- Use secure defaults
- Avoid hardcoded secrets
- Review dependencies for vulnerabilities

## Testing

### Manual Testing
```bash
# Test basic workflow
contextflow init --template side-project
contextflow setup github  # Use test token
contextflow context --quick
contextflow update "Test session"
contextflow status
```

### Integration Testing
- Test with real APIs (use test accounts)
- Verify credential storage/retrieval
- Test error handling
- Check cross-platform compatibility

## Release Process

### For Maintainers Only

1. **Prepare release**
   ```bash
   git checkout develop
   git pull origin develop
   
   # Update version in setup.py and __init__.py
   # Update CHANGELOG.md
   ```

2. **Create release PR**
   ```bash
   git checkout -b release/v1.x.x
   git commit -m "Prepare release v1.x.x"
   git push origin release/v1.x.x
   
   # Create PR: release/v1.x.x -> main
   ```

3. **After merge to main**
   ```bash
   git checkout main
   git pull origin main
   git tag v1.x.x
   git push origin v1.x.x
   
   # Merge main back to develop
   git checkout develop
   git merge main
   git push origin develop
   ```

## Issue Guidelines

### Bug Reports
- Use the bug report template
- Include steps to reproduce
- Provide system information
- Include relevant logs (no credentials!)

### Feature Requests
- Use the feature request template
- Explain the use case
- Consider implementation complexity
- Discuss alternatives

### Security Issues
- **Do not** create public issues for security vulnerabilities
- Email matt.wheeler70@gmail.com directly
- Include detailed reproduction steps
- Allow time for investigation and fix

## Community Guidelines

### Be Respectful
- Use inclusive language
- Be patient with newcomers
- Provide constructive feedback
- Help others learn

### Stay Focused
- Keep discussions on-topic
- Use appropriate channels (issues vs discussions)
- Search before creating new issues
- Follow up on your contributions

## Getting Help

### Documentation
- Read the README.md
- Check docs/ directory
- Review examples/

### Communication
- GitHub Issues for bugs and features
- GitHub Discussions for questions
- Email matt.wheeler70@gmail.com for security issues

### Development Questions
- Check existing issues and PRs
- Look at the code for examples
- Ask specific questions with context

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes for significant contributions
- GitHub contributor graphs

Thank you for contributing to ContextFlow! 🚀
