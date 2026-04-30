from collections.abc import Sequence

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.level import Level
from app.schemas.level import LevelCreate, LevelUpdate


def check_duplicate_name_or_tag(
    db: Session, name: str, tag: str, exclude_id: int | None = None
) -> str | None:
    """
    Check if a level with the same case-insensitive name or tag already exists.
    Returns 'name' if name conflicts, 'tag' if tag conflicts, else None.
    """
    query = db.query(Level).filter(
        (func.lower(Level.name) == name.lower())
        | (func.lower(Level.tag) == tag.lower())
    )
    if exclude_id is not None:
        query = query.filter(Level.id != exclude_id)

    conflict = query.first()
    if conflict:
        if conflict.name.lower() == name.lower():
            return "name"
        return "tag"
    return None


def get_level_by_modular_code(
    db: Session, modular_code: str, exclude_id: int | None = None
) -> Level | None:
    """Return a level matching the given modular_code, optionally excluding an ID."""
    query = db.query(Level).filter(Level.modular_code == modular_code)
    if exclude_id is not None:
        query = query.filter(Level.id != exclude_id)
    return query.first()


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
