from collections.abc import Sequence

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.enums import LevelAcademicType
from app.crud import grade_crud, section_crud
from app.models.section import Section
from app.schemas.section import SectionCreate, SectionUpdate

_PREFIX_BY_LEVEL_TYPE: dict[LevelAcademicType, str] = {
    LevelAcademicType.REGULAR: "SR",
    LevelAcademicType.EXTRAORDINARIA: "SE",
}


def _resolve_level_type(db: Session, grade_id: int) -> LevelAcademicType:
    """Resolve the academic level type for a given grade.

    Navigates the Grade → Level relationship to determine
    whether the section belongs to a Regular or Extraordinaria level.
    """
    grade = grade_crud.get_grade(db, grade_id)
    if grade is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Grade with id {grade_id} not found",
        )
    return grade.level.type


def _generate_section_id(db: Session, level_type: LevelAcademicType) -> str:
    """Generate the next sequential section ID based on the level type.

    Uses MAX(id) strategy: always increments from the highest existing code
    for the given prefix, guaranteeing no collisions even when sections are deleted.
    """
    prefix = _PREFIX_BY_LEVEL_TYPE[level_type]
    last_id = section_crud.get_max_id_by_prefix(db, prefix)

    next_number = 1 if last_id is None else int(last_id.split("-")[1]) + 1
    return f"{prefix}-{next_number:03d}"


def get_section(db: Session, section_id: int | str) -> Section | None:
    return section_crud.get_section(db, section_id)


def get_sections(db: Session, skip: int = 0, limit: int = 100) -> Sequence[Section]:
    return section_crud.get_sections(db, skip=skip, limit=limit)


def create_section(db: Session, section_in: SectionCreate) -> Section:
    level_type = _resolve_level_type(db, section_in.grade_id)
    section_id = _generate_section_id(db, level_type)
    return section_crud.create_section(db, section_id, section_in)


def update_section(db: Session, section: Section, section_in: SectionUpdate) -> Section:
    return section_crud.update_section(db, section, section_in)


def delete_section(db: Session, section: Section) -> None:
    section_crud.delete_section(db, section)
