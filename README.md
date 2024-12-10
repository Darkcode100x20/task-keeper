# Flask-Todolist

Task Keeper is a simple yet functional To-Do List web application designed to help users manage their daily tasks. It features user authentication, API endpoints, and a minimal UI.

---

## Table of Contents
1. [Features](#features)
2. [Setup Instructions](#setup-instructions)
    - [Using Docker](#using-docker)
    - [Manual Setup](#manual-setup)
3. [Testing Guide](#testing-guide)
4. [API Endpoints Documentation](#api-endpoints-documentation)
5. [GitHub Actions Workflow](#github-actions-workflow)
6. [Technologies and Extensions Used](#technologies-and-extensions-used)
7. [Contributing](#contributing)
8. [License](#license)

---

## Features

- **User Authentication:** Sign up, log in, and manage user accounts.
- **To-Do Lists:** Create, view, update, and delete tasks.
- **RESTful API:** Fully-featured API for task and list management.
- **Responsive UI:** Interactive interface with modern design.
- **Deployment-Ready:** Optimized for production with Render and Gunicorn. Another option is to run the application on Docker

---

## Setup Instructions

### Using Docker

To quickly set up and run the application using Docker:

1. Build the Docker container:
   ```bash
   docker compose build
   docker compose up
2. Access the application at http://localhost:8000.

--- 
## Technologies and Extensions Used

### Backend Framework
- **Flask:** Lightweight WSGI (Web Server Gateway Interface) web application framework enabling rapid development with its flexibility and extensive ecosystem
- **Flask-SQLAlchemy:** SQL toolkit providing ORM (Object Relational Mapping)  functionality and simplified database operations
- **Flask-Migrate:** Database migration handling using Alembic for version control of database schema
- **Flask-Login:** User session management and authentication handling
- **Flask-WTF:** Form handling and validation with CSRF protection. To generate HTML forms with objects and classes 

### Database
- **SQLite:** Development database
- **PostgreSQL:** Production database hosted on Render

### Frontend
- **Skeleton CSS:** Lightweight CSS framework providing responsive grid and basic styling
- **jQuery:** JavaScript library simplifying DOM (Document Object Model) manipulation and AJAX (Asynchronous JavaScript and XML) requests

### Development Tools
- **Python-dotenv:** Environment variable management
- **Flask-Testing:** Unit testing utilities
- **pytest:** Testing framework for comprehensive test coverage

### Deployment & CI/CD
- **Gunicorn:** Production-grade WSGI (Web Server Gateway Interface) HTTP Server
- **Docker:** Containerization for consistent development and deployment environments
- **GitHub Actions:** Automated CI/CD pipeline including:
  - Automated testing
  - Code quality checks
  - Deployment to Render
- **Render:** Cloud platform hosting the production application with automatic deployments

