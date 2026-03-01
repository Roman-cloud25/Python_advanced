# FastAPI + SQLAlchemy + Alembic: Categories & Questions API

A FastAPI-based API for managing categories and questions with a **one-to-many** database relationship (one category can have multiple questions).

---

## Features

- **Database Models**: Implemented `categories` and `questions` tables using **SQLAlchemy 2.0**.
- **Migrations**: Configured **Alembic** for database schema versioning.
- **REST API**: FastAPI endpoints for:
  - Creating categories
  - Adding questions
  - Fetching all questions
- **Data Validation**: Used **Pydantic** for request/response schema validation.
