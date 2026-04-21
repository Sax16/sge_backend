from collections.abc import Sequence

from sqlalchemy.orm import Session

from app.models.charge_discount import ChargeDiscount
from app.schemas.charge_discount import ChargeDiscountCreate, ChargeDiscountUpdate


def create_charge_discount(db: Session, charge_discount_in: ChargeDiscountCreate) -> ChargeDiscount:
    charge_discount = ChargeDiscount(**charge_discount_in.model_dump())
    db.add(charge_discount)
    db.commit()
    db.refresh(charge_discount)
    return charge_discount


def get_charge_discount(db: Session, charge_discount_id: int | str) -> ChargeDiscount | None:
    return db.query(ChargeDiscount).filter(ChargeDiscount.id == charge_discount_id).first()


def get_charge_discounts(db: Session, skip: int = 0, limit: int = 100) -> Sequence[ChargeDiscount]:
    return db.query(ChargeDiscount).order_by(ChargeDiscount.id).offset(skip).limit(limit).all()


def update_charge_discount(
    db: Session, charge_discount: ChargeDiscount, charge_discount_in: ChargeDiscountUpdate
) -> ChargeDiscount:
    data = charge_discount_in.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(charge_discount, key, value)
    db.add(charge_discount)
    db.commit()
    db.refresh(charge_discount)
    return charge_discount


def delete_charge_discount(db: Session, charge_discount: ChargeDiscount) -> None:
    db.delete(charge_discount)
    db.commit()
