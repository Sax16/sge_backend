from collections.abc import Sequence

from sqlalchemy.orm import Session

from app.models.grade import Grade
from app.schemas.grade import GradeCreate, GradeUpdate


def create_grade(db: Session, grade_in: GradeCreate) -> Grade:
    grade = Grade(**grade_in.model_dump())
    db.add(grade)
    db.commit()
    db.refresh(grade)
    return grade


def get_grade(db: Session, grade_id: int | str) -> Grade | None:
    return db.query(Grade).filter(Grade.id == grade_id).first()


def get_grades(db: Session, skip: int = 0, limit: int = 100) -> Sequence[Grade]:
    return db.query(Grade).order_by(Grade.id).offset(skip).limit(limit).all()


def update_grade(
    db: Session, grade: Grade, grade_in: GradeUpdate
) -> Grade:
    data = grade_in.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(grade, key, value)
    db.add(grade)
    db.commit()
    db.refresh(grade)
    return grade


def delete_grade(db: Session, grade: Grade) -> None:
    db.delete(grade)
    db.commit()


def get_grade_by_tag(db: Session, tag: str) -> Grade | None:
    return db.query(Grade).filter(Grade.tag == tag).first()


def get_grade_by_name_and_level(db: Session, name: str, level_id: int) -> Grade | None:
    return db.query(Grade).filter(Grade.name == name, Grade.level_id == level_id).first()
