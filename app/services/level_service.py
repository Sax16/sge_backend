from app.core.enums import LevelAcademicType
from collections.abc import Sequence
from fastapi import HTTPException

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

    # Validar unicidad
    if level_crud.get_level_by_name(db, level.name):
        raise HTTPException(status_code=409, detail=f"El nivel con el nombre '{level.name}' ya existe.")
    
    if level_crud.get_level_by_tag(db, level.tag):
        raise HTTPException(status_code=409, detail=f"El tag '{level.tag}' ya está en uso.")
        
    if level.modular_code and level_crud.get_level_by_modular_code(db, level.modular_code):
        raise HTTPException(status_code=409, detail=f"El código modular '{level.modular_code}' ya está asignado a otro nivel.")

    return level_crud.create_level(db, level)


def update_level(db: Session, level: Level, level_in: LevelUpdate) -> Level:
    # Solo se permite actualizar el codigo modular de los niveles de tipo Regular
    if level.type == LevelAcademicType.REGULAR:
        if level_in.name is not None or level_in.tag is not None:
            raise HTTPException(
                status_code=400, 
                detail="No se puede actualizar el nombre o el tag de un nivel de tipo Regular"
            )

    # Validar unicidad ignorando el nivel actual
    if level_in.name is not None and level_in.name != level.name:
        if level_crud.get_level_by_name(db, level_in.name):
            raise HTTPException(status_code=409, detail=f"El nivel con el nombre '{level_in.name}' ya existe.")
            
    if level_in.tag is not None and level_in.tag != level.tag:
        if level_crud.get_level_by_tag(db, level_in.tag):
            raise HTTPException(status_code=409, detail=f"El tag '{level_in.tag}' ya está en uso.")
            
    if level_in.modular_code is not None and level_in.modular_code != level.modular_code:
        if level_crud.get_level_by_modular_code(db, level_in.modular_code):
            raise HTTPException(status_code=409, detail=f"El código modular '{level_in.modular_code}' ya está asignado a otro nivel.")

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