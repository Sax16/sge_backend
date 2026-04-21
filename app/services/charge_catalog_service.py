from collections.abc import Sequence
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.models.charge_catalog import ChargeCatalog
from app.schemas.charge_catalog import ChargeCatalogCreate, ChargeCatalogUpdate
from app.crud import charge_catalog_crud


def get_charge_catalog(db: Session, charge_catalog_id: int | str) -> ChargeCatalog | None:
    return charge_catalog_crud.get_charge_catalog(db, charge_catalog_id)


def get_charge_catalogs(db: Session, skip: int = 0, limit: int = 100) -> Sequence[ChargeCatalog]:
    return charge_catalog_crud.get_charge_catalogs(db, skip=skip, limit=limit)


def create_charge_catalog(db: Session, charge_catalog: ChargeCatalogCreate) -> ChargeCatalog:
    return charge_catalog_crud.create_charge_catalog(db, charge_catalog)


def update_charge_catalog(db: Session, charge_catalog: ChargeCatalog, charge_catalog_in: ChargeCatalogUpdate) -> ChargeCatalog:
    return charge_catalog_crud.update_charge_catalog(db, charge_catalog, charge_catalog_in)


def delete_charge_catalog(db: Session, charge_catalog: ChargeCatalog) -> None:
    charge_catalog_crud.delete_charge_catalog(db, charge_catalog)
