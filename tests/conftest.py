"""
Root-level test configuration and shared fixtures.

Uses an in-memory SQLite database so that tests are fast, isolated,
and never touch the real PostgreSQL database.  Authentication
dependencies are overridden to inject deterministic test users.

Design decisions:
    - ``StaticPool`` ensures a single shared connection for the in-memory
      SQLite database.  Without it, each ``Session()`` would open a new
      connection — and with ``sqlite://`` each new connection gets a
      *fresh, empty* database.
    - ``@compiles(SmallInteger, 'sqlite')`` renders ``SmallInteger`` as
      ``INTEGER`` in DDL so that SQLite autoincrement works.  SQLite only
      auto-increments columns whose *declared* type is exactly ``INTEGER``.
"""
from collections.abc import Generator
from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import SmallInteger, create_engine, event
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.enums import EmployeePosition, Gender, UserRole
from app.core.security import get_password_hash
from app.dependencies import get_current_user, get_db
from app.main import app
from app.models import Base
from app.models.employee import Employee
from app.models.user import User

# ---------------------------------------------------------------------------
# SQLite compatibility: SmallInteger → INTEGER
# ---------------------------------------------------------------------------
@compiles(SmallInteger, "sqlite")
def _compile_smallint_sqlite(type_, compiler, **kw):
    return "INTEGER"


# ---------------------------------------------------------------------------
# Database engine (in-memory SQLite with StaticPool)
# ---------------------------------------------------------------------------
SQLALCHEMY_TEST_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


@event.listens_for(engine, "connect")
def _set_sqlite_pragma(dbapi_connection, _connection_record):
    """Enable FK enforcement in SQLite (off by default)."""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def setup_database():
    """Create all tables before each test and drop them after."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    """Provide a transactional database session scoped to a single test."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


def _override_get_db():
    """Dependency override for ``get_db``."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


# -- Seed helpers -----------------------------------------------------------

def _create_employee(db: Session, *, dni: str = "12345678") -> Employee:
    """Insert a minimal employee and return it."""
    employee = Employee(
        first_name="Test",
        last_name="Employee",
        dni=dni,
        gender=Gender.MASCULINO,
        phone_number="999999999",
        is_active=True,
        position=EmployeePosition.DOCENTE,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


def _create_user(
    db: Session,
    *,
    username: str = "admin_test",
    password: str = "secret123",
    role: UserRole = UserRole.SUPER_ADMIN,
    employee: Employee | None = None,
) -> User:
    """Insert a user linked to an employee and return it."""
    if employee is None:
        employee = _create_employee(db)
    user = User(
        username=username,
        password=get_password_hash(password),
        is_active=True,
        role=role,
        employee_id=employee.id,
        created_at=datetime.now(timezone.utc),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# -- Client fixtures --------------------------------------------------------

@pytest.fixture()
def super_admin_user(db_session: Session) -> User:
    """Pre-seeded SUPER_ADMIN user available to tests that need one."""
    return _create_user(db_session, role=UserRole.SUPER_ADMIN)


@pytest.fixture()
def admin_user(db_session: Session) -> User:
    """Pre-seeded ADMIN user available to tests that need one."""
    emp = _create_employee(db_session, dni="87654321")
    return _create_user(
        db_session,
        username="admin_regular",
        role=UserRole.ADMIN,
        employee=emp,
    )


@pytest.fixture()
def client_unauthenticated() -> TestClient:
    """TestClient with NO authentication override (anonymous access)."""
    app.dependency_overrides[get_db] = _override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture()
def client_super_admin(super_admin_user: User) -> TestClient:
    """TestClient authenticated as SUPER_ADMIN."""
    app.dependency_overrides[get_db] = _override_get_db
    app.dependency_overrides[get_current_user] = lambda: super_admin_user
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture()
def client_admin(admin_user: User) -> TestClient:
    """TestClient authenticated as ADMIN."""
    app.dependency_overrides[get_db] = _override_get_db
    app.dependency_overrides[get_current_user] = lambda: admin_user
    yield TestClient(app)
    app.dependency_overrides.clear()
