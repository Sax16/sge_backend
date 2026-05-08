from collections.abc import Sequence
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.models.economic_level import EconomicLevel
from app.schemas.economic_level import EconomicLevelCreate, EconomicLevelUpdate
from app.crud import economic_level_crud


def get_economic_level(db: Session, economic_level_id: int | str) -> EconomicLevel | None:
    return economic_level_crud.get_economic_level(db, economic_level_id)


def get_economic_levels(db: Session, skip: int = 0, limit: int = 100) -> Sequence[EconomicLevel]:
    return economic_level_crud.get_economic_levels(db, skip=skip, limit=limit)


def create_economic_level(db: Session, economic_level: EconomicLevelCreate) -> EconomicLevel:
    existing_economic_level = economic_level_crud.get_economic_level_by_name(db, economic_level.name)
    if existing_economic_level:
        raise HTTPException(status_code=400, detail="El nivel económico ya existe")
    return economic_level_crud.create_economic_level(db, economic_level)


def update_economic_level(db: Session, economic_level: EconomicLevel, economic_level_in: EconomicLevelUpdate) -> EconomicLevel:
    existing_economic_level = economic_level_crud.get_economic_level_by_name(db, economic_level_in.name)
    if existing_economic_level:
        raise HTTPException(status_code=400, detail="El nivel económico ya existe")
    return economic_level_crud.update_economic_level(db, economic_level, economic_level_in)


def delete_economic_level(db: Session, economic_level: EconomicLevel) -> None:
    economic_level_crud.delete_economic_level(db, economic_level)
