User Registration and Login: Allows users to register and login using their credentials.
JWT Authentication: Secures endpoints using JWT tokens.
CRUD Operations: Supports Create, Read, and Update for students, courses, attendance logs, and users.
Automatic First User Creation: When the application is run for the first time, an initial user (admin) is automatically created.
Logging: Logs various events in the system.
Error Handling: Catches and logs errors in the system.
Test Coverage: Includes tests for user registration, login, and protected routes.

Backend: Python, Flask
Database: SQLite (SQLAlchemy as ORM)
Authentication: JWT (JSON Web Token)
Testing: pytest
Logging: Built-in Python logging
