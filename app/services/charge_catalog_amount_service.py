from collections.abc import Sequence
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.models.charge_catalog_amount import ChargeCatalogAmount
from app.schemas.charge_catalog_amount import ChargeCatalogAmountCreate, ChargeCatalogAmountUpdate
from app.crud import charge_catalog_amount_crud


def get_charge_catalog_amount(db: Session, charge_catalog_amount_id: int | str) -> ChargeCatalogAmount | None:
    return charge_catalog_amount_crud.get_charge_catalog_amount(db, charge_catalog_amount_id)


def get_charge_catalog_amounts(db: Session, skip: int = 0, limit: int = 100) -> Sequence[ChargeCatalogAmount]:
    return charge_catalog_amount_crud.get_charge_catalog_amounts(db, skip=skip, limit=limit)


def create_charge_catalog_amount(db: Session, charge_catalog_amount: ChargeCatalogAmountCreate) -> ChargeCatalogAmount:
    return charge_catalog_amount_crud.create_charge_catalog_amount(db, charge_catalog_amount)


def update_charge_catalog_amount(db: Session, charge_catalog_amount: ChargeCatalogAmount, charge_catalog_amount_in: ChargeCatalogAmountUpdate) -> ChargeCatalogAmount:
    return charge_catalog_amount_crud.update_charge_catalog_amount(db, charge_catalog_amount, charge_catalog_amount_in)


def delete_charge_catalog_amount(db: Session, charge_catalog_amount: ChargeCatalogAmount) -> None:
    charge_catalog_amount_crud.delete_charge_catalog_amount(db, charge_catalog_amount)
