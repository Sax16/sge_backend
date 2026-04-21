from collections.abc import Sequence

from sqlalchemy.orm import Session

from app.models.academic_period import AcademicPeriod
from app.schemas.academic_period import AcademicPeriodCreate, AcademicPeriodUpdate


def create_academic_period(db: Session, academic_period_in: AcademicPeriodCreate) -> AcademicPeriod:
    academic_period = AcademicPeriod(**academic_period_in.model_dump())
    db.add(academic_period)
    db.commit()
    db.refresh(academic_period)
    return academic_period


def get_academic_period(db: Session, academic_period_id: int | str) -> AcademicPeriod | None:
    return db.query(AcademicPeriod).filter(AcademicPeriod.id == academic_period_id).first()


def get_academic_periods(db: Session, skip: int = 0, limit: int = 100) -> Sequence[AcademicPeriod]:
    return db.query(AcademicPeriod).order_by(AcademicPeriod.id).offset(skip).limit(limit).all()


def update_academic_period(
    db: Session, academic_period: AcademicPeriod, academic_period_in: AcademicPeriodUpdate
) -> AcademicPeriod:
    data = academic_period_in.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(academic_period, key, value)
    db.add(academic_period)
    db.commit()
    db.refresh(academic_period)
    return academic_period


def delete_academic_period(db: Session, academic_period: AcademicPeriod) -> None:
    db.delete(academic_period)
    db.commit()
