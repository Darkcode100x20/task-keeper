"""
Database models for the TodoList application.
This module defines models for User, TodoList, and Todolist, along with their relationships,
validation logic, and utilities. It includes core functionality such as:
- User authentication and admin management
- Todolist list creation, retrieval, and deletion
- Todolist item creation, status updates (open/finished), and tracking
"""

import re
from datetime import datetime
from pytz import UTC
from flask import url_for
from flask_login import UserMixin
from sqlalchemy.orm import synonym
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login_manager

# Regular expressions for input validation
EMAIL_REGEX = re.compile(r"^\S+@\S+\.\S+$")  # Matches a standard email format
USERNAME_REGEX = re.compile(r"^\S+$")        # Ensures no whitespace in username input


class Todolist:
    """Simple Todolist class for basic task representation without database integration."""
    def __init__(self, task, created_at=None):
        self.task = task
        self.created_at = created_at or datetime.now(UTC)


def check_length(attribute, length):
    """
    Validates the length of an attribute.

    Args:
        attribute (str): The string to check.
        length (int): Maximum allowed length.

    Returns:
        bool: True if attribute exists and length is within the limit, False otherwise.
    """
    try:
        return bool(attribute) and len(attribute) <= length
    except:
        return False


class BaseModel:
    """
    Base model class providing common database operations.
    Implements save, delete, and from_dict convenience methods.
    """

    def __commit(self):
        """
        Internal helper method that attempts to commit the current session to the database.
        If an IntegrityError occurs, the transaction is rolled back.
        """
        from sqlalchemy.exc import IntegrityError
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    def delete(self):
        """
        Removes the current model instance from the database and commits the change.
        """
        db.session.delete(self)
        self.__commit()

    def save(self):
        """
        Persists the current model instance to the database.
        Returns:
            self: For method chaining.
        """
        db.session.add(self)
        self.__commit()
        return self

    @classmethod
    def from_dict(cls, model_dict):
        """
        Creates a new model instance from a dictionary of attributes and saves it.

        Args:
            model_dict (dict): A dictionary of attributes to set on the model.

        Returns:
            BaseModel: A new instance of the model populated with given attributes.
        """
        return cls(**model_dict).save()


