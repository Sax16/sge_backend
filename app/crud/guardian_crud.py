from collections.abc import Sequence

from sqlalchemy.orm import Session

from app.models.guardian import Guardian
from app.schemas.guardian import GuardianCreate, GuardianUpdate


def create_guardian(db: Session, guardian_in: GuardianCreate) -> Guardian:
    guardian = Guardian(**guardian_in.model_dump())
    db.add(guardian)
    db.commit()
    db.refresh(guardian)
    return guardian


def get_guardian(db: Session, guardian_id: int | str) -> Guardian | None:
    return db.query(Guardian).filter(Guardian.id == guardian_id).first()


def get_guardians(db: Session, skip: int = 0, limit: int = 100) -> Sequence[Guardian]:
    return db.query(Guardian).order_by(Guardian.id).offset(skip).limit(limit).all()


def update_guardian(
    db: Session, guardian: Guardian, guardian_in: GuardianUpdate
) -> Guardian:
    data = guardian_in.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(guardian, key, value)
    db.add(guardian)
    db.commit()
    db.refresh(guardian)
    return guardian


def delete_guardian(db: Session, guardian: Guardian) -> None:
    db.delete(guardian)
    db.commit()
