from collections.abc import Sequence
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.models.academic_period import AcademicPeriod
from app.schemas.academic_period import AcademicPeriodCreate, AcademicPeriodUpdate
from app.crud import academic_period_crud


def get_academic_period(db: Session, academic_period_id: int | str) -> AcademicPeriod | None:
    return academic_period_crud.get_academic_period(db, academic_period_id)


def get_academic_periods(db: Session, skip: int = 0, limit: int = 100) -> Sequence[AcademicPeriod]:
    return academic_period_crud.get_academic_periods(db, skip=skip, limit=limit)


def create_academic_period(db: Session, academic_period: AcademicPeriodCreate) -> AcademicPeriod:
    return academic_period_crud.create_academic_period(db, academic_period)


def update_academic_period(db: Session, academic_period: AcademicPeriod, academic_period_in: AcademicPeriodUpdate) -> AcademicPeriod:
    return academic_period_crud.update_academic_period(db, academic_period, academic_period_in)


def delete_academic_period(db: Session, academic_period: AcademicPeriod) -> None:
    academic_period_crud.delete_academic_period(db, academic_period)
