# Level 3: Mocking and Patching

**Duration:** ~10 minutes

## Concept

Mocking allows you to replace dependencies with test doubles, enabling:
- Testing without a real database
- Controlling external service responses
- Verifying function calls

## Key Patterns

### Creating Mock Objects

```python
from unittest.mock import Mock, MagicMock

# basic mock
mock_obj = Mock()
mock_obj.some_method.return_value = "result"

# MagicMock auto-creates attributes
magic_mock = MagicMock()
magic_mock.nested.deeply.method.return_value = 42
```

### Using patch() Decorator

```python
from unittest.mock import patch

@patch("my_module.external_function")
def test_uses_external(mock_external):
    """Replace external_function during test."""
    mock_external.return_value = "mocked"
    
    result = my_function()
    
    assert result == "mocked"
    mock_external.assert_called_once()
```

### Using patch() Context Manager

```python
def test_with_context():
    with patch("my_module.external") as mock_ext:
        mock_ext.return_value = "value"
        result = my_function()
    
    assert result == "value"
```

### Mocking a Database Session

```python
def test_service_with_mock_session():
    # arrange
    mock_session = Mock()
    mock_user = Mock()
    mock_user.name = "John"
    
    # configure query chain
    mock_session.execute.return_value.scalar_one_or_none.return_value = mock_user
    
    # act
    result = get_user(mock_session, "john")
    
    # assert
    assert result.name == "John"
    mock_session.execute.assert_called_once()
```

### Verifying Calls

```python
# was called?
mock.method.assert_called()
mock.method.assert_called_once()
mock.method.assert_not_called()

# with specific args?
mock.method.assert_called_with("arg1", key="value")
mock.method.assert_called_once_with("arg1")

# call count
assert mock.method.call_count == 3

# inspect all calls
mock.method.call_args_list  # list of call objects
```

## Examples from Workshop

### Example 1: Mocking Database Session

```python
def test_get_user_by_username_with_mock_session(self):
    """Test user lookup with mocked database session."""
    # arrange
    mock_session = Mock()
    mock_user = Mock(spec=User)
    mock_user.username = "testuser"

    mock_session.execute.return_value.scalar_one_or_none.return_value = mock_user

    # act
    result = get_user_by_username(mock_session, "testuser")

    # assert
    assert result.username == "testuser"
    mock_session.execute.assert_called_once()
```

### Example 2: Patching Settings

```python
@patch("project.security.get_settings")
def test_create_access_token_uses_settings(self, mock_get_settings):
    """Test that create_access_token uses settings."""
    mock_settings = Mock()
    mock_settings.SECRET_KEY = "test-secret"
    mock_settings.ALGORITHM = "HS256"
    mock_get_settings.return_value = mock_settings

    payload = TokenPayload(username="test", role="user", user_uuid="123")
    token = create_access_token(payload)

    assert token.access_token is not None
    mock_get_settings.assert_called()
```

### Example 3: Multiple Patches

```python
@patch("project.security.get_settings")
@patch("project.security.jwt.encode")
def test_token_payload_structure(self, mock_encode, mock_get_settings):
    """Test JWT payload contains expected fields."""
    mock_settings = Mock()
    mock_settings.SECRET_KEY = "secret"
    mock_settings.ALGORITHM = "HS256"
    mock_get_settings.return_value = mock_settings
    mock_encode.return_value = "mock-token"

    payload = TokenPayload(username="john", role="admin", user_uuid="123")
    create_access_token(payload)

    # inspect what was passed to jwt.encode
    call_args = mock_encode.call_args[0][0]
    assert call_args["username"] == "john"
    assert "exp" in call_args
```

## Exercises

Complete these tests in `tests/unit/test_level_3_mocking.py`:

1. **TestAuthServiceWithMocks** - Mock user lookup and password verify
2. **TestDependenciesWithMocks** - Mock token decode and user service
3. **TestTokenExpirationWithPatchedDatetime** - Patch datetime.now()
4. **TestTaskServiceCreateWithMocks** - Verify session method calls

## Tips

- Patch where the function is **used**, not where it's defined
- Use `spec=` to make mocks stricter (catches typos)
- Order of `@patch` decorators is reversed in function args
- `MagicMock` is useful for complex objects with many attributes
- Keep patches minimal - only mock what you need
