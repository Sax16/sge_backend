from collections.abc import Sequence

from sqlalchemy.orm import Session

from app.models.section import Section
from app.schemas.section import SectionCreate, SectionUpdate


def create_section(db: Session, section_in: SectionCreate) -> Section:
    section = Section(**section_in.model_dump())
    db.add(section)
    db.commit()
    db.refresh(section)
    return section


def get_section(db: Session, section_id: int | str) -> Section | None:
    return db.query(Section).filter(Section.id == section_id).first()


def get_sections(db: Session, skip: int = 0, limit: int = 100) -> Sequence[Section]:
    return db.query(Section).order_by(Section.id).offset(skip).limit(limit).all()


def update_section(
    db: Session, section: Section, section_in: SectionUpdate
) -> Section:
    data = section_in.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(section, key, value)
    db.add(section)
    db.commit()
    db.refresh(section)
    return section


def delete_section(db: Session, section: Section) -> None:
    db.delete(section)
    db.commit()
