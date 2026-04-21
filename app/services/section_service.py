from collections.abc import Sequence
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.models.section import Section
from app.schemas.section import SectionCreate, SectionUpdate
from app.crud import section_crud


def get_section(db: Session, section_id: int | str) -> Section | None:
    return section_crud.get_section(db, section_id)


def get_sections(db: Session, skip: int = 0, limit: int = 100) -> Sequence[Section]:
    return section_crud.get_sections(db, skip=skip, limit=limit)


def create_section(db: Session, section: SectionCreate) -> Section:
    return section_crud.create_section(db, section)


def update_section(db: Session, section: Section, section_in: SectionUpdate) -> Section:
    return section_crud.update_section(db, section, section_in)


def delete_section(db: Session, section: Section) -> None:
    section_crud.delete_section(db, section)
