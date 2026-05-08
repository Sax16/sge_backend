from sqlalchemy import func
from collections.abc import Sequence

from sqlalchemy.orm import Session

from app.models.economic_level import EconomicLevel
from app.schemas.economic_level import EconomicLevelCreate, EconomicLevelUpdate


def create_economic_level(db: Session, economic_level_in: EconomicLevelCreate) -> EconomicLevel:
    economic_level = EconomicLevel(**economic_level_in.model_dump())
    db.add(economic_level)
    db.commit()
    db.refresh(economic_level)
    return economic_level


def get_economic_level(db: Session, economic_level_id: int | str) -> EconomicLevel | None:
    return db.query(EconomicLevel).filter(EconomicLevel.id == economic_level_id).first()


def get_economic_level_by_name(db: Session, name: str) -> EconomicLevel | None:
    return db.query(EconomicLevel).filter(func.lower(EconomicLevel.name) == name.lower()).first()


def get_economic_levels(db: Session, skip: int = 0, limit: int = 100) -> Sequence[EconomicLevel]:
    return db.query(EconomicLevel).order_by(EconomicLevel.id).offset(skip).limit(limit).all()


def update_economic_level(
    db: Session, economic_level: EconomicLevel, economic_level_in: EconomicLevelUpdate
) -> EconomicLevel:
    data = economic_level_in.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(economic_level, key, value)
    db.add(economic_level)
    db.commit()
    db.refresh(economic_level)
    return economic_level


def delete_economic_level(db: Session, economic_level: EconomicLevel) -> None:
    db.delete(economic_level)
    db.commit()
