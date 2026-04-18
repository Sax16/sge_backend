"""
Shared fixtures and factory helpers for API v1 endpoint tests.

Following SRP, each factory creates exactly ONE entity and can be
customised via keyword arguments so tests remain declarative.
"""
from datetime import date, datetime, timezone
from decimal import Decimal

import pytest
from sqlalchemy.orm import Session

from app.core.enums import (
    EmployeePosition,
    ExpenseType,
    Gender,
    UserRole,
)
from app.core.security import get_password_hash
from app.models.employee import Employee
from app.models.expense import Expense
from app.models.user import User


# ---------------------------------------------------------------------------
# Factory helpers
# ---------------------------------------------------------------------------

class EmployeeFactory:
    """Creates Employee ORM instances in the database."""

    _counter = 0

    @classmethod
    def create(
        cls,
        db: Session,
        *,
        first_name: str = "Juan",
        last_name: str = "Pérez",
        dni: str | None = None,
        gender: Gender = Gender.MASCULINO,
        birth_date: date | None = None,
        phone_number: str = "999888777",
        email: str | None = None,
        is_active: bool = True,
        position: EmployeePosition = EmployeePosition.DOCENTE,
    ) -> Employee:
        cls._counter += 1
        employee = Employee(
            first_name=first_name,
            last_name=last_name,
            dni=dni or f"1000000{cls._counter:02d}",
            gender=gender,
            birth_date=birth_date,
            phone_number=phone_number,
            email=email,
            is_active=is_active,
            position=position,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        db.add(employee)
        db.commit()
        db.refresh(employee)
        return employee


class UserFactory:
    """Creates User ORM instances in the database."""

    _counter = 0

    @classmethod
    def create(
        cls,
        db: Session,
        *,
        username: str | None = None,
        password: str = "TestPass123",
        role: UserRole = UserRole.ADMIN,
        is_active: bool = True,
        employee: Employee | None = None,
    ) -> User:
        cls._counter += 1
        if employee is None:
            employee = EmployeeFactory.create(db)
        user = User(
            username=username or f"testuser_{cls._counter}",
            password=get_password_hash(password),
            role=role,
            is_active=is_active,
            employee_id=employee.id,
            created_at=datetime.now(timezone.utc),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user


class ExpenseFactory:
    """Creates Expense ORM instances in the database."""

    _counter = 0

    @classmethod
    def create(
        cls,
        db: Session,
        *,
        name: str = "Material de oficina",
        amount: Decimal = Decimal("150.50"),
        expense_date: date | None = None,
        expense_type: ExpenseType = ExpenseType.ADMINISTRATIVO,
        details: str | None = None,
        user: User | None = None,
    ) -> Expense:
        cls._counter += 1
        if user is None:
            user = UserFactory.create(db)
        expense = Expense(
            name=name,
            amount=amount,
            date=expense_date or date.today(),
            expense_type=expense_type,
            details=details,
            user_id=user.id,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        db.add(expense)
        db.commit()
        db.refresh(expense)
        return expense


# ---------------------------------------------------------------------------
# Reset factory counters between tests to avoid DNI collisions
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def _reset_factory_counters():
    EmployeeFactory._counter = 0
    UserFactory._counter = 0
    ExpenseFactory._counter = 0
    yield
