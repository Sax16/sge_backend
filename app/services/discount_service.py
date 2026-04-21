from collections.abc import Sequence
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.models.discount import Discount
from app.schemas.discount import DiscountCreate, DiscountUpdate
from app.crud import discount_crud


def get_discount(db: Session, discount_id: int | str) -> Discount | None:
    return discount_crud.get_discount(db, discount_id)


def get_discounts(db: Session, skip: int = 0, limit: int = 100) -> Sequence[Discount]:
    return discount_crud.get_discounts(db, skip=skip, limit=limit)


def create_discount(db: Session, discount: DiscountCreate) -> Discount:
    return discount_crud.create_discount(db, discount)


def update_discount(db: Session, discount: Discount, discount_in: DiscountUpdate) -> Discount:
    return discount_crud.update_discount(db, discount, discount_in)


def delete_discount(db: Session, discount: Discount) -> None:
    discount_crud.delete_discount(db, discount)
