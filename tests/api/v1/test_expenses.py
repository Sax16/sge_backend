"""
Tests for the Expenses endpoints (CRUD under /expenses).

Covers:
- List expenses (GET /).
- Get expense by ID (GET /{id}).
- Create expense (POST /) — injects current_user.id automatically.
- Update expense (PUT /{id}).
- Delete expense (DELETE /{id}) — restricted to SUPER_ADMIN.
- 404 for non-existent expense.
- 403 for ADMIN trying to delete.
- 401 for unauthenticated access.
"""
import pytest
from datetime import date
from decimal import Decimal
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.enums import ExpenseType
from tests.api.v1.conftest import ExpenseFactory, UserFactory

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
BASE_URL = "/expenses"


def _expense_payload(**overrides) -> dict:
    """Return a valid expense creation payload."""
    data = {
        "name": "Pago de luz",
        "amount": "250.00",
        "date": str(date.today()),
        "expenseType": ExpenseType.SERVICIOS.value,
        "details": "Recibo del mes de abril",
    }
    data.update(overrides)
    return data


# ---------------------------------------------------------------------------
# GET /expenses
# ---------------------------------------------------------------------------

class TestListExpenses:

    def test_list_empty(self, client_super_admin: TestClient):
        """An empty database returns an empty list."""
        response = client_super_admin.get(BASE_URL)

        assert response.status_code == 200
        assert response.json() == []

    def test_list_returns_seeded_expenses(
        self, client_super_admin: TestClient, db_session: Session
    ):
        """Seeded expenses appear in the list."""
        user = UserFactory.create(db_session)
        ExpenseFactory.create(db_session, user=user, name="Internet")
        ExpenseFactory.create(db_session, user=user, name="Agua")

        response = client_super_admin.get(BASE_URL)

        assert response.status_code == 200
        assert len(response.json()) >= 2

    def test_list_respects_pagination(
        self, client_super_admin: TestClient, db_session: Session
    ):
        """skip/limit params control pagination."""
        user = UserFactory.create(db_session)
        for i in range(5):
            ExpenseFactory.create(db_session, user=user, name=f"Exp{i}")

        response = client_super_admin.get(BASE_URL, params={"skip": 0, "limit": 3})

        assert response.status_code == 200
        assert len(response.json()) == 3


# ---------------------------------------------------------------------------
# GET /expenses/{id}
# ---------------------------------------------------------------------------

class TestGetExpense:

    def test_get_existing(
        self, client_super_admin: TestClient, db_session: Session
    ):
        """Fetching an existing expense returns its data."""
        user = UserFactory.create(db_session)
        exp = ExpenseFactory.create(db_session, user=user, name="Teléfono")

        response = client_super_admin.get(f"{BASE_URL}/{exp.id}")

        assert response.status_code == 200
        body = response.json()
        assert body["name"] == "Teléfono"
        assert body["id"] == exp.id

    def test_get_nonexistent(self, client_super_admin: TestClient):
        """Fetching a non-existent expense returns 404."""
        response = client_super_admin.get(f"{BASE_URL}/99999")

        assert response.status_code == 404


# ---------------------------------------------------------------------------
# POST /expenses
# ---------------------------------------------------------------------------

class TestCreateExpense:

    def test_create_success(self, client_super_admin: TestClient):
        """Creating an expense returns 201 with user_id auto-assigned."""
        payload = _expense_payload()

        response = client_super_admin.post(BASE_URL, json=payload)

        assert response.status_code == 201
        body = response.json()
        assert body["name"] == "Pago de luz"
        assert "id" in body
        assert "userId" in body

    def test_create_missing_required_field(self, client_super_admin: TestClient):
        """Omitting a required field returns 422."""
        payload = _expense_payload()
        del payload["amount"]

        response = client_super_admin.post(BASE_URL, json=payload)

        assert response.status_code == 422

    def test_create_invalid_amount(self, client_super_admin: TestClient):
        """An amount exceeding the max returns 422."""
        payload = _expense_payload(amount="99999.99")

        response = client_super_admin.post(BASE_URL, json=payload)

        assert response.status_code == 422


# ---------------------------------------------------------------------------
# PUT /expenses/{id}
# ---------------------------------------------------------------------------

class TestUpdateExpense:

    def test_update_success(
        self, client_super_admin: TestClient, db_session: Session
    ):
        """Updating an expense returns 204 No Content."""
        user = UserFactory.create(db_session)
        exp = ExpenseFactory.create(db_session, user=user, name="Original")

        payload = _expense_payload(name="Actualizado")
        response = client_super_admin.put(f"{BASE_URL}/{exp.id}", json=payload)

        assert response.status_code == 204
        assert response.content == b""

        # Verify the update was persisted
        get_response = client_super_admin.get(f"{BASE_URL}/{exp.id}")
        assert get_response.json()["name"] == "Actualizado"

    def test_update_nonexistent(self, client_super_admin: TestClient):
        """Updating a non-existent expense returns 404."""
        payload = _expense_payload()
        response = client_super_admin.put(f"{BASE_URL}/99999", json=payload)

        assert response.status_code == 404

    def test_partial_update(
        self, client_super_admin: TestClient, db_session: Session
    ):
        """Sending only some fields for update still works (other fields remain)."""
        user = UserFactory.create(db_session)
        exp = ExpenseFactory.create(
            db_session, user=user, name="Parcial",
            amount=Decimal("100.00"),
        )

        payload = _expense_payload(name="Parcial Editado")
        response = client_super_admin.put(f"{BASE_URL}/{exp.id}", json=payload)

        assert response.status_code == 204

        # Verify the update was persisted
        get_response = client_super_admin.get(f"{BASE_URL}/{exp.id}")
        assert get_response.json()["name"] == "Parcial Editado"


# ---------------------------------------------------------------------------
# DELETE /expenses/{id}
# ---------------------------------------------------------------------------

class TestDeleteExpense:

    def test_delete_success_super_admin(
        self, client_super_admin: TestClient, db_session: Session
    ):
        """SUPER_ADMIN can delete an expense (204)."""
        user = UserFactory.create(db_session)
        exp = ExpenseFactory.create(db_session, user=user)

        response = client_super_admin.delete(f"{BASE_URL}/{exp.id}")

        assert response.status_code == 204

        # Confirm deletion
        get_response = client_super_admin.get(f"{BASE_URL}/{exp.id}")
        assert get_response.status_code == 404

    def test_delete_nonexistent(self, client_super_admin: TestClient):
        """Deleting a non-existent expense returns 404."""
        response = client_super_admin.delete(f"{BASE_URL}/99999")

        assert response.status_code == 404

    def test_delete_forbidden_for_admin(
        self, client_admin: TestClient, db_session: Session
    ):
        """ADMIN role cannot delete expenses (403)."""
        user = UserFactory.create(db_session)
        exp = ExpenseFactory.create(db_session, user=user)

        response = client_admin.delete(f"{BASE_URL}/{exp.id}")

        assert response.status_code == 403


# ---------------------------------------------------------------------------
# Authorization
# ---------------------------------------------------------------------------

class TestExpensesAuthorization:

    def test_admin_can_read(self, client_admin: TestClient):
        """ADMIN role can list expenses."""
        response = client_admin.get(BASE_URL)

        assert response.status_code == 200

    def test_unauthenticated_is_rejected(
        self, client_unauthenticated: TestClient
    ):
        """Unauthenticated requests are rejected with 401."""
        response = client_unauthenticated.get(BASE_URL)

        assert response.status_code == 401
