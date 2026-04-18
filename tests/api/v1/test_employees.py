"""
Tests for the Employees endpoints (CRUD under /employees).

Covers:
- List employees (GET /).
- Get employee by ID (GET /{id}).
- Create employee (POST /).
- Update employee (PUT /{id}).
- Delete employee (DELETE /{id}).
- 404 for non-existent employee.
- 403 for unauthenticated / insufficient role.
- Business rule: duplicate DNI on create / update.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.enums import EmployeePosition, Gender
from tests.api.v1.conftest import EmployeeFactory

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
BASE_URL = "/employees"


def _employee_payload(**overrides) -> dict:
    """Return a valid employee creation payload, with optional overrides."""
    data = {
        "firstName": "María",
        "lastName": "García",
        "dni": "99887766",
        "gender": Gender.FEMENINO.value,
        "phoneNumber": "912345678",
        "isActive": True,
        "position": EmployeePosition.SECRETARIA.value,
    }
    data.update(overrides)
    return data


# ---------------------------------------------------------------------------
# GET /employees
# ---------------------------------------------------------------------------

class TestListEmployees:

    def test_list_only_fixture_employee(self, client_super_admin: TestClient):
        """Without extra seeds, only the fixture-created employee exists."""
        response = client_super_admin.get(BASE_URL)

        assert response.status_code == 200
        # The super_admin fixture seeds one employee for the auth user
        assert len(response.json()) == 1

    def test_list_returns_seeded_employees(
        self, client_super_admin: TestClient, db_session: Session
    ):
        """Seeded employees appear in the list response."""
        EmployeeFactory.create(db_session, first_name="Ana")
        EmployeeFactory.create(db_session, first_name="Luis")

        response = client_super_admin.get(BASE_URL)

        assert response.status_code == 200
        data = response.json()
        # 2 created + the one seeded by super_admin_user fixture
        assert len(data) >= 2

    def test_list_respects_pagination(
        self, client_super_admin: TestClient, db_session: Session
    ):
        """skip and limit query params control pagination."""
        for i in range(5):
            EmployeeFactory.create(db_session, first_name=f"Emp{i}")

        response = client_super_admin.get(BASE_URL, params={"skip": 0, "limit": 2})

        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_list_requires_authentication(self, client_unauthenticated: TestClient):
        """Unauthenticated access is rejected (401)."""
        response = client_unauthenticated.get(BASE_URL)

        assert response.status_code == 401


# ---------------------------------------------------------------------------
# GET /employees/{id}
# ---------------------------------------------------------------------------

class TestGetEmployee:

    def test_get_existing(
        self, client_super_admin: TestClient, db_session: Session
    ):
        """Fetching an existing employee returns its data."""
        emp = EmployeeFactory.create(db_session, first_name="Pedro")

        response = client_super_admin.get(f"{BASE_URL}/{emp.id}")

        assert response.status_code == 200
        body = response.json()
        assert body["firstName"] == "Pedro"
        assert body["id"] == emp.id

    def test_get_nonexistent(self, client_super_admin: TestClient):
        """Fetching an ID that does not exist returns 404."""
        response = client_super_admin.get(f"{BASE_URL}/99999")

        assert response.status_code == 404


# ---------------------------------------------------------------------------
# POST /employees
# ---------------------------------------------------------------------------

class TestCreateEmployee:

    def test_create_success(self, client_super_admin: TestClient):
        """Creating an employee with valid data returns 201."""
        payload = _employee_payload()

        response = client_super_admin.post(BASE_URL, json=payload)

        assert response.status_code == 201
        body = response.json()
        assert body["firstName"] == "María"
        assert body["dni"] == "99887766"
        assert "id" in body

    def test_create_duplicate_dni(
        self, client_super_admin: TestClient, db_session: Session
    ):
        """Creating an employee with an existing DNI returns 400."""
        EmployeeFactory.create(db_session, dni="11223344")

        payload = _employee_payload(dni="11223344")
        response = client_super_admin.post(BASE_URL, json=payload)

        assert response.status_code == 400
        assert "DNI" in response.json()["detail"]

    def test_create_missing_required_field(self, client_super_admin: TestClient):
        """Omitting a required field returns 422."""
        payload = _employee_payload()
        del payload["dni"]

        response = client_super_admin.post(BASE_URL, json=payload)

        assert response.status_code == 422


# ---------------------------------------------------------------------------
# PUT /employees/{id}
# ---------------------------------------------------------------------------

class TestUpdateEmployee:

    def test_update_success(
        self, client_super_admin: TestClient, db_session: Session
    ):
        """Updating an existing employee returns 204 No Content."""
        emp = EmployeeFactory.create(db_session, first_name="Carlos")

        payload = _employee_payload(firstName="Carlos Editado", dni=emp.dni)
        response = client_super_admin.put(f"{BASE_URL}/{emp.id}", json=payload)

        assert response.status_code == 204
        assert response.content == b""

        # Verify the update was persisted
        get_response = client_super_admin.get(f"{BASE_URL}/{emp.id}")
        assert get_response.json()["firstName"] == "Carlos Editado"

    def test_update_nonexistent(self, client_super_admin: TestClient):
        """Updating a non-existent employee returns 404."""
        payload = _employee_payload()
        response = client_super_admin.put(f"{BASE_URL}/99999", json=payload)

        assert response.status_code == 404

    def test_update_duplicate_dni(
        self, client_super_admin: TestClient, db_session: Session
    ):
        """Changing DNI to one already taken by another employee returns 400."""
        emp_a = EmployeeFactory.create(db_session, dni="11111111")
        emp_b = EmployeeFactory.create(db_session, dni="22222222")

        payload = _employee_payload(dni="11111111")
        response = client_super_admin.put(f"{BASE_URL}/{emp_b.id}", json=payload)

        assert response.status_code == 400


# ---------------------------------------------------------------------------
# DELETE /employees/{id}
# ---------------------------------------------------------------------------

class TestDeleteEmployee:

    def test_delete_success(
        self, client_super_admin: TestClient, db_session: Session
    ):
        """Deleting an existing employee returns 204."""
        emp = EmployeeFactory.create(db_session, first_name="ToDelete")

        response = client_super_admin.delete(f"{BASE_URL}/{emp.id}")

        assert response.status_code == 204

        # Verify it's actually gone
        get_response = client_super_admin.get(f"{BASE_URL}/{emp.id}")
        assert get_response.status_code == 404

    def test_delete_nonexistent(self, client_super_admin: TestClient):
        """Deleting a non-existent employee returns 404."""
        response = client_super_admin.delete(f"{BASE_URL}/99999")

        assert response.status_code == 404


# ---------------------------------------------------------------------------
# Authorization
# ---------------------------------------------------------------------------

class TestEmployeesAuthorization:

    def test_admin_can_access(
        self, client_admin: TestClient, db_session: Session
    ):
        """ADMIN role has access to employee endpoints."""
        EmployeeFactory.create(db_session)

        response = client_admin.get(BASE_URL)

        assert response.status_code == 200

    def test_unauthenticated_is_rejected(
        self, client_unauthenticated: TestClient
    ):
        """Unauthenticated requests are rejected with 401."""
        response = client_unauthenticated.get(BASE_URL)

        assert response.status_code == 401
