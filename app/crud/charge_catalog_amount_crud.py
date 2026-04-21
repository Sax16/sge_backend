from collections.abc import Sequence

from sqlalchemy.orm import Session

from app.models.charge_catalog_amount import ChargeCatalogAmount
from app.schemas.charge_catalog_amount import ChargeCatalogAmountCreate, ChargeCatalogAmountUpdate


def create_charge_catalog_amount(db: Session, charge_catalog_amount_in: ChargeCatalogAmountCreate) -> ChargeCatalogAmount:
    charge_catalog_amount = ChargeCatalogAmount(**charge_catalog_amount_in.model_dump())
    db.add(charge_catalog_amount)
    db.commit()
    db.refresh(charge_catalog_amount)
    return charge_catalog_amount


def get_charge_catalog_amount(db: Session, charge_catalog_amount_id: int | str) -> ChargeCatalogAmount | None:
    return db.query(ChargeCatalogAmount).filter(ChargeCatalogAmount.id == charge_catalog_amount_id).first()


def get_charge_catalog_amounts(db: Session, skip: int = 0, limit: int = 100) -> Sequence[ChargeCatalogAmount]:
    return db.query(ChargeCatalogAmount).order_by(ChargeCatalogAmount.id).offset(skip).limit(limit).all()


def update_charge_catalog_amount(
    db: Session, charge_catalog_amount: ChargeCatalogAmount, charge_catalog_amount_in: ChargeCatalogAmountUpdate
) -> ChargeCatalogAmount:
    data = charge_catalog_amount_in.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(charge_catalog_amount, key, value)
    db.add(charge_catalog_amount)
    db.commit()
    db.refresh(charge_catalog_amount)
    return charge_catalog_amount


def delete_charge_catalog_amount(db: Session, charge_catalog_amount: ChargeCatalogAmount) -> None:
    db.delete(charge_catalog_amount)
    db.commit()
