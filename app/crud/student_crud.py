from collections.abc import Sequence

from sqlalchemy.orm import Session, joinedload

from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate


def create_student(db: Session, student_in: StudentCreate) -> Student:
    student = Student(**student_in.model_dump())
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


def get_student(db: Session, student_id: int | str) -> Student | None:
    return db.query(Student).options(joinedload(Student.economic_level)).filter(Student.id == student_id).first()


def get_students(db: Session, skip: int = 0, limit: int = 100) -> Sequence[Student]:
    return db.query(Student).options(joinedload(Student.economic_level)).order_by(Student.id).offset(skip).limit(limit).all()


def update_student(
    db: Session, student: Student, student_in: StudentUpdate
) -> Student:
    data = student_in.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(student, key, value)
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


def delete_student(db: Session, student: Student) -> None:
    db.delete(student)
    db.commit()
