from app.core.enums import LevelAcademicType
from collections.abc import Sequence
from fastapi import HTTPException, status

from sqlalchemy.orm import Session

from app.models.level import Level
from app.schemas.level import LevelCreate, LevelUpdate
from app.crud import level_crud


def get_level(db: Session, level_id: int | str) -> Level | None:
    return level_crud.get_level(db, level_id)


def get_levels(db: Session, skip: int = 0, limit: int = 100) -> Sequence[Level]:
    return level_crud.get_levels(db, skip=skip, limit=limit)


def create_level(db: Session, level: LevelCreate) -> Level:
    # Solo se permite crear niveles de tipo Extraordinaria
    if not _is_extraordinary_level(level):
        raise HTTPException(
            status_code=400, 
            detail=f"Solo se permite crear niveles de tipo {LevelAcademicType.EXTRAORDINARIA.value}"
        )

    # Validar unicidad (case-insensitive para name y tag)
    conflict = level_crud.check_duplicate_name_or_tag(db, level.name, level.tag)
    if conflict:
        field_es = "nombre" if conflict == "name" else "tag"
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe un nivel con ese {field_es}."
        )
        
    if level.modular_code and level_crud.get_level_by_modular_code(db, level.modular_code):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"El código modular '{level.modular_code}' ya está asignado a otro nivel."
        )

    return level_crud.create_level(db, level)


def update_level(db: Session, level: Level, level_in: LevelUpdate) -> Level:
    # Solo se permite actualizar el codigo modular de los niveles de tipo Regular
    if level.type == LevelAcademicType.REGULAR:
        if level_in.name is not None or level_in.tag is not None:
            raise HTTPException(
                status_code=400, 
                detail="No se puede actualizar el nombre o el tag de un nivel de tipo Regular"
            )

    # Resolver valores efectivos (lo que viene en el payload o lo que ya existe)
    name = level_in.name if level_in.name is not None else level.name
    tag = level_in.tag if level_in.tag is not None else level.tag

    # Validar unicidad (case-insensitive para name y tag)
    conflict = level_crud.check_duplicate_name_or_tag(db, name, tag, exclude_id=level.id)
    if conflict:
        field_es = "nombre" if conflict == "name" else "tag"
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe un nivel con ese {field_es}."
        )

    if level_in.modular_code is not None:
        existing = level_crud.get_level_by_modular_code(
            db, level_in.modular_code, exclude_id=level.id
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"El código modular '{level_in.modular_code}' ya está asignado a otro nivel."
            )

    return level_crud.update_level(db, level, level_in)


def delete_level(db: Session, level: Level) -> None:
    # Solo se permite eliminar niveles de tipo Extraordinaria
    if not _is_extraordinary_level(level):
        raise HTTPException(
            status_code=400, 
            detail=f"Solo se permite eliminar niveles de tipo {LevelAcademicType.EXTRAORDINARIA.value}"
        )

    # Validar que no tenga grados asociados
    if level.grades:
        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar este nivel porque tiene grados asociados. Elimine o reasigne los grados primero."
        )

    level_crud.delete_level(db, level)


def _is_extraordinary_level(level: LevelCreate | Level) -> bool:
    return level.type == LevelAcademicType.EXTRAORDINARIA