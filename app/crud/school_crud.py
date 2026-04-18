from sqlalchemy.orm import Session

from app.models.school import School
from app.schemas.school import SchoolCreate, SchoolUpdate


def create_school(db: Session, school_in: SchoolCreate) -> School:
    school = School(**school_in.model_dump())
    db.add(school)
    db.commit()
    db.refresh(school)
    return school


def get_school(db: Session, school_id: int) -> School | None:
    return db.query(School).filter(School.id == school_id).first()


def update_school(
    db: Session, school: School, school_in: SchoolUpdate
) -> School:
    data = school_in.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(school, key, value)
    db.add(school)
    db.commit()
    db.refresh(school)
    return school
