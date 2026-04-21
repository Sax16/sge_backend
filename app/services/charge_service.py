from collections.abc import Sequence
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.models.charge import Charge
from app.schemas.charge import ChargeCreate, ChargeUpdate
from app.crud import charge_crud


def get_charge(db: Session, charge_id: int | str) -> Charge | None:
    return charge_crud.get_charge(db, charge_id)


def get_charges(db: Session, skip: int = 0, limit: int = 100) -> Sequence[Charge]:
    return charge_crud.get_charges(db, skip=skip, limit=limit)


def create_charge(db: Session, charge: ChargeCreate) -> Charge:
    return charge_crud.create_charge(db, charge)


def update_charge(db: Session, charge: Charge, charge_in: ChargeUpdate) -> Charge:
    return charge_crud.update_charge(db, charge, charge_in)


def delete_charge(db: Session, charge: Charge) -> None:
    charge_crud.delete_charge(db, charge)
