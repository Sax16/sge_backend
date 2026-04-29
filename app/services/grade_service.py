from collections.abc import Sequence
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.core.enums import LevelAcademicType
from app.models.grade import Grade
from app.schemas.grade import GradeCreate, GradeUpdate
from app.crud import grade_crud, level_crud


def get_grade(db: Session, grade_id: int | str) -> Grade | None:
    return grade_crud.get_grade(db, grade_id)


def get_grades(db: Session, skip: int = 0, limit: int = 100) -> Sequence[Grade]:
    return grade_crud.get_grades(db, skip=skip, limit=limit)


def create_grade(db: Session, grade: GradeCreate) -> Grade:
    level = level_crud.get_level(db, grade.level_id)
    if not level:
        raise HTTPException(status_code=404, detail="El nivel especificado no existe")
        
    if level.type == LevelAcademicType.REGULAR:
        raise HTTPException(
            status_code=400, 
            detail="No se permite crear grados en un nivel de tipo Regular"
        )
    return grade_crud.create_grade(db, grade)


def update_grade(db: Session, grade: Grade, grade_in: GradeUpdate) -> Grade:
    if grade.level.type == LevelAcademicType.REGULAR:
        raise HTTPException(
            status_code=400, 
            detail="No se permite editar o actualizar grados que pertenecen a un nivel de tipo Regular"
        )
    return grade_crud.update_grade(db, grade, grade_in)


def delete_grade(db: Session, grade: Grade) -> None:
    if grade.level.type == LevelAcademicType.REGULAR:
        raise HTTPException(
            status_code=400, 
            detail="No se permite eliminar grados que pertenecen a un nivel de tipo Regular"
        )
    grade_crud.delete_grade(db, grade)
