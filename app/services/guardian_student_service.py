from collections.abc import Sequence
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.models.guardian_student import GuardianStudent
from app.schemas.guardian_student import GuardianStudentCreate, GuardianStudentUpdate
from app.crud import guardian_student_crud


def get_guardian_student(db: Session, guardian_student_id: int | str) -> GuardianStudent | None:
    return guardian_student_crud.get_guardian_student(db, guardian_student_id)


def get_guardian_students(db: Session, skip: int = 0, limit: int = 100) -> Sequence[GuardianStudent]:
    return guardian_student_crud.get_guardian_students(db, skip=skip, limit=limit)


def create_guardian_student(db: Session, guardian_student: GuardianStudentCreate) -> GuardianStudent:
    return guardian_student_crud.create_guardian_student(db, guardian_student)


def update_guardian_student(db: Session, guardian_student: GuardianStudent, guardian_student_in: GuardianStudentUpdate) -> GuardianStudent:
    return guardian_student_crud.update_guardian_student(db, guardian_student, guardian_student_in)


def delete_guardian_student(db: Session, guardian_student: GuardianStudent) -> None:
    guardian_student_crud.delete_guardian_student(db, guardian_student)
