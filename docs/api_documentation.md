# Task Keeper API Documentation

## Base URL
http://localhost:5000/api/
## Authentication
- Authentication required for most endpoints
- Admin privileges needed for deletion operations
- Uses Flask-Login session authentication

## Endpoints

### Users

#### GET /users/
Lists all users.

**Response:**
```json
{
  "users": [
    {
      "username": "john_doe",
      "user_url": "/api/user/john_doe",
      "member_since": "2024-01-01T00:00:00Z",
      "last_seen": "2024-01-02T00:00:00Z",
      "todolists": "/api/user/john_doe/todolists",
      "todolist_count": 5
    }
  ]
}
```

#### Post /users/
Creates new user.

**Request:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password"
}
```

#### DELETE /user/<username>/
Deletes user.

**Request:**
```json
{
  "username": "john_doe"
}
```
## Todo Lists


#### GET /user/<username>/todolists/
Lists user's todo lists.
**Response:** 
```json
{
  "todolists": [
    {
      "title": "Work Tasks",
      "creator": "john_doe",
      "created_at": "2024-01-01T00:00:00Z",
      "total_todo_count": 10,
      "open_todo_count": 5,
      "finished_todo_count": 5,
      "todos": "/api/todolist/1/todos"
    }
  ]
}
```

#### POST /user/<username>/todolists/
Creates new todo lists.
**Request:** 
```json
{
  "title": "Work Tasks"
}
```

#### PUT /todolist/<todolist_id>/
Updates todo list title.
**Request:** 
```json
{
  "title": "Updated Work Tasks"
}
```

#### DELETE /todolist/<todolist_id>/
Deletes todo list (admin only).
**Request:** 
```json
{
  "todolist_id": 1
}
```
## Todos
#### GET /todolist/<todolist_id>/todos/
Lists todos in todo list
**Response:** 
```json
{
  "todos": [
    {
      "description": "Complete documentation",
      "creator": "john_doe",
      "created_at": "2024-01-01T00:00:00Z",
      "status": "open"
    }
  ]
}
```

#### POST /user/<username>/todolist/<todolist_id>/
Creates new todo
**Request:**
```json
{
  "description": "Complete documentation"
}
```

#### PUT /todo/<todo_id>/
Updates todo status
**Request:**
```json
{
  "is_finished": true
}
```

#### DELETE /todo/<todo_id>/
**Request:**
Deletes todo 
```json
{
  "todo_id": 1
}
```
## Error Responses
**All Errors return**
```json
{
  "error": "Error message"
}
```
## Status codes

- 400: Bad request
- 401: Unauthorized
- 403: Forbidden
- 404: Not found
- 500: Internal Server Error