"""
Tests for the Auth endpoints (POST /auth/login, GET /auth/login/me).

Covers:
- Successful login with valid credentials.
- Login failure with wrong password.
- Login failure with non-existent username.
- Login failure for inactive user.
- GET /me returns the authenticated user's data.
- GET /me rejects unauthenticated requests.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.enums import UserRole
from app.core.security import get_password_hash
from app.models.user import User
from tests.api.v1.conftest import EmployeeFactory, UserFactory

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
LOGIN_URL = "/auth/login"
ME_URL = "/auth/login/me"
VALID_PASSWORD = "SuperSecret123"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _seed_active_user(db: Session, *, role: UserRole = UserRole.SUPER_ADMIN) -> User:
    """Create an active user with a known plain-text password."""
    emp = EmployeeFactory.create(db)
    return UserFactory.create(
        db,
        username="login_user",
        password=VALID_PASSWORD,
        role=role,
        employee=emp,
    )


def _seed_inactive_user(db: Session) -> User:
    """Create an inactive user."""
    emp = EmployeeFactory.create(db)
    return UserFactory.create(
        db,
        username="inactive_user",
        password=VALID_PASSWORD,
        is_active=False,
        employee=emp,
    )


# ---------------------------------------------------------------------------
# POST /auth/login
# ---------------------------------------------------------------------------

class TestLogin:
    """Unit tests for the login endpoint."""

    def test_login_success(
        self, client_unauthenticated: TestClient, db_session: Session
    ):
        """A valid username + password returns an access token."""
        _seed_active_user(db_session)

        response = client_unauthenticated.post(
            LOGIN_URL,
            data={"username": "login_user", "password": VALID_PASSWORD},
        )

        assert response.status_code == 200
        body = response.json()
        assert "access_token" in body
        assert body["token_type"] == "Bearer"

    def test_login_wrong_password(
        self, client_unauthenticated: TestClient, db_session: Session
    ):
        """Wrong password returns 401."""
        _seed_active_user(db_session)

        response = client_unauthenticated.post(
            LOGIN_URL,
            data={"username": "login_user", "password": "WRONG_PASSWORD"},
        )

        assert response.status_code == 401

    def test_login_nonexistent_user(
        self, client_unauthenticated: TestClient
    ):
        """Non-existent username returns 401."""
        response = client_unauthenticated.post(
            LOGIN_URL,
            data={"username": "ghost", "password": "whatever"},
        )

        assert response.status_code == 401

    def test_login_inactive_user(
        self, client_unauthenticated: TestClient, db_session: Session
    ):
        """An inactive user cannot log in (401)."""
        _seed_inactive_user(db_session)

        response = client_unauthenticated.post(
            LOGIN_URL,
            data={"username": "inactive_user", "password": VALID_PASSWORD},
        )

        assert response.status_code == 401
        assert "deshabilitado" in response.json()["detail"]


# ---------------------------------------------------------------------------
# GET /auth/login/me
# ---------------------------------------------------------------------------

class TestMe:
    """Unit tests for the /me endpoint."""

    def test_me_authenticated(
        self, client_super_admin: TestClient, super_admin_user: User
    ):
        """An authenticated user can retrieve their own profile."""
        response = client_super_admin.get(ME_URL)

        assert response.status_code == 200
        body = response.json()
        assert body["username"] == super_admin_user.username
        assert body["id"] == super_admin_user.id

    def test_me_unauthenticated(self, client_unauthenticated: TestClient):
        """Unauthenticated requests to /me return 401."""
        response = client_unauthenticated.get(ME_URL)

        assert response.status_code == 401
