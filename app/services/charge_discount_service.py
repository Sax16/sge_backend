from collections.abc import Sequence
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.models.charge_discount import ChargeDiscount
from app.schemas.charge_discount import ChargeDiscountCreate, ChargeDiscountUpdate
from app.crud import charge_discount_crud


def get_charge_discount(db: Session, charge_discount_id: int | str) -> ChargeDiscount | None:
    return charge_discount_crud.get_charge_discount(db, charge_discount_id)


def get_charge_discounts(db: Session, skip: int = 0, limit: int = 100) -> Sequence[ChargeDiscount]:
    return charge_discount_crud.get_charge_discounts(db, skip=skip, limit=limit)


def create_charge_discount(db: Session, charge_discount: ChargeDiscountCreate) -> ChargeDiscount:
    return charge_discount_crud.create_charge_discount(db, charge_discount)


def update_charge_discount(db: Session, charge_discount: ChargeDiscount, charge_discount_in: ChargeDiscountUpdate) -> ChargeDiscount:
    return charge_discount_crud.update_charge_discount(db, charge_discount, charge_discount_in)


def delete_charge_discount(db: Session, charge_discount: ChargeDiscount) -> None:
    charge_discount_crud.delete_charge_discount(db, charge_discount)