class User(UserMixin, db.Model, BaseModel):
    """
    User model for authentication and Todolist list management.
    This model includes:
    - Username and email validation
    - Password hashing and verification
    - Tracking member since and last seen times
    - Admin privileges management
    """

    __tablename__ = "user"

    # Database columns
    id = db.Column(db.Integer, primary_key=True)
    _username = db.Column("username", db.String(64), unique=True)
    _email = db.Column("email", db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    member_since = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)

    # Relationships
    Todolists = db.relationship("TodoList", backref="user", lazy="dynamic")

    def __repr__(self):
        """String representation showing admin status and username."""
        if self.is_admin:
            return f"<Admin {self.username}>"
        return f"<User {self.username}>"

    @property
    def username(self):
        """
        Gets the username of the user.

        Returns:
            str: The username.
        """
        return self._username

    @username.setter
    def username(self, username):
        """
        Sets the username, ensuring it meets length and format requirements.

        Args:
            username (str): The desired username.

        Raises:
            ValueError: If the username is invalid or too long.
        """
        is_valid_length = check_length(username, 64)
        if not is_valid_length or not bool(USERNAME_REGEX.match(username)):
            raise ValueError(f"{username} is not a valid username")
        self._username = username

    username = synonym("_username", descriptor=username)

    @property
    def email(self):
        """
        Gets the email address of the user.

        Returns:
            str: The user's email.
        """
        return self._email

    @email.setter
    def email(self, email):
        """
        Sets the email address, ensuring it meets length and format requirements.

        Args:
            email (str): The desired email address.

        Raises:
            ValueError: If the email is invalid or too long.
        """
        if not check_length(email, 64) or not bool(EMAIL_REGEX.match(email)):
            raise ValueError(f"{email} is not a valid email address")
        self._email = email

    email = synonym("_email", descriptor=email)

    @property
    def password(self):
        """
        Prevents access to the password attribute.

        Raises:
            AttributeError: Password is not readable.
        """
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        """
        Hashes and sets the user's password.

        Args:
            password (str): The plaintext password.

        Raises:
            ValueError: If no password is provided or if the hashed password is too long.
        """
        if not bool(password):
            raise ValueError("no password given")

        hashed_password = generate_password_hash(password)
        if len(hashed_password) > 256:
            raise ValueError("not a valid password, hash is too long")
        self.password_hash = hashed_password

    def verify_password(self, password):
        """
        Checks if the provided plaintext password matches the stored hash.

        Args:
            password (str): The password to verify.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return check_password_hash(self.password_hash, password)

    def seen(self):
        """
        Updates the user's last seen timestamp to the current time and saves it.

        Returns:
            User: The updated user instance.
        """
        self.last_seen = datetime.now(UTC)
        return self.save()

    def to_dict(self):
        """
        Converts the user model into a dictionary suitable for JSON responses.

        Returns:
            dict: Dictionary containing user data and related URLs.
        """
        return {
            "username": self.username,
            "user_url": url_for("api.get_user", username=self.username, _external=True),
            "member_since": self.member_since,
            "last_seen": self.last_seen,
            "Todolists": url_for("api.get_user_Todolists", username=self.username, _external=True),
            "Todolist_count": self.Todolists.count(),
        }

    def promote_to_admin(self):
        """
        Grants admin privileges to the user and saves the change.

        Returns:
            User: The updated user instance with admin privileges.
        """
        self.is_admin = True
        return self.save()


@login_manager.user_loader
def load_user(user_id):
    """
    Flask-Login user loader callback.
    Given a user ID, returns the corresponding User object or None if not found.
    """
    return User.query.get(int(user_id))


class TodoList(db.Model, BaseModel):
    """
    Represents a Todolist list, which holds a set of Todolist items.
    Each list has a creator and a title, and tracks created_at timestamps.
    """

    __tablename__ = "Todolist"
    id = db.Column(db.Integer, primary_key=True)
    _title = db.Column("title", db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    creator = db.Column(db.String(64), db.ForeignKey("user.username"))
    todos = db.relationship("Todolist", backref="Todolist", lazy="dynamic")

    def __init__(self, title=None, creator=None, created_at=None):
        """
        Initializes a TodoList instance.

        Args:
            title (str, optional): The title of the Todolist list.
            creator (str, optional): The username of the creator.
            created_at (datetime, optional): When the list was created.
        """
        self.title = title or "untitled"
        self.creator = creator
        self.created_at = created_at or datetime.now(UTC)

    def __repr__(self):
        """
        String representation of the Todolist list object.

        Returns:
            str: A string showing the title of the Todolist list.
        """
        return f"<Todolist: {self.title}>"

    @property
    def title(self):
        """
        Gets the title of the Todolist list.

        Returns:
            str: The Todolist list title.
        """
        return self._title

    @title.setter
    def title(self, title):
        """
        Sets the title of the Todolist list, ensuring it meets length requirements.

        Args:
            title (str): The desired title.

        Raises:
            ValueError: If the title is invalid or too long.
        """
        if not check_length(title, 128):
            raise ValueError(f"{title} is not a valid title")
        self._title = title

    title = synonym("_title", descriptor=title)

    @property
    def todos_url(self):
        """
        Provides the URL endpoint for retrieving todos in this list.

        Returns:
            str: The URL to access this list's todos.
        """
        url = None
        kwargs = dict(Todolist_id=self.id, _external=True)
        if self.creator:
            kwargs["username"] = self.creator
            url = "api.get_user_Todolist_todos"
        return url_for(url or "api.get_Todolist_todos", **kwargs)

    def to_dict(self):
        """
        Converts the Todolist list model into a dictionary suitable for JSON responses.

        Returns:
            dict: Dictionary containing Todolist list data and related statistics.
        """
        return {
            "title": self.title,
            "creator": self.creator,
            "created_at": self.created_at,
            "total_todo_count": self.todo_count,
            "open_todo_count": self.open_count,
            "finished_todo_count": self.finished_count,
            "todos": self.todos_url,
        }

    @property
    def todo_count(self):
        """
        Returns the total number of todos in this list.

        Returns:
            int: The count of all todos in the list.
        """
        return self.todos.order_by(None).count()

    @property
    def finished_count(self):
        """
        Returns the number of finished todos in this list.

        Returns:
            int: The count of finished todos.
        """
        return self.todos.filter_by(is_finished=True).count()

    @property
    def open_count(self):
        """
        Returns the number of open (not finished) todos in this list.

        Returns:
            int: The count of open todos.
        """
        return self.todos.filter_by(is_finished=False).count()


class Todolist(db.Model, BaseModel):
    """
    Represents a single Todolist item in a Todolist list.
    Tracks description, creation time, finish time, and status.
    """

    __tablename__ = "Todolist"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    finished_at = db.Column(db.DateTime, index=True, default=None)
    is_finished = db.Column(db.Boolean, default=False)
    creator = db.Column(db.String(64), db.ForeignKey("user.username"))
    Todolist_id = db.Column(db.Integer, db.ForeignKey("Todolist.id"))

    def __init__(self, description, Todolist_id, creator=None, created_at=None):
        """
        Initializes a Todolist instance.

        Args:
            description (str): The description of the Todolist task.
            Todolist_id (int): The ID of the related TodoList.
            creator (str, optional): The username of the creator.
            created_at (datetime, optional): The creation timestamp.
        """
        self.description = description
        self.Todolist_id = Todolist_id
        self.creator = creator
        self.created_at = created_at or datetime.now(UTC)

    def __repr__(self):
        """
        String representation of the Todolist item, including its status, description, and creator.

        Returns:
            str: A string representation of the Todolist.
        """
        return "<{} Todolist: {} by {}>".format(
            self.status, self.description, self.creator or "None"
        )

    @property
    def status(self):
        """
        Returns the current status of the Todolist.

        Returns:
            str: 'finished' if the Todolist is completed, 'open' otherwise.
        """
        return "finished" if self.is_finished else "open"

    def finished(self):
        """
        Marks this Todolist as finished and updates the finished_at timestamp.
        """
        self.is_finished = True
        self.finished_at = datetime.now(UTC)
        self.save()

    def reopen(self):
        """
        Marks this Todolist as not finished and clears the finished_at timestamp.
        """
        self.is_finished = False
        self.finished_at = None
        self.save()

    def to_dict(self):
        """
        Converts the Todolist model into a dictionary suitable for JSON responses.

        Returns:
            dict: Dictionary containing Todolist data including its status and timestamps.
        """
        return {
            "description": self.description,
            "creator": self.creator,
            "created_at": self.created_at,
            "status": self.status,
        }
