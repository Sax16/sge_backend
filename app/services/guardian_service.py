from collections.abc import Sequence
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.models.guardian import Guardian
from app.schemas.guardian import GuardianCreate, GuardianUpdate
from app.crud import guardian_crud


def get_guardian(db: Session, guardian_id: int | str) -> Guardian | None:
    return guardian_crud.get_guardian(db, guardian_id)


def get_guardians(db: Session, skip: int = 0, limit: int = 100) -> Sequence[Guardian]:
    return guardian_crud.get_guardians(db, skip=skip, limit=limit)


def create_guardian(db: Session, guardian: GuardianCreate) -> Guardian:
    return guardian_crud.create_guardian(db, guardian)


def update_guardian(db: Session, guardian: Guardian, guardian_in: GuardianUpdate) -> Guardian:
    return guardian_crud.update_guardian(db, guardian, guardian_in)


def delete_guardian(db: Session, guardian: Guardian) -> None:
    guardian_crud.delete_guardian(db, guardian)
