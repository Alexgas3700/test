# Contributing to Marketing Email Workflow System

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone <your-fork-url>`
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Run tests: `pytest`
6. Commit your changes: `git commit -m "Add your feature"`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Create a Pull Request

## Development Setup

### Prerequisites

- Python 3.8 or higher
- pip
- virtualenv (recommended)

### Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov black flake8 mypy
```

## Code Style

We follow PEP 8 style guidelines with some modifications:

- Line length: 100 characters
- Use type hints where possible
- Use docstrings for all public functions and classes

### Formatting

Format your code with Black:

```bash
black src/ tests/ examples/
```

### Linting

Check your code with flake8:

```bash
flake8 src/ tests/ examples/
```

### Type Checking

Run mypy for type checking:

```bash
mypy src/
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_subscriber_service.py

# Run specific test
pytest tests/test_subscriber_service.py::test_add_subscriber
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files with `test_` prefix
- Name test functions with `test_` prefix
- Use descriptive test names
- Include docstrings explaining what the test does

Example:

```python
def test_add_subscriber():
    """Test adding a subscriber to the service"""
    service = SubscriberService()
    subscriber = Subscriber(email="test@example.com")
    result = service.add_subscriber(subscriber)
    assert result.email == "test@example.com"
```

## Project Structure

```
.
├── src/
│   ├── config/          # Configuration management
│   ├── models/          # Data models
│   ├── services/        # Business logic
│   ├── templates/       # Email templates
│   ├── workflows/       # Workflow engine
│   └── utils/           # Utility functions
├── examples/            # Usage examples
├── tests/               # Test files
├── README.md
├── QUICKSTART.md
├── CONTRIBUTING.md
└── requirements.txt
```

## Adding New Features

### Adding a New Service

1. Create a new file in `src/services/`
2. Implement the service class
3. Add to `src/services/__init__.py`
4. Write tests in `tests/test_<service_name>.py`
5. Add examples in `examples/`
6. Update documentation

### Adding a New Model

1. Create a new file in `src/models/`
2. Define the model using Pydantic
3. Add to `src/models/__init__.py`
4. Write validation tests
5. Update documentation

### Adding a New Workflow Template

1. Add to `src/workflows/workflow_builder.py`
2. Add to `WorkflowTemplates` class
3. Write tests
4. Add example usage
5. Update documentation

## Documentation

### Docstring Format

Use Google-style docstrings:

```python
def send_email(to: str, subject: str, body: str) -> bool:
    """Send an email to a recipient.
    
    Args:
        to: Email address of the recipient
        subject: Email subject line
        body: Email body content
    
    Returns:
        True if email was sent successfully, False otherwise
    
    Raises:
        ValueError: If email address is invalid
    """
    pass
```

### Updating Documentation

- Update README.md for major features
- Update QUICKSTART.md for user-facing changes
- Add examples for new features
- Update type hints and docstrings

## Pull Request Process

1. **Update tests**: Ensure all tests pass and add new tests for your changes
2. **Update documentation**: Update relevant documentation files
3. **Follow code style**: Run Black and flake8
4. **Write clear commit messages**: Use descriptive commit messages
5. **Keep PRs focused**: One feature or fix per PR
6. **Add examples**: Include usage examples for new features

### PR Title Format

- `feat: Add new feature`
- `fix: Fix bug in component`
- `docs: Update documentation`
- `test: Add tests for feature`
- `refactor: Refactor component`
- `style: Format code`

### PR Description

Include:
- What changes were made
- Why the changes were necessary
- How to test the changes
- Any breaking changes
- Related issues

## Code Review

All submissions require review. We use GitHub pull requests for this purpose.

Reviewers will check:
- Code quality and style
- Test coverage
- Documentation
- Performance implications
- Security considerations

## Reporting Issues

### Bug Reports

Include:
- Clear description of the bug
- Steps to reproduce
- Expected behavior
- Actual behavior
- Python version and OS
- Error messages and stack traces

### Feature Requests

Include:
- Clear description of the feature
- Use cases and examples
- Why this feature would be useful
- Possible implementation approach

## Community

- Be respectful and inclusive
- Help others learn and grow
- Provide constructive feedback
- Follow the code of conduct

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).

## Questions?

If you have questions about contributing, please open an issue or reach out to the maintainers.

Thank you for contributing! 🎉
