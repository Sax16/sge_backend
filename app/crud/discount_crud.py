from collections.abc import Sequence

from sqlalchemy.orm import Session

from app.models.discount import Discount
from app.schemas.discount import DiscountCreate, DiscountUpdate


def create_discount(db: Session, discount_in: DiscountCreate) -> Discount:
    discount = Discount(**discount_in.model_dump())
    db.add(discount)
    db.commit()
    db.refresh(discount)
    return discount


def get_discount(db: Session, discount_id: int | str) -> Discount | None:
    return db.query(Discount).filter(Discount.id == discount_id).first()


def get_discounts(db: Session, skip: int = 0, limit: int = 100) -> Sequence[Discount]:
    return db.query(Discount).order_by(Discount.id).offset(skip).limit(limit).all()


def update_discount(
    db: Session, discount: Discount, discount_in: DiscountUpdate
) -> Discount:
    data = discount_in.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(discount, key, value)
    db.add(discount)
    db.commit()
    db.refresh(discount)
    return discount


def delete_discount(db: Session, discount: Discount) -> None:
    db.delete(discount)
    db.commit()
