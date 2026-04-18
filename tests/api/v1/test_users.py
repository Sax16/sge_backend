"""
Tests for the Users endpoints (CRUD under /users).

Covers:
- List users (GET /).
- Get user by ID (GET /{id}).
- Create user (POST /).
- Update user (PUT /{id}).
- Delete user (DELETE /{id}).
- 404 for non-existent user.
- 403 for non-SUPER_ADMIN.
- Business rules: duplicate username, non-existent employee, employee already assigned.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.enums import UserRole
from tests.api.v1.conftest import EmployeeFactory, UserFactory

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
BASE_URL = "/users"


def _user_payload(employee_id: int, **overrides) -> dict:
    """Return a valid user creation payload."""
    data = {
        "username": "new_user",
        "password": "SecureP@ss1",
        "isActive": True,
        "role": UserRole.ADMIN.value,
        "employeeId": employee_id,
    }
    data.update(overrides)
    return data


# ---------------------------------------------------------------------------
# GET /users
# ---------------------------------------------------------------------------

class TestListUsers:

    def test_list_returns_users(
        self, client_super_admin: TestClient, db_session: Session
    ):
        """The list endpoint returns existing users."""
        UserFactory.create(db_session, username="extra_user")

        response = client_super_admin.get(BASE_URL)

        assert response.status_code == 200
        data = response.json()
        # At minimum: super_admin from fixture + extra_user
        assert len(data) >= 2

    def test_list_respects_pagination(
        self, client_super_admin: TestClient, db_session: Session
    ):
        """skip and limit query params limit the result set."""
        for i in range(5):
            UserFactory.create(db_session)

        response = client_super_admin.get(BASE_URL, params={"skip": 0, "limit": 2})

        assert response.status_code == 200
        assert len(response.json()) == 2


# ---------------------------------------------------------------------------
# GET /users/{id}
# ---------------------------------------------------------------------------

class TestGetUser:

    def test_get_existing_user(
        self, client_super_admin: TestClient, super_admin_user
    ):
        """Fetching an existing user returns 200 with correct data."""
        response = client_super_admin.get(f"{BASE_URL}/{super_admin_user.id}")

        assert response.status_code == 200
        body = response.json()
        assert body["username"] == super_admin_user.username

    def test_get_nonexistent_user(self, client_super_admin: TestClient):
        """Fetching a non-existent user returns 404."""
        response = client_super_admin.get(f"{BASE_URL}/99999")

        assert response.status_code == 404


# ---------------------------------------------------------------------------
# POST /users
# ---------------------------------------------------------------------------

class TestCreateUser:

    def test_create_success(
        self, client_super_admin: TestClient, db_session: Session
    ):
        """Creating a user with valid data returns 201."""
        emp = EmployeeFactory.create(db_session)
        payload = _user_payload(emp.id)

        response = client_super_admin.post(BASE_URL, json=payload)

        assert response.status_code == 201
        body = response.json()
        assert body["username"] == "new_user"
        assert "id" in body

    def test_create_duplicate_username(
        self, client_super_admin: TestClient, db_session: Session
    ):
        """Creating a user with an existing username returns 400."""
        emp1 = EmployeeFactory.create(db_session)
        emp2 = EmployeeFactory.create(db_session)
        UserFactory.create(db_session, username="duplicate_name", employee=emp1)

        payload = _user_payload(emp2.id, username="duplicate_name")
        response = client_super_admin.post(BASE_URL, json=payload)

        assert response.status_code == 400
        assert "already exists" in response.json()["detail"]

    def test_create_nonexistent_employee(
        self, client_super_admin: TestClient
    ):
        """Creating a user linked to a non-existent employee returns 404."""
        payload = _user_payload(employee_id=99999)

        response = client_super_admin.post(BASE_URL, json=payload)

        assert response.status_code == 404

    def test_create_employee_already_assigned(
        self, client_super_admin: TestClient, db_session: Session
    ):
        """Creating a user for an employee that already has a user returns 400."""
        emp = EmployeeFactory.create(db_session)
        UserFactory.create(db_session, employee=emp)

        payload = _user_payload(emp.id, username="another_user")
        response = client_super_admin.post(BASE_URL, json=payload)

        assert response.status_code == 400
        assert "already assigned" in response.json()["detail"]

    def test_create_missing_required_field(
        self, client_super_admin: TestClient, db_session: Session
    ):
        """Omitting required fields returns 422."""
        emp = EmployeeFactory.create(db_session)
        payload = _user_payload(emp.id)
        del payload["password"]

        response = client_super_admin.post(BASE_URL, json=payload)

        assert response.status_code == 422


# ---------------------------------------------------------------------------
# PUT /users/{id}
# ---------------------------------------------------------------------------

class TestUpdateUser:

    def test_update_success(
        self, client_super_admin: TestClient, db_session: Session
    ):
        """Updating a user returns 204 No Content."""
        user = UserFactory.create(db_session, username="to_update")

        payload = {
            "username": "updated_user",
            "isActive": True,
            "role": UserRole.ADMIN.value,
        }
        response = client_super_admin.put(f"{BASE_URL}/{user.id}", json=payload)

        assert response.status_code == 204
        assert response.content == b""

        # Verify the update was persisted
        get_response = client_super_admin.get(f"{BASE_URL}/{user.id}")
        assert get_response.json()["username"] == "updated_user"

    def test_update_nonexistent_user(self, client_super_admin: TestClient):
        """Updating a non-existent user returns 404."""
        payload = {
            "username": "ghost",
            "isActive": True,
            "role": UserRole.ADMIN.value,
        }
        response = client_super_admin.put(f"{BASE_URL}/99999", json=payload)

        assert response.status_code == 404

    def test_update_duplicate_username(
        self, client_super_admin: TestClient, db_session: Session
    ):
        """Changing username to one that already belongs to another user returns 400."""
        user_a = UserFactory.create(db_session, username="user_a")
        user_b = UserFactory.create(db_session, username="user_b")

        payload = {
            "username": "user_a",   # already taken
            "isActive": True,
            "role": UserRole.ADMIN.value,
        }
        response = client_super_admin.put(f"{BASE_URL}/{user_b.id}", json=payload)

        assert response.status_code == 400


# ---------------------------------------------------------------------------
# DELETE /users/{id}
# ---------------------------------------------------------------------------

class TestDeleteUser:

    def test_delete_success(
        self, client_super_admin: TestClient, db_session: Session
    ):
        """Deleting an existing user returns 204."""
        user = UserFactory.create(db_session, username="to_delete")

        response = client_super_admin.delete(f"{BASE_URL}/{user.id}")

        assert response.status_code == 204

        # Confirm deletion
        get_response = client_super_admin.get(f"{BASE_URL}/{user.id}")
        assert get_response.status_code == 404

    def test_delete_nonexistent_user(self, client_super_admin: TestClient):
        """Deleting a non-existent user returns 404."""
        response = client_super_admin.delete(f"{BASE_URL}/99999")

        assert response.status_code == 404


# ---------------------------------------------------------------------------
# Authorization — only SUPER_ADMIN allowed
# ---------------------------------------------------------------------------

class TestUsersAuthorization:

    def test_admin_cannot_access(self, client_admin: TestClient):
        """ADMIN role is forbidden (403) from user management."""
        response = client_admin.get(BASE_URL)

        assert response.status_code == 403

    def test_unauthenticated_is_rejected(
        self, client_unauthenticated: TestClient
    ):
        """Unauthenticated requests are rejected with 401."""
        response = client_unauthenticated.get(BASE_URL)

        assert response.status_code == 401
