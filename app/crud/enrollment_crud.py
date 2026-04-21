from collections.abc import Sequence

from sqlalchemy.orm import Session

from app.models.enrollment import Enrollment
from app.schemas.enrollment import EnrollmentCreate, EnrollmentUpdate


def create_enrollment(db: Session, enrollment_in: EnrollmentCreate) -> Enrollment:
    enrollment = Enrollment(**enrollment_in.model_dump())
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment


def get_enrollment(db: Session, enrollment_id: int | str) -> Enrollment | None:
    return db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()


def get_enrollments(db: Session, skip: int = 0, limit: int = 100) -> Sequence[Enrollment]:
    return db.query(Enrollment).order_by(Enrollment.id).offset(skip).limit(limit).all()


def update_enrollment(
    db: Session, enrollment: Enrollment, enrollment_in: EnrollmentUpdate
) -> Enrollment:
    data = enrollment_in.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(enrollment, key, value)
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment


def delete_enrollment(db: Session, enrollment: Enrollment) -> None:
    db.delete(enrollment)
    db.commit()
