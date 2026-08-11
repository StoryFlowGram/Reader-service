# Reader Service — SFG

> Microservice managing user reading library and reading progress. Links users with books from `book-service` and tracks active reader positions across chapters.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Running the Service](#running-the-service)
- [Environment Variables](#environment-variables)
- [API](#api)
- [Project Structure](#project-structure)

---

## Overview

Reader Service serves as the bridge between users and book content:

- **Personal Library Management**: Add or remove books from personal user shelf
- **Reading Progress Tracking**: Persists current chapter ID, paragraph index, and scroll percentage
- **Book Service Integration**: Fetches book metadata via HTTP using `httpx` and internal gateway credentials

---

## Architecture

```
User Action
     │
     ▼
Reader Service
 ├── /user-books  ──▶ Manage personal library
 └── /reading-progress ──▶ Track reading state
        │
        ├── PostgreSQL (reader-db)
        │    user_books, reading_progress
        │
        └── book-service (HTTP)
             fetches book metadata
```

---

## Technology Stack

| Package | Version | Role |
|--------|---------|------|
| `fastapi[all]` | ^0.118.0 | HTTP framework |
| `sqlalchemy` | ^2.0.43 | ORM |
| `asyncpg` | ^0.30.0 | Async PostgreSQL driver |
| `alembic` | ^1.17.0 | Database migrations |
| `httpx` | ^0.28.1 | Async HTTP client |
| `loguru` | ^0.7.3 | Logging |
| Python | ≥ 3.12 | Runtime |

---

## Running the Service

### Locally (Poetry)

```bash
cd Backend/reader-service
cp .env.example .env
poetry install
alembic upgrade head
uvicorn main:app --reload --port 8004
```

### Docker

```bash
docker build -t sfg-reader-service .
docker run -p 8004:8000 --env-file .env sfg-reader-service
```

---

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `READER_DB_USER` | Database user | `reader_user` |
| `READER_DB_PASSWORD` | Database password | `reader_password` |
| `READER_DB_NAME` | Database name | `reader-db` |
| `READER_DB_HOST` | Database host | `reader-db` |
| `READER_BOOK_SERVICE_URL` | Downstream book-service URL | `http://book-service:8000` |
| `INTERNAL_GATEWAY_TOKEN` | Token for inter-service calls | `replace_me` |

---

## API

### `GET /health`

```json
{ "status": "ok", "service": "reader-service" }
```

### User Books — `/user-books`

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/user-books` | List books in user's library |
| `POST` | `/user-books/{book_id}` | Add book to library |
| `DELETE` | `/user-books/{book_id}` | Remove book from library |

### Reading Progress — `/reading-progress`

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/reading-progress/{book_id}` | Get reading progress for a book |
| `PUT` | `/reading-progress/{book_id}` | Save/update reading progress |

---

## Project Structure

```
reader-service/
├── main.py                   # FastAPI entrypoint
├── app/
│   ├── domain/               # UserBook & ReadingProgress entities
│   ├── application/          # Use cases for library & progress
│   ├── infrastructure/       # Database models, HTTP clients, DI
│   └── presentation/         # Controllers & API routing
├── alembic/                  # Database migrations
├── Dockerfile
└── pyproject.toml
```
