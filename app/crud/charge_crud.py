from collections.abc import Sequence

from sqlalchemy.orm import Session

from app.models.charge import Charge
from app.schemas.charge import ChargeCreate, ChargeUpdate


def create_charge(db: Session, charge_in: ChargeCreate) -> Charge:
    charge = Charge(**charge_in.model_dump())
    db.add(charge)
    db.commit()
    db.refresh(charge)
    return charge


def get_charge(db: Session, charge_id: int | str) -> Charge | None:
    return db.query(Charge).filter(Charge.id == charge_id).first()


def get_charges(db: Session, skip: int = 0, limit: int = 100) -> Sequence[Charge]:
    return db.query(Charge).order_by(Charge.id).offset(skip).limit(limit).all()


def update_charge(
    db: Session, charge: Charge, charge_in: ChargeUpdate
) -> Charge:
    data = charge_in.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(charge, key, value)
    db.add(charge)
    db.commit()
    db.refresh(charge)
    return charge


def delete_charge(db: Session, charge: Charge) -> None:
    db.delete(charge)
    db.commit()
