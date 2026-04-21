from collections.abc import Sequence

from sqlalchemy.orm import Session

from app.models.level import Level
from app.schemas.level import LevelCreate, LevelUpdate


def create_level(db: Session, level_in: LevelCreate) -> Level:
    level = Level(**level_in.model_dump())
    db.add(level)
    db.commit()
    db.refresh(level)
    return level


def get_level(db: Session, level_id: int | str) -> Level | None:
    return db.query(Level).filter(Level.id == level_id).first()


def get_levels(db: Session, skip: int = 0, limit: int = 100) -> Sequence[Level]:
    return db.query(Level).order_by(Level.id).offset(skip).limit(limit).all()


def update_level(
    db: Session, level: Level, level_in: LevelUpdate
) -> Level:
    data = level_in.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(level, key, value)
    db.add(level)
    db.commit()
    db.refresh(level)
    return level


def delete_level(db: Session, level: Level) -> None:
    db.delete(level)
    db.commit()
