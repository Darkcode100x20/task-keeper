# Testing Guide

## Setup

1. Install test dependencies:
```bash
pip install -r test-requirements.txt
export FLASK_ENV=testing
export DATABASE_URL=sqlite:///test.db
```

## Test structure

### Unit Tests (tests/test_basics.py)
Test basic application 
```python
def test_adding_new_todo():
    todo = Todo(description="Test todo", todolist_id=1).save()
    assert todo.description == "Test todo"
    assert not todo.is_finished
```
### API Tests (tests/test_api.py)
Tests REST API endpoints
```python
def test_get_todos():
    response = self.client.get('/api/todos/')
    assert response.status_code == 200
    assert 'todos' in response.json
```
### Integration Tests (tests/test_client.py)
Test full application flow:
```python
def test_user_workflow():
    # Register
    response = self.register_user("testuser")
    assert response.status_code == 302
    
    # Login
    response = self.login_user("testuser")
    assert response.status_code == 302
```
## Running Tests 
All tests
```bash
python -m pytest
```
Specific Test File
```bash
python -m pytest tests/test_api.py
```
Specific Test Case
```bash
python -m pytest tests/test_api.py::TodolistAPITestCase::test_get_todos
```
## Test Categories 
### Authentication Tests
- User registration
- Login / Logout
- Password validation
- Session management
### Todo List Test 
- Creating lists
- Adding todos
- Making todos complete
- List permissions
### API Tests
- Endpoint responses
- Data validation
- Error handling
- Authentication requirements

## Example Test cases
### Test API Endpoints
```python
def test_create_todo():
    response = self.client.post(
        url_for('api.add_todo'),
        json={
            'description': 'New todo',
            'todolist_id': 1
        },
        headers={'Content-Type': 'application/json'}
    )
    assert response.status_code == 201
    assert 'description' in response.json
```
### Testing authentication
```python
def test_invalid_login():
    response = self.client.post(
        url_for('auth.login'),
        data={
            'email': 'wrong@example.com',
            'password': 'wrongpassword'
        }
    )
    assert response.status_code == 401
```
### Testing Models
```python
def test_todo_completion():
    todo = Todo(description="Test todo", todolist_id=1).save()
    todo.finished()
    assert todo.is_finished
    assert todo.finished_at is not None
```
### Coverage reports
Generate coverage report
```bash
coverage run -m pytest
coverage report
coverage html  # Generates detailed HTML report
```
## Common issues and solutions
### Database Cleanup 
```python
def tearDown(self):
    db.session.remove()
    db.drop_all()
```
### Authentication in tests
```python
def login_user(self, name):
    return self.client.post(
        url_for('auth.login'),
        data={
            'email_or_username': name + '@example.com',
            'password': 'correcthorsebatterystaple'
        }
    )
```