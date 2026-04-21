from collections.abc import Sequence
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.models.enrollment import Enrollment
from app.schemas.enrollment import EnrollmentCreate, EnrollmentUpdate
from app.crud import enrollment_crud


def get_enrollment(db: Session, enrollment_id: int | str) -> Enrollment | None:
    return enrollment_crud.get_enrollment(db, enrollment_id)


def get_enrollments(db: Session, skip: int = 0, limit: int = 100) -> Sequence[Enrollment]:
    return enrollment_crud.get_enrollments(db, skip=skip, limit=limit)


def create_enrollment(db: Session, enrollment: EnrollmentCreate) -> Enrollment:
    return enrollment_crud.create_enrollment(db, enrollment)


def update_enrollment(db: Session, enrollment: Enrollment, enrollment_in: EnrollmentUpdate) -> Enrollment:
    return enrollment_crud.update_enrollment(db, enrollment, enrollment_in)


def delete_enrollment(db: Session, enrollment: Enrollment) -> None:
    enrollment_crud.delete_enrollment(db, enrollment)
