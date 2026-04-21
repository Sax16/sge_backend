from collections.abc import Sequence

from sqlalchemy.orm import Session

from app.models.payment_scheme import PaymentScheme
from app.schemas.payment_scheme import PaymentSchemeCreate, PaymentSchemeUpdate


def create_payment_scheme(db: Session, payment_scheme_in: PaymentSchemeCreate) -> PaymentScheme:
    payment_scheme = PaymentScheme(**payment_scheme_in.model_dump())
    db.add(payment_scheme)
    db.commit()
    db.refresh(payment_scheme)
    return payment_scheme


def get_payment_scheme(db: Session, payment_scheme_id: int | str) -> PaymentScheme | None:
    return db.query(PaymentScheme).filter(PaymentScheme.id == payment_scheme_id).first()


def get_payment_schemes(db: Session, skip: int = 0, limit: int = 100) -> Sequence[PaymentScheme]:
    return db.query(PaymentScheme).order_by(PaymentScheme.id).offset(skip).limit(limit).all()


def update_payment_scheme(
    db: Session, payment_scheme: PaymentScheme, payment_scheme_in: PaymentSchemeUpdate
) -> PaymentScheme:
    data = payment_scheme_in.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(payment_scheme, key, value)
    db.add(payment_scheme)
    db.commit()
    db.refresh(payment_scheme)
    return payment_scheme


def delete_payment_scheme(db: Session, payment_scheme: PaymentScheme) -> None:
    db.delete(payment_scheme)
    db.commit()
