from collections.abc import Sequence

from sqlalchemy import exists, func
from sqlalchemy.orm import Session

from app.models.enrollment import Enrollment
from app.models.section import Section
from app.schemas.section import SectionCreate, SectionUpdate


def check_duplicate_name_or_tag(
    db: Session, grade_id: int, name: str, tag: str, exclude_id: str | None = None
) -> str | None:
    """
    Check if a section with the same case-insensitive name or tag already exists in the grade.
    Returns 'name' if name conflicts, 'tag' if tag conflicts, else None.
    """
    query = db.query(Section).filter(
        Section.grade_id == grade_id,
        (func.lower(Section.name) == name.lower()) | (func.lower(Section.tag) == tag.lower())
    )
    if exclude_id:
        query = query.filter(Section.id != exclude_id)
        
    conflict = query.first()
    if conflict:
        if conflict.name.lower() == name.lower():
            return "name"
        return "tag"
    return None


def has_enrollments(db: Session, section_id: str) -> bool:
    """Check if a section has any associated enrollments."""
    return db.query(
        exists().where(Enrollment.section_id == section_id)
    ).scalar()


def get_max_id_by_prefix(db: Session, prefix: str) -> str | None:
    """Return the highest section ID matching the given prefix, or None if no match exists."""
    return db.query(func.max(Section.id)).filter(
        Section.id.like(f"{prefix}-%")
    ).scalar()


def create_section(db: Session, section_id: str, section_in: SectionCreate) -> Section:
    """Persist a new section with the given pre-generated ID."""
    section = Section(id=section_id, **section_in.model_dump())
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
