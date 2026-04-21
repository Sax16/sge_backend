from collections.abc import Sequence

from sqlalchemy.orm import Session

from app.models.guardian_student import GuardianStudent
from app.schemas.guardian_student import GuardianStudentCreate, GuardianStudentUpdate


def create_guardian_student(db: Session, guardian_student_in: GuardianStudentCreate) -> GuardianStudent:
    guardian_student = GuardianStudent(**guardian_student_in.model_dump())
    db.add(guardian_student)
    db.commit()
    db.refresh(guardian_student)
    return guardian_student


def get_guardian_student(db: Session, guardian_student_id: int | str) -> GuardianStudent | None:
    return db.query(GuardianStudent).filter(GuardianStudent.id == guardian_student_id).first()


def get_guardian_students(db: Session, skip: int = 0, limit: int = 100) -> Sequence[GuardianStudent]:
    return db.query(GuardianStudent).order_by(GuardianStudent.id).offset(skip).limit(limit).all()


def update_guardian_student(
    db: Session, guardian_student: GuardianStudent, guardian_student_in: GuardianStudentUpdate
) -> GuardianStudent:
    data = guardian_student_in.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(guardian_student, key, value)
    db.add(guardian_student)
    db.commit()
    db.refresh(guardian_student)
    return guardian_student


def delete_guardian_student(db: Session, guardian_student: GuardianStudent) -> None:
    db.delete(guardian_student)
    db.commit()
