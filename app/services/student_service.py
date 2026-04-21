from collections.abc import Sequence
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate
from app.crud import student_crud


def get_student(db: Session, student_id: int | str) -> Student | None:
    return student_crud.get_student(db, student_id)


def get_students(db: Session, skip: int = 0, limit: int = 100) -> Sequence[Student]:
    return student_crud.get_students(db, skip=skip, limit=limit)


def create_student(db: Session, student: StudentCreate) -> Student:
    return student_crud.create_student(db, student)


def update_student(db: Session, student: Student, student_in: StudentUpdate) -> Student:
    return student_crud.update_student(db, student, student_in)


def delete_student(db: Session, student: Student) -> None:
    student_crud.delete_student(db, student)
