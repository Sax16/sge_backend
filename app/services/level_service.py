from collections.abc import Sequence
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.models.level import Level
from app.schemas.level import LevelCreate, LevelUpdate
from app.crud import level_crud


def get_level(db: Session, level_id: int | str) -> Level | None:
    return level_crud.get_level(db, level_id)


def get_levels(db: Session, skip: int = 0, limit: int = 100) -> Sequence[Level]:
    return level_crud.get_levels(db, skip=skip, limit=limit)


def create_level(db: Session, level: LevelCreate) -> Level:
    return level_crud.create_level(db, level)


def update_level(db: Session, level: Level, level_in: LevelUpdate) -> Level:
    return level_crud.update_level(db, level, level_in)


def delete_level(db: Session, level: Level) -> None:
    level_crud.delete_level(db, level)
