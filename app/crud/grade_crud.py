from collections.abc import Sequence

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.grade import Grade
from app.schemas.grade import GradeCreate, GradeUpdate


def check_duplicate_name_or_tag(
    db: Session, level_id: int, name: str, tag: str, exclude_id: int | None = None
) -> str | None:
    """
    Check if a grade with the same case-insensitive name (within the level)
    or tag (globally unique) already exists.
    Returns 'name' if name conflicts, 'tag' if tag conflicts, else None.
    """
    # Tag is globally unique
    tag_query = db.query(Grade).filter(func.lower(Grade.tag) == tag.lower())
    if exclude_id is not None:
        tag_query = tag_query.filter(Grade.id != exclude_id)
    if tag_query.first():
        return "tag"

    # Name is unique within the same level
    name_query = db.query(Grade).filter(
        Grade.level_id == level_id,
        func.lower(Grade.name) == name.lower(),
    )
    if exclude_id is not None:
        name_query = name_query.filter(Grade.id != exclude_id)
    if name_query.first():
        return "name"

    return None


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
