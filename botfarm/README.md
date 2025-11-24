# Botfarm Microservice

A RESTful microservice for managing bot users (test credentials) used in E2E testing. Provides endpoints to create users, list them, acquire/release locks to prevent concurrent usage during tests.

Built with:
- **FastAPI** (async)
- **SQLAlchemy 2.0** (async ORM)
- **PostgreSQL 14+** (asyncpg driver)
- **Pydantic v2** (validation/schemas)
- **Alembic** (migrations)
- **pytest** (>75% coverage)
- **Docker** (containerized deployment)

## Features

- UUID-based users with hashed passwords (bcrypt)
- Enum-constrained environments (`prod`, `preprod`, `stage`) and domains (`canary`, `regular`)
- Atomic locking with `locktime` timestamp
- Dependency injection for DB sessions
- Input validation and error handling (409 for locked users, 400 for duplicates)
- Health check endpoint
- CORS enabled
- In-memory SQLite tests

## Project Structure

```
/botfarm
├── app/
│   ├── __init__.py
│   ├── core/
│   │   ├── config.py          # Pydantic settings (.env)
│   │   ├── database.py        # Async engine/session/lifespan
│   │   └── security.py        # Password hashing
│   ├── crud/
│   │   └── user.py            # CRUD operations
│   ├── models/
│   │   └── user.py            # SQLAlchemy User model
│   ├── routers/
│   │   └── users.py           # API routes
│   └── schemas/
│       └── user.py            # Pydantic schemas
├── alembic/                   # Migrations
├── tests/                     # pytest suite
├── main.py                    # FastAPI app
├── requirements.txt
├── alembic.ini
├── pytest.ini
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Quick Start

### 1. Prerequisites
- Python 3.10+
- PostgreSQL 14+ (or Docker)
- Docker & docker-compose (recommended)

### 2. Setup Environment
```bash
cp .env.example .env  # Create if missing
```

Example `.env`:
```
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/botfarm
PROJECT_NAME=Botfarm
LOG_LEVEL=INFO
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
#### Option A: Alembic Migrations (Recommended)
```bash
alembic upgrade head
```

#### Option B: Auto-create Tables (Development)
Tables auto-create on startup via lifespan event.

### 5. Run Server
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Open http://localhost:8000/docs for interactive API docs (Swagger).

### 6. Docker Deployment
```bash
docker-compose up -d
```

See `docker-compose.yml` for Postgres + app services.

## API Endpoints

All under `/api/v1/users`

| Method | Endpoint              | Description                  | Response |
|--------|-----------------------|------------------------------|----------|
| POST   | `/`                  | Create user                 | 201 User |
| GET    | `/`                  | List all users              | 200 [User] |
| POST   | `/{user_id}/acquire` | Lock user (if available)    | 200 {message} or 409 Conflict |
| POST   | `/{user_id}/release` | Unlock user                 | 200 {message} or 404 Not Found |

**User Schema Example:**
```json
{
  "id": "uuid",
  "login": "user@example.com",
  "project_id": "uuid",
  "env": "prod",
  "domain": "canary",
  "created_at": "2024-01-01T00:00:00Z",
  "locktime": null
}
```

**Create Request:**
```json
{
  "login": "test@example.com",
  "password": "securepass123",
  "project_id": "550e8400-e29b-41d4-a716-446655440000",
  "env": "stage",
  "domain": "regular"
}
```

## Testing

```bash
pytest  # Runs tests with coverage >75%
```

- Uses in-memory SQLite for isolation
- Covers CRUD, validation, locking edge cases
- `pytest --cov-report=html` for coverage report

## Deployment

### Docker
- `Dockerfile`: Multi-stage Python app
- `docker-compose.yml`: App + Postgres stack

Example `docker-compose up` spins up:
- botfarm-app:8000
- postgres:5432 (with botfarm DB)

### Kubernetes/Minikube (Bonus)
- Probes: `/health` (liveness/readiness/startup)
- Deploy with `kubectl apply -f k8s/`

### Health Checks
```
GET /health → {"status": "healthy"}
```

## Migrations (Alembic)

```bash
alembic revision --autogenerate -m "Add users table"
alembic upgrade head
```

Update `alembic.ini` `sqlalchemy.url` for prod.

## Coverage & Quality
- PEP8 compliant (black/isort pre-commit recommended)
- Type hints everywhere
- Docstrings on all functions
- >75% branch coverage

## Troubleshooting
- **Connection errors**: Check `DATABASE_URL`, Postgres running
- **Lock issues**: Locks are atomic; use `release_lock` after tests
- **Tests fail**: Ensure `aiosqlite` installed

## Additional (Implemented Bonus)
- ✅ Async (asyncio/asyncpg)
- ✅ Alembic migrations
- ✅ Probes (`/health`)

Questions? Check `/docs` or open an issue.
