from collections.abc import Sequence
from datetime import date
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.core.enums import StudentStatus
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate
from app.crud import student_crud
from app.crud import economic_level_crud


def _validate_student_data(db: Session, student_in: StudentCreate | StudentUpdate, current_student: Student | None = None) -> None:
    if getattr(student_in, "dni", None):
        existing_student = student_crud.get_student_by_dni(db, student_in.dni)
        if existing_student and (not current_student or existing_student.id != current_student.id):
            raise HTTPException(status_code=400, detail="El DNI ya pertenece a otro estudiante")

    if getattr(student_in, "economic_level_id", None):
        if not economic_level_crud.get_economic_level(db, student_in.economic_level_id):
            raise HTTPException(status_code=404, detail="El nivel económico especificado no existe")

    if getattr(student_in, "birth_date", None):
        today = date.today()
        born = student_in.birth_date
        age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
        if age < 2:
            raise HTTPException(status_code=400, detail="El estudiante debe tener al menos 2 años de edad")


def get_student(db: Session, student_id: int | str) -> Student | None:
    return student_crud.get_student(db, student_id)


def get_students(db: Session, skip: int = 0, limit: int = 100) -> Sequence[Student]:
    return student_crud.get_students(db, skip=skip, limit=limit)


def create_student(db: Session, student: StudentCreate) -> Student:
    _validate_student_data(db, student)
    
    student.status = StudentStatus.PENDIENTE
    return student_crud.create_student(db, student)


def update_student(db: Session, student: Student, student_in: StudentUpdate) -> Student:
    _validate_student_data(db, student_in, current_student=student)
    
    if student_in.status is not None:
        if student_in.status not in [StudentStatus.RETIRADO, StudentStatus.EGRESADO]:
            raise HTTPException(
                status_code=400, 
                detail="Al actualizar, el estado solo puede cambiarse a Retirado o Egresado"
            )

    return student_crud.update_student(db, student, student_in)


def delete_student(db: Session, student: Student) -> None:
    student_in = StudentUpdate(status=StudentStatus.INACTIVE)
    student_crud.update_student(db, student, student_in)
