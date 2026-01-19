# Level 4: Integration Tests

**Duration:** ~10 minutes

## Concept

Integration tests verify that multiple components work together with a real database:
- Service functions execute actual SQL queries
- ORM relationships and mappings work correctly
- Complex filtering and pagination behave as expected
- Data integrity is maintained through CRUD operations

## Key Differences from Unit Tests

| Aspect | Unit Tests | Integration Tests |
|--------|------------|-------------------|
| Database | Mocked | Real SQLite |
| Speed | Fast (ms) | Slower (100ms+) |
| Isolation | Full | Per-test DB |
| Confidence | Logic only | Full stack |

## Key Patterns

### Database Session Fixture

```python
@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    """Creates fresh SQLite DB for each test."""
    engine = create_test_engine()
    setup_test_database(engine)
    
    with Session(engine) as session:
        yield session
        session.rollback()
    
    teardown_test_database(engine)
```

### Arranging Test Data

```python
def test_with_real_data(db_session: Session):
    # arrange: create test entities in database
    user = User(
        uuid=uuid4(),
        username="testuser",
        email="test@example.com",
        password_hash=encrypt_password("pass123"),
        role=Role.USER.value,
    )
    db_session.add(user)
    db_session.commit()
    
    # act: call service with real session
    result = get_user_by_uuid(db_session, user.uuid)
    
    # assert: verify data from database
    assert result.username == "testuser"
```

### Testing Pagination

```python
def test_pagination(db_session: Session, created_user: User):
    # arrange: create many records
    for i in range(15):
        task = Task(title=f"Task {i}", ...)
        db_session.add(task)
    db_session.commit()
    
    # act: paginate
    page1 = get_tasks(db_session, PaginationParams(limit=5, offset=0))
    page2 = get_tasks(db_session, PaginationParams(limit=5, offset=5))
    
    # assert: correct pagination
    assert page1.total == 15
    assert len(page1.results) == 5
    assert len(page2.results) == 5
    
    # pages don't overlap
    page1_ids = {t.uuid for t in page1.results}
    page2_ids = {t.uuid for t in page2.results}
    assert page1_ids.isdisjoint(page2_ids)
```

### Testing Filters

```python
def test_filtering(db_session: Session):
    # arrange: create data with different attributes
    task1 = Task(status=TaskStatus.TODO.value, ...)
    task2 = Task(status=TaskStatus.DONE.value, ...)
    db_session.add_all([task1, task2])
    db_session.commit()
    
    # act: filter
    todo_tasks = get_tasks(
        db_session, 
        pagination,
        status_filter=TaskStatus.TODO,
    )
    
    # assert: only matching records
    assert all(t.status == TaskStatus.TODO.value for t in todo_tasks.results)
```

## Examples from Workshop

### Example 1: Service Creates and Retrieves

```python
def test_user_service_creates_and_retrieves_user(self, db_session: Session):
    """Test full flow: service → ORM → database → ORM."""
    user_data = UserCreate(
        username="newuser",
        email="newuser@example.com",
        password="password123",
        role=Role.USER,
    )
    
    # create through service
    created = user_service.create_user(db_session, user_data)
    
    # verify persisted
    assert created.uuid is not None
    
    # retrieve through service
    retrieved = user_service.get_user_by_uuid(db_session, created.uuid)
    assert retrieved.username == "newuser"
```

### Example 2: Error Handling with Database

```python
def test_service_raises_not_found_for_missing_entity(self, db_session: Session):
    """Verify proper exception when data doesn't exist."""
    non_existent_uuid = uuid4()

    with pytest.raises(EntityNotFoundError) as exc_info:
        user_service.get_user_by_uuid(db_session, non_existent_uuid)

    assert exc_info.value.entity_type == "User"
```

### Example 3: Data Lifecycle

```python
def test_task_lifecycle_maintains_integrity(self, db_session: Session, created_user: User):
    """Test create → update → delete maintains consistency."""
    # CREATE
    task_data = TaskCreate(title="Test", status=TaskStatus.TODO)
    created = task_service.create_task(db_session, task_data, created_user)
    
    # verify in DB
    db_task = db_session.get(Task, created.uuid)
    assert db_task is not None
    
    # UPDATE
    update_data = TaskUpdate(status=TaskStatus.DONE)
    updated = task_service.update_task(db_session, created.uuid, update_data)
    assert updated.status == TaskStatus.DONE.value
    
    # DELETE
    task_service.delete_task(db_session, created.uuid)
    
    # verify gone
    with pytest.raises(EntityNotFoundError):
        task_service.get_task_by_uuid(db_session, created.uuid)
```

## Exercises

Complete these tests in `tests/integration/test_level_4_integration.py`:

1. **test_get_users_returns_all_active_users** - Create users and verify listing
2. **test_task_update_preserves_unset_fields** - Partial updates don't overwrite
3. **test_pagination_empty_results** - Offset beyond data returns empty list

## Tips

- Use fixtures like `created_user`, `created_task` to reduce setup code
- Always commit after adding entities: `db_session.commit()`
- Test both success AND error paths
- Verify data in DB after operations: `db_session.get(Model, uuid)`
- Integration tests are slower - run unit tests first during development
