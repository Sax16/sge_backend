from collections.abc import Sequence

from sqlalchemy.orm import Session

from app.models.charge_catalog import ChargeCatalog
from app.schemas.charge_catalog import ChargeCatalogCreate, ChargeCatalogUpdate


def create_charge_catalog(db: Session, charge_catalog_in: ChargeCatalogCreate) -> ChargeCatalog:
    charge_catalog = ChargeCatalog(**charge_catalog_in.model_dump())
    db.add(charge_catalog)
    db.commit()
    db.refresh(charge_catalog)
    return charge_catalog


def get_charge_catalog(db: Session, charge_catalog_id: int | str) -> ChargeCatalog | None:
    return db.query(ChargeCatalog).filter(ChargeCatalog.id == charge_catalog_id).first()


def get_charge_catalogs(db: Session, skip: int = 0, limit: int = 100) -> Sequence[ChargeCatalog]:
    return db.query(ChargeCatalog).order_by(ChargeCatalog.id).offset(skip).limit(limit).all()


def update_charge_catalog(
    db: Session, charge_catalog: ChargeCatalog, charge_catalog_in: ChargeCatalogUpdate
) -> ChargeCatalog:
    data = charge_catalog_in.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(charge_catalog, key, value)
    db.add(charge_catalog)
    db.commit()
    db.refresh(charge_catalog)
    return charge_catalog


def delete_charge_catalog(db: Session, charge_catalog: ChargeCatalog) -> None:
    db.delete(charge_catalog)
    db.commit()
