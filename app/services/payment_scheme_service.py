from collections.abc import Sequence
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.models.payment_scheme import PaymentScheme
from app.schemas.payment_scheme import PaymentSchemeCreate, PaymentSchemeUpdate
from app.crud import payment_scheme_crud


def get_payment_scheme(db: Session, payment_scheme_id: int | str) -> PaymentScheme | None:
    return payment_scheme_crud.get_payment_scheme(db, payment_scheme_id)


def get_payment_schemes(db: Session, skip: int = 0, limit: int = 100) -> Sequence[PaymentScheme]:
    return payment_scheme_crud.get_payment_schemes(db, skip=skip, limit=limit)


def create_payment_scheme(db: Session, payment_scheme: PaymentSchemeCreate) -> PaymentScheme:
    return payment_scheme_crud.create_payment_scheme(db, payment_scheme)


def update_payment_scheme(db: Session, payment_scheme: PaymentScheme, payment_scheme_in: PaymentSchemeUpdate) -> PaymentScheme:
    return payment_scheme_crud.update_payment_scheme(db, payment_scheme, payment_scheme_in)


def delete_payment_scheme(db: Session, payment_scheme: PaymentScheme) -> None:
    payment_scheme_crud.delete_payment_scheme(db, payment_scheme)
