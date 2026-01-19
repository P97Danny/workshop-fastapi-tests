# Level 2: Exception Testing

**Duration:** ~10 minutes

## Concept

Exception testing verifies that code raises expected exceptions when given invalid input or encountering error conditions.

## Key Patterns

### pytest.raises() Basic Usage

```python
import pytest

def test_raises_value_error():
    """Test that function raises ValueError."""
    with pytest.raises(ValueError):
        my_function("invalid input")
```

### Checking Exception Details

```python
def test_raises_with_message():
    """Test exception message content."""
    with pytest.raises(ValueError) as exc_info:
        my_function("bad")
    
    assert "invalid" in str(exc_info.value)

def test_raises_with_attributes():
    """Test custom exception attributes."""
    with pytest.raises(MyCustomError) as exc_info:
        my_function("bad")
    
    assert exc_info.value.error_code == 123
```

### Testing Pydantic Validation

```python
from pydantic import ValidationError

def test_model_rejects_invalid_input():
    """Test Pydantic raises ValidationError."""
    with pytest.raises(ValidationError) as exc_info:
        MyModel(age=-1)
    
    errors = exc_info.value.errors()
    assert len(errors) == 1
    assert errors[0]["loc"] == ("age",)
```

### Testing Boundaries

```python
def test_rejects_value_below_minimum():
    """Test lower boundary."""
    with pytest.raises(ValidationError):
        MyModel(count=0)  # must be > 0

def test_accepts_minimum_value():
    """Test at boundary (no exception)."""
    model = MyModel(count=1)  # exactly at minimum
    assert model.count == 1
```

## Examples from Workshop

### Example 1: Validation Boundary

```python
def test_pagination_rejects_negative_offset(self):
    """PaginationParams should reject negative offset."""
    with pytest.raises(PydanticValidationError) as exc_info:
        PaginationParams(offset=-1)

    errors = exc_info.value.errors()
    assert len(errors) == 1
    assert errors[0]["loc"] == ("offset",)
```

### Example 2: Custom Exception

```python
def test_entity_not_found_stores_entity_type(self):
    """EntityNotFoundError should store entity_type attribute."""
    error = EntityNotFoundError("Task", "abc-123")

    assert error.entity_type == "Task"
    assert error.identifier == "abc-123"
```

### Example 3: Function That Raises

```python
def test_entity_not_found_can_be_raised_and_caught(self):
    """EntityNotFoundError should be raiseable and catchable."""

    def lookup_user(user_id: str):
        raise EntityNotFoundError("User", user_id)

    with pytest.raises(EntityNotFoundError) as exc_info:
        lookup_user("nonexistent")

    assert exc_info.value.entity_type == "User"
```

## Exercises

Complete these tests in `tests/unit/test_level_2_exceptions.py`:

1. **TestSettingsValidation** - Test config validation errors
2. **TestAuthenticationError** - Test auth exception defaults
3. **TestAuthorizationError** - Test role requirement storage
4. **TestValidationErrorField** - Test field context
5. **TestTaskCreateTitleValidation** - Test string length limits

## Tips

- Always use `pytest.raises()` as a context manager
- Access exception with `exc_info.value`
- For Pydantic, use `exc_info.value.errors()` for details
- Test both failure AND success at boundaries
