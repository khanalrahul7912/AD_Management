# Contributing to AD Management System

Thank you for your interest in contributing to the AD Management System! This document provides guidelines for contributing to the project.

## Code of Conduct

Be respectful and constructive in all interactions. We're all here to build better software together.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- A clear, descriptive title
- Steps to reproduce the problem
- Expected behavior
- Actual behavior
- Your environment (OS, Python version, AD server type)
- Any relevant logs or error messages

### Suggesting Enhancements

Enhancement suggestions are welcome! Please create an issue with:
- A clear, descriptive title
- Detailed description of the proposed feature
- Use cases and benefits
- Any implementation ideas you have

### Pull Requests

1. **Fork the repository** and create your branch from `main`
   ```bash
   git checkout -b feature/my-new-feature
   ```

2. **Make your changes**
   - Follow the existing code style
   - Add comments for complex logic
   - Update documentation if needed

3. **Test your changes**
   - Ensure existing functionality still works
   - Test your new feature thoroughly
   - Run the test suite: `python test_app.py`

4. **Commit your changes**
   ```bash
   git commit -m "Add new feature: description"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/my-new-feature
   ```

6. **Create a Pull Request**
   - Provide a clear description of the changes
   - Reference any related issues
   - Include screenshots for UI changes

## Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/khanalrahul7912/AD_Management.git
   cd AD_Management
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your AD settings
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

## Code Style Guidelines

### Python Code
- Follow PEP 8 style guide
- Use meaningful variable and function names
- Maximum line length: 100 characters
- Use docstrings for functions and classes
- Add type hints where appropriate

Example:
```python
def get_user(username: str) -> dict:
    """
    Retrieve user information from Active Directory.
    
    Args:
        username: The sAMAccountName of the user
        
    Returns:
        Dictionary containing user information
    """
    # Implementation
```

### HTML Templates
- Use proper indentation (2 spaces)
- Follow Jinja2 best practices
- Keep templates DRY (Don't Repeat Yourself)
- Use semantic HTML5 elements

### JavaScript
- Use modern ES6+ syntax
- Add comments for complex logic
- Keep files focused and modular

## Project Structure

```
AD_Management/
├── app/
│   ├── __init__.py          # Application factory
│   ├── ad_manager.py        # AD operations
│   ├── auth.py              # Authentication
│   ├── users.py             # User management
│   ├── groups.py            # Group management
│   ├── computers.py         # Computer management
│   ├── decorators.py        # Custom decorators
│   └── templates/           # HTML templates
├── config.py                # Configuration
├── app.py                   # Entry point
└── requirements.txt         # Dependencies
```

## Testing

### Running Tests
```bash
python test_app.py
```

### Writing Tests
- Add tests for new features
- Ensure tests are reproducible
- Use descriptive test names

## Documentation

- Update README.md for user-facing changes
- Update DEPLOYMENT.md for deployment-related changes
- Add inline comments for complex code
- Update docstrings when modifying functions

## Git Commit Messages

Write clear, concise commit messages:
- Use present tense ("Add feature" not "Added feature")
- First line should be 50 characters or less
- Reference issues and pull requests when relevant

Examples:
```
Add user password reset functionality

Fix group member removal bug (#123)

Update documentation for deployment

Improve error handling in AD connection
```

## Areas for Contribution

We especially welcome contributions in these areas:

### Features
- [ ] Organizational Unit (OU) management
- [ ] Bulk user operations (import/export CSV)
- [ ] User photo/avatar management
- [ ] Advanced search filters
- [ ] Audit logging
- [ ] Email notifications
- [ ] Multi-factor authentication
- [ ] REST API endpoints
- [ ] Custom reports and dashboards

### Improvements
- [ ] Enhanced error messages
- [ ] Better mobile responsiveness
- [ ] Performance optimizations
- [ ] Internationalization (i18n)
- [ ] Dark mode theme
- [ ] Advanced permission system
- [ ] Connection pooling optimization

### Testing
- [ ] Unit tests
- [ ] Integration tests
- [ ] End-to-end tests
- [ ] Load testing

### Documentation
- [ ] Video tutorials
- [ ] More code examples
- [ ] Troubleshooting guide
- [ ] API documentation

## Questions?

If you have questions about contributing, feel free to:
- Open an issue for discussion
- Contact the maintainers
- Check existing issues and pull requests

## License

By contributing to this project, you agree that your contributions will be licensed under the project's MIT License.

## Recognition

Contributors will be recognized in the project README and release notes.

Thank you for contributing to AD Management System! 🎉
