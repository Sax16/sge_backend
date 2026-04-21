from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.services import section_service
from app.dependencies import get_db, check_admin_or_super_admin
from app.schemas.section import SectionCreate, SectionRead, SectionUpdate


router = APIRouter(dependencies=[Depends(check_admin_or_super_admin)])


@router.get("/{section_id}", response_model=SectionRead, description="Get a section by ID")
def get_section(
    section_id: str, db: Session = Depends(get_db)
) -> SectionRead:
    section = section_service.get_section(db, section_id)
    if section is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Section not found")
    return section


@router.get("", response_model=list[SectionRead], description="List all sections")
def get_sections(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[SectionRead]:
    sections = section_service.get_sections(db, skip=skip, limit=limit)
    return list(sections)


@router.post(
    "", response_model=SectionRead, status_code=status.HTTP_201_CREATED,
    description="Create a new section"
)
def create_section(
    section_in: SectionCreate, db: Session = Depends(get_db)
) -> SectionRead:
    section = section_service.create_section(db, section_in)
    return section


@router.put(
    "/{section_id}", status_code=status.HTTP_204_NO_CONTENT,
    description="Update a section by ID"
)
def update_section(
    section_id: str, section_in: SectionUpdate, db: Session = Depends(get_db)
) -> Response:
    section = section_service.get_section(db, section_id)
    if section is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Section not found")
    section_service.update_section(db, section, section_in)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/{section_id}", status_code=status.HTTP_204_NO_CONTENT, description="Delete a section by ID")
def delete_section(
    section_id: str, db: Session = Depends(get_db)
) -> Response:
    section = section_service.get_section(db, section_id)
    if section is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Section not found")

    try:
        section_service.delete_section(db, section)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se puede eliminar porque tiene registros relacionados.")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
