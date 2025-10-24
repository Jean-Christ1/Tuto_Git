# Contributing to Natural Language to SQL Accelerator

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Testing](#testing)

## Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

### Our Standards

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive criticism
- Accept responsibility and learn from mistakes

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Create a branch** for your changes
4. **Make your changes** and commit them
5. **Push to your fork** and submit a pull request

## Development Setup

### Prerequisites

- Python 3.9+
- Node.js 18+
- Git
- OpenAI or Anthropic API key

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your API keys
```

### Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env
# Edit .env if needed
```

### Running Locally

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

## Coding Standards

### Python (Backend)

- **Style Guide**: Follow PEP 8
- **Docstrings**: Use NumPy-style docstrings for all functions and classes
- **Type Hints**: Use type hints where appropriate
- **Formatting**: Use Black for code formatting
- **Imports**: Use isort for organizing imports
- **Linting**: Use flake8 for linting

Example function:

```python
def process_query(query: str, max_results: int = 100) -> Dict[str, Any]:
    """
    Process a natural language query.

    Parameters
    ----------
    query : str
        Natural language query to process.
    max_results : int, optional
        Maximum number of results to return (default: 100).

    Returns
    -------
    Dict[str, Any]
        Query results with metadata.

    Raises
    ------
    ValueError
        If query is invalid.

    Examples
    --------
    >>> result = process_query("Show all customers")
    >>> print(result['row_count'])
    59
    """
    # Implementation
```

### JavaScript/React (Frontend)

- **Style Guide**: Use ESLint with recommended React settings
- **Formatting**: Use Prettier
- **Components**: Use functional components with hooks
- **Naming**: PascalCase for components, camelCase for functions
- **Documentation**: Add JSDoc comments for complex functions

Example component:

```javascript
/**
 * QueryInput Component
 *
 * Input component for natural language queries.
 *
 * @param {Object} props - Component props
 * @param {Function} props.onSubmit - Callback when query is submitted
 * @param {boolean} props.loading - Loading state
 * @returns {JSX.Element} QueryInput component
 */
const QueryInput = ({ onSubmit, loading }) => {
  // Implementation
};
```

## Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, etc.)
- **refactor**: Code refactoring
- **test**: Adding or updating tests
- **chore**: Maintenance tasks

### Examples

```
feat(backend): add query caching support

Implement Redis-based caching for frequently executed queries
to improve performance.

Closes #123
```

```
fix(frontend): resolve chart rendering issue

Fix bar chart not displaying correctly when data contains
null values.

Fixes #456
```

## Pull Request Process

1. **Update documentation** if you're changing functionality
2. **Add tests** for new features or bug fixes
3. **Ensure all tests pass** before submitting
4. **Update the README.md** if needed
5. **Follow the code style** guidelines
6. **Write a clear PR description** explaining:
   - What changes you made
   - Why you made them
   - How to test them

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How to test these changes

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests pass
```

## Testing

### Backend Tests

```bash
cd backend
pytest tests/ -v --cov=app
```

### Frontend Tests

```bash
cd frontend
npm test
```

### Integration Tests

```bash
# Start services
docker-compose up -d

# Run integration tests
pytest tests/integration/ -v
```

## Code Review Process

1. **At least one maintainer** must approve the PR
2. **All CI checks** must pass
3. **Code must follow** style guidelines
4. **Documentation must be** updated if needed
5. **Tests must be** included and passing

## Development Workflow

1. Create a feature branch from `main`
2. Make your changes
3. Write/update tests
4. Run tests locally
5. Commit your changes
6. Push to your fork
7. Create a pull request
8. Address review feedback
9. Merge after approval

## Issue Guidelines

### Reporting Bugs

Include:
- Clear title and description
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)
- Screenshots if applicable

### Requesting Features

Include:
- Clear use case
- Expected behavior
- Why this would be useful
- Potential implementation ideas

## Project Structure

```
natural-language-to-sql-accelerator/
├── backend/           # Python FastAPI backend
├── frontend/          # React frontend
├── database/          # Database files
├── docs/             # Documentation
└── tests/            # Tests
```

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [LangChain Documentation](https://python.langchain.com/)
- [Tailwind CSS Documentation](https://tailwindcss.com/)

## Questions?

Feel free to:
- Open an issue for questions
- Join our discussions
- Contact the maintainers

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing! 🎉
