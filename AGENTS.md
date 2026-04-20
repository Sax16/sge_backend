# AGENTS.md - Elohim SGE Backend

## Project Overview
FastAPI + SQLAlchemy + PostgreSQL school management system with Alembic migrations.

## Run Commands
- **Dev server**: `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
- **Tests**: `pytest` (uses in-memory SQLite - no external DB required)
- **Single test file**: `pytest tests/api/test_employees.py`
- **Migrations**: `alembic upgrade head` / `alembic revision --autogenerate -m "message"`

## Architecture
- **Entry**: `app/main.py` - FastAPI app with lifespan, CORS, and v1 router
- **API v1**: `app/api/v1/` - endpoints, router at `app/api/v1/router.py`
- **Models**: `app/models/` - SQLAlchemy (Base in `app/models/__init__.py`)
- **Schemas**: `app/schemas/` - Pydantic request/response models
- **CRUD**: `app/crud/` - database operations
- **Services**: `app/services/` - business logic
- **Core**: `app/core/config.py` (settings), `app/core/database.py`, `app/core/security.py`

## Testing Fixtures (tests/conftest.py)
- `client_unauthenticated` - TestClient without auth
- `client_super_admin` - authenticated as SUPER_ADMIN
- `client_admin` - authenticated as ADMIN
- `super_admin_user`, `admin_user` - user fixtures
- `db_session` - transactional DB session
- Tests use SQLite with StaticPool and FK enforcement enabled

## Key Dependencies
- `fastapi`, `sqlalchemy`, `alembic`, `psycopg2-binary`, `pydantic`, `pytest`, `pytest-asyncio`

## DB Config
- PostgreSQL: set in `.env` (POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, POSTGRES_HOST, POSTGRES_PORT)
- SECRET_KEY required in `.env`

## Enums
`app/core/enums.py` - UserRole, Gender, EmployeePosition