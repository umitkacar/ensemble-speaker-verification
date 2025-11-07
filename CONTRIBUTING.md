# Contributing to Speech Verification Ensemble

Thank you for considering contributing to Speech Verification Ensemble! 🎉

## Development Setup

### 1. Clone the repository

```bash
git clone https://github.com/umitkacar/Speech-Verification-Ensemble.git
cd Speech-Verification-Ensemble
```

### 2. Install Hatch

```bash
pip install hatch
```

### 3. Create development environment

```bash
# Hatch will automatically create a virtual environment
hatch shell
```

### 4. Install pre-commit hooks

```bash
pre-commit install
```

## Development Workflow

### Running Tests

```bash
# Run all tests
hatch run test

# Run with coverage
hatch run test-cov

# Run specific test
hatch run test tests/test_version.py
```

### Code Quality

```bash
# Format code with black
hatch run format

# Check formatting
hatch run format-check

# Lint with ruff
hatch run lint

# Type check with mypy
hatch run type-check

# Run all checks
hatch run all
```

### Running the CLI

```bash
# Install in development mode
pip install -e .

# Or run directly
hatch run speech-verify --help
```

## Code Style

We follow:
- **Black** for code formatting (line length: 88)
- **Ruff** for linting
- **MyPy** for type checking
- **Google style** for docstrings

### Example Code Style

```python
"""Module docstring."""

import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


def my_function(
    param1: str,
    param2: int,
    optional_param: Optional[str] = None,
) -> bool:
    """
    Short description of the function.

    Longer description if needed.

    Args:
        param1: Description of param1
        param2: Description of param2
        optional_param: Description of optional parameter

    Returns:
        Description of return value

    Raises:
        ValueError: When something goes wrong
    """
    # Implementation
    pass
```

## Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

Examples:
```
feat(cli): add batch verification command

Add new CLI command for batch processing multiple audio pairs.
Includes progress bar and JSON output support.

Closes #42
```

## Pull Request Process

1. **Fork** the repository
2. **Create a branch** from `main`:
   ```bash
   git checkout -b feature/my-new-feature
   ```
3. **Make your changes** with clear, logical commits
4. **Add tests** for new functionality
5. **Update documentation** if needed
6. **Run all checks**:
   ```bash
   hatch run all
   ```
7. **Push to your fork**:
   ```bash
   git push origin feature/my-new-feature
   ```
8. **Open a Pull Request** with a clear description

## Testing Guidelines

- Write tests for all new features
- Maintain or improve code coverage
- Use descriptive test names
- Group related tests in classes

```python
import pytest

def test_feature_with_valid_input():
    """Test feature with valid input."""
    # Arrange
    input_data = "valid"

    # Act
    result = my_function(input_data)

    # Assert
    assert result is True


def test_feature_with_invalid_input():
    """Test feature raises error with invalid input."""
    with pytest.raises(ValueError):
        my_function("invalid")
```

## Documentation

- Update README.md if adding new features
- Add docstrings to all public functions/classes
- Use type hints everywhere
- Include usage examples

## Questions?

- 💬 Open a [Discussion](https://github.com/umitkacar/Speech-Verification-Ensemble/discussions)
- 🐛 Report bugs via [Issues](https://github.com/umitkacar/Speech-Verification-Ensemble/issues)
- 📧 Contact maintainers

## Code of Conduct

Be respectful, inclusive, and professional. We're all here to learn and improve.

---

Thank you for contributing! 🙏
