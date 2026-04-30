from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.services import level_service
from app.dependencies import get_db, check_admin_or_super_admin
from app.schemas.level import LevelCreate, LevelRead, LevelUpdate


router = APIRouter(dependencies=[Depends(check_admin_or_super_admin)])


@router.get(
    "/{level_id}",
    response_model=LevelRead,
    summary="Obtener nivel por ID",
    description="""
Retorna los datos de un nivel educativo específico, incluyendo
su nombre, tag, código modular y tipo académico.

**Requiere:** Rol `ADMIN` o `SUPER_ADMIN`.
""",
    responses={
        200: {"description": "Nivel encontrado"},
        404: {"description": "Nivel no encontrado"},
    },
)
def get_level(
    level_id: int, db: Session = Depends(get_db)
) -> LevelRead:
    level = level_service.get_level(db, level_id)
    if level is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Level not found")
    return level


@router.get(
    "",
    response_model=list[LevelRead],
    summary="Listar niveles",
    description="""
Retorna la lista paginada de todos los niveles educativos registrados
en el sistema (regulares y extraordinarios).

**Requiere:** Rol `ADMIN` o `SUPER_ADMIN`.

**Paginación:**
- `skip`: Número de registros a omitir (por defecto `0`).
- `limit`: Máximo de registros a retornar (por defecto `100`).
""",
    responses={
        200: {"description": "Lista de niveles retornada exitosamente"},
    },
)
def get_levels(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[LevelRead]:
    levels = level_service.get_levels(db, skip=skip, limit=limit)
    return list(levels)


@router.post(
    "",
    response_model=LevelRead,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nivel",
    description="""
Crea un nuevo nivel educativo en el sistema.

**Requiere:** Rol `ADMIN` o `SUPER_ADMIN`.

**Reglas de negocio:**
- Solo se permite crear niveles de tipo `EXTRAORDINARIA`.
- Los niveles de tipo `REGULAR` son precargados por el sistema
    y no pueden ser creados manualmente.
- El `name`, `tag` y `modularCode` deben ser únicos en todo el sistema.
""",
    responses={
        201: {"description": "Nivel creado exitosamente"},
        400: {
            "description": "Regla de negocio violada",
            "content": {
                "application/json": {
                    "examples": {
                        "tipo_no_permitido": {
                            "summary": "Tipo de nivel no permitido",
                            "value": {"detail": "Solo se permite crear niveles de tipo Extraordinaria"},
                        },
                    }
                }
            },
        },
        409: {
            "description": "Conflicto de integridad de datos",
            "content": {
                "application/json": {
                    "examples": {
                        "nombre_duplicado": {
                            "summary": "Nombre ya en uso",
                            "value": {"detail": "El nivel con el nombre 'Secundaria' ya existe."},
                        },
                    }
                }
            },
        },
    },
)
def create_level(
    level_in: LevelCreate, db: Session = Depends(get_db)
) -> LevelRead:
    level = level_service.create_level(db, level_in)
    return level


@router.put(
    "/{level_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Actualizar nivel",
    description="""
Actualiza los datos de un nivel educativo existente. Solo se modifican
los campos enviados (actualización parcial).

**Requiere:** Rol `ADMIN` o `SUPER_ADMIN`.

**Reglas de negocio:**
- **Niveles `REGULAR`:** Solo se permite actualizar el `modularCode`.
    No se puede modificar el `name` ni el `tag`.
- **Niveles `EXTRAORDINARIA`:** Se pueden actualizar todos los campos
    (`name`, `tag`, `modularCode`).
- El `name`, `tag` y `modularCode` deben ser únicos. Si se envían valores ya registrados por otro nivel, la petición será rechazada.
""",
    responses={
        204: {"description": "Nivel actualizado exitosamente"},
        400: {
            "description": "Regla de negocio violada",
            "content": {
                "application/json": {
                    "examples": {
                        "campo_no_permitido": {
                            "summary": "Campo protegido en nivel Regular",
                            "value": {"detail": "No se puede actualizar el nombre o el tag de un nivel de tipo Regular"},
                        },
                    }
                }
            },
        },
        404: {"description": "Nivel no encontrado"},
        409: {
            "description": "Conflicto de integridad de datos",
            "content": {
                "application/json": {
                    "examples": {
                        "tag_duplicado": {
                            "summary": "Tag ya en uso",
                            "value": {"detail": "El tag 'SEC' ya está en uso."},
                        },
                    }
                }
            },
        },
    },
)
def update_level(
    level_id: int, level_in: LevelUpdate, db: Session = Depends(get_db)
) -> Response:
    level = level_service.get_level(db, level_id)
    if level is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Level not found")
    level_service.update_level(db, level, level_in)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete(
    "/{level_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar nivel",
    description="""
Elimina permanentemente un nivel educativo del sistema.

**Requiere:** Rol `ADMIN` o `SUPER_ADMIN`.

**Reglas de negocio:**
- Solo se permite eliminar niveles de tipo `EXTRAORDINARIA`.
- Los niveles de tipo `REGULAR` son protegidos por el sistema
    y no pueden ser eliminados.
- Si el nivel tiene grados asociados, la eliminación será rechazada.
""",
    responses={
        204: {"description": "Nivel eliminado exitosamente"},
        400: {
            "description": "Regla de negocio violada",
            "content": {
                "application/json": {
                    "examples": {
                        "tipo_no_permitido": {
                            "summary": "Nivel Regular protegido",
                            "value": {"detail": "Solo se permite eliminar niveles de tipo Extraordinaria"},
                        },
                        "tiene_grados": {
                            "summary": "Tiene grados asociados",
                            "value": {"detail": "No se puede eliminar este nivel porque tiene grados asociados. Elimine o reasigne los grados primero."},
                        },
                    }
                }
            },
        },
        404: {"description": "Nivel no encontrado"},
    },
)
def delete_level(
    level_id: int, db: Session = Depends(get_db)
) -> Response:
    level = level_service.get_level(db, level_id)
    if level is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Level not found")

    level_service.delete_level(db, level)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
