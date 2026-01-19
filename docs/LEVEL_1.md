# Level 1: Simple Assertion Tests

**Duration:** ~10 minutes

## Concept

Simple assertion tests verify basic behavior:
- Default values are correct
- Functions return expected outputs
- Data structures contain expected data

## Key Patterns

### Basic Assertions

```python
# equality
assert result == expected

# identity
assert result is None
assert result is not None

# truthiness
assert result  # truthy
assert not result  # falsy

# containment
assert item in collection
assert key in dictionary

# type checking
assert isinstance(result, MyClass)
```

### Testing Pydantic Models

```python
from my_module import MyModel

def test_model_defaults():
    """Test default values are set correctly."""
    model = MyModel()
    
    assert model.name == "default"
    assert model.count == 0

def test_model_accepts_values():
    """Test custom values override defaults."""
    model = MyModel(name="custom", count=5)
    
    assert model.name == "custom"
    assert model.count == 5
```

### Testing Pure Functions

```python
def test_function_returns_expected_type():
    """Verify return type."""
    result = my_function("input")
    
    assert isinstance(result, str)

def test_function_transforms_input():
    """Verify transformation logic."""
    result = uppercase("hello")
    
    assert result == "HELLO"
```

## Examples from Workshop

### Example 1: Testing Default Values

```python
def test_pagination_params_has_correct_defaults(self):
    """Test that PaginationParams has sensible defaults."""
    params = PaginationParams()

    assert params.limit == 10
    assert params.offset == 0
    assert params.sort_order == "asc"
```

### Example 2: Testing Schema Validation

```python
def test_task_create_with_minimal_fields(self):
    """Test TaskCreate with only required fields."""
    task = TaskCreate(title="My Task")

    assert task.title == "My Task"
    assert task.description is None
    assert task.status == TaskStatus.TODO
    assert task.priority == 3  # default
```

### Example 3: Testing Function Behavior

```python
def test_encrypt_password_produces_different_hashes(self):
    """Same password should produce different hashes (due to salt)."""
    password = "mypassword"

    hash1 = encrypt_password(password)
    hash2 = encrypt_password(password)

    # bcrypt salts produce unique hashes
    assert hash1 != hash2
```

## Exercises

Complete these tests in `tests/unit/test_level_1_basics.py`:

1. **TestPaginationHelpers** - Test pagination math functions
2. **TestTaskStatusEnum** - Verify enum values
3. **TestUserResponseSchema** - Test model_validate()
4. **TestRoleEnum** - Verify role values
5. **TestValidationErrorContext** - Test exception context

## Tips

- Start with the simplest assertion
- One logical assertion per test (related asserts are OK)
- Use descriptive test names
- Read example tests for patterns
