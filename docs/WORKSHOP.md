# Pytest Unit Testing Workshop

**Duration:** ~30 minutes  
**Level:** Beginner to Intermediate

## Introduction

This workshop teaches pytest unit testing patterns through hands-on exercises with a FastAPI application.

### What are Unit Tests?

Unit tests are **isolated, small tests** that verify a single unit of code (function, class, method) works correctly. Key characteristics:

- **Isolated**: No external dependencies (database, network, filesystem)
- **Fast**: Execute in milliseconds
- **Deterministic**: Same input always produces same output
- **Focused**: Test one thing at a time

### Why Unit Test?

- Catch bugs early in development
- Document expected behavior
- Enable safe refactoring
- Faster feedback than integration/e2e tests

## Workshop Structure

| Level | Topic | Time | File |
|-------|-------|------|------|
| 1 | Simple Assertions | 10 min | `test_level_1_basics.py` |
| 2 | Exception Testing | 10 min | `test_level_2_exceptions.py` |
| 3 | Mocking/Patching | 10 min | `test_level_3_mocking.py` |

## Setup

```bash
# activate environment (Poetry v2)
eval "$(poetry env activate)"

# verify pytest works
pytest --version

# run example tests
pytest tests/unit/test_level_1_basics.py -v
```

## Running Tests

### Basic Commands

```bash
# run all tests
pytest

# run specific file
pytest tests/unit/test_level_1_basics.py

# run specific test class
pytest tests/unit/test_level_1_basics.py::TestPaginationParamsDefaults

# run specific test
pytest tests/unit/test_level_1_basics.py::TestPaginationParamsDefaults::test_pagination_params_has_correct_defaults

# verbose output
pytest -v

# stop on first failure
pytest -x

# show print statements
pytest -s
```

### Using Markers

```bash
# run by level
pytest -k level_1 -v
pytest -k level_2 -v
pytest -k level_3 -v

# run all unit tests
pytest -m unit -v
```

### Coverage Reports

```bash
# terminal report
pytest tests/unit/ --cov=project --cov-report=term-missing

# HTML report
pytest tests/unit/ --cov=project --cov-report=html
open htmlcov/index.html  # view in browser
```

## Workshop Levels

### Level 1: Simple Assertions (10 min)

**Goal:** Test pure functions and Pydantic models.

**Concepts:**
- Basic assertions (`assert`, `==`, `is`, `in`)
- Testing default values
- Testing schema validation

See: [LEVEL_1.md](LEVEL_1.md)

### Level 2: Exception Testing (10 min)

**Goal:** Verify functions raise expected exceptions.

**Concepts:**
- `pytest.raises()` context manager
- Checking exception attributes
- Testing validation boundaries

See: [LEVEL_2.md](LEVEL_2.md)

### Level 3: Mocking/Patching (10 min)

**Goal:** Isolate units by replacing dependencies.

**Concepts:**
- `Mock` and `MagicMock`
- `@patch` decorator
- Verifying call counts and arguments

See: [LEVEL_3.md](LEVEL_3.md)

## Best Practices

### What to Test

✅ **Good candidates for unit tests:**
- Pure functions (no side effects)
- Data validation logic
- Business rules
- Exception handling paths
- Edge cases and boundaries

❌ **Skip unit tests for:**
- Simple getters/setters
- Framework code (FastAPI routes work)
- External library behavior
- Code that's trivially correct

### Test Naming

```python
def test_<what>_<expected_behavior>():
    """Descriptive docstring explaining the test."""
    pass

# examples:
def test_pagination_rejects_negative_offset():
def test_create_user_raises_on_duplicate_email():
def test_encrypt_password_produces_unique_hashes():
```

### Test Structure (AAA Pattern)

```python
def test_example():
    # Arrange - set up test data
    user = User(name="John")
    
    # Act - execute the code under test
    result = user.get_greeting()
    
    # Assert - verify the outcome
    assert result == "Hello, John!"
```

## Exercises

Each level has **example tests** (study these) and **exercises** (complete these).

Exercises are marked with `# TODO:` comments and have `pass` as placeholder.

### Tips for Exercises

1. Read the docstring - it explains what to test
2. Look at the example tests above for patterns
3. Run the test with `-v` to see detailed output
4. Use `pytest --tb=short` for cleaner tracebacks

## Further Reading

- [pytest documentation](https://docs.pytest.org/)
- [unittest.mock documentation](https://docs.python.org/3/library/unittest.mock.html)
- [Testing FastAPI](https://fastapi.tiangolo.com/tutorial/testing/)
