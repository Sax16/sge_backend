from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.services import economic_level_service
from app.dependencies import get_db, check_admin_or_super_admin
from app.schemas.economic_level import EconomicLevelCreate, EconomicLevelRead, EconomicLevelUpdate


router = APIRouter(dependencies=[Depends(check_admin_or_super_admin)])


@router.get(
    "/{economic_level_id}", 
    response_model=EconomicLevelRead, 
    summary="Obtener nivel económico por ID",
    description="""
Recupera los detalles de un nivel económico específico.

**Requiere:** Rol `ADMIN` o `SUPER_ADMIN`.
""",
    responses={
        200: {"description": "Nivel económico encontrado exitosamente"},
        404: {
            "description": "Nivel económico no encontrado",
            "content": {
                "application/json": {
                    "examples": {
                        "no_encontrado": {
                            "summary": "Nivel económico inexistente",
                            "value": {"detail": "EconomicLevel not found"},
                        }
                    }
                }
            }
        }
    }
)
def get_economic_level(
    economic_level_id: int, db: Session = Depends(get_db)
) -> EconomicLevelRead:
    economic_level = economic_level_service.get_economic_level(db, economic_level_id)
    if economic_level is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="EconomicLevel not found")
    return economic_level


@router.get(
    "", 
    response_model=list[EconomicLevelRead], 
    summary="Listar niveles económicos",
    description="""
Lista todos los niveles económicos registrados en el sistema, con soporte de paginación.

**Requiere:** Rol `ADMIN` o `SUPER_ADMIN`.
""",
    responses={
        200: {"description": "Lista de niveles económicos devuelta exitosamente"}
    }
)
def get_economic_levels(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[EconomicLevelRead]:
    economic_levels = economic_level_service.get_economic_levels(db, skip=skip, limit=limit)
    return list(economic_levels)


@router.post(
    "", 
    response_model=EconomicLevelRead, 
    status_code=status.HTTP_201_CREATED,
    summary="Crear nivel económico",
    description="""
Crea un nuevo nivel económico en el sistema.

**Requiere:** Rol `ADMIN` o `SUPER_ADMIN`.

**Reglas de negocio:**
- El nombre del nivel económico debe ser **único**. No pueden existir dos niveles con el mismo nombre.
""",
    responses={
        201: {"description": "Nivel económico creado exitosamente"},
        400: {
            "description": "Regla de negocio violada",
            "content": {
                "application/json": {
                    "examples": {
                        "nombre_duplicado": {
                            "summary": "Nombre ya existe",
                            "value": {"detail": "El nivel económico ya existe"},
                        }
                    }
                }
            }
        }
    }
)
def create_economic_level(
    economic_level_in: EconomicLevelCreate, db: Session = Depends(get_db)
) -> EconomicLevelRead:
    economic_level = economic_level_service.create_economic_level(db, economic_level_in)
    return economic_level


@router.put(
    "/{economic_level_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Actualizar nivel económico",
    description="""
Actualiza la información de un nivel económico existente.
Se pueden proporcionar campos parciales.

**Requiere:** Rol `ADMIN` o `SUPER_ADMIN`.

**Reglas de negocio:**
- Si se actualiza el nombre, este no puede coincidir con el nombre de otro nivel económico existente (excluyéndose a sí mismo).
""",
    responses={
        204: {"description": "Nivel económico actualizado exitosamente"},
        400: {
            "description": "Regla de negocio violada",
            "content": {
                "application/json": {
                    "examples": {
                        "nombre_en_uso": {
                            "summary": "Nombre en uso por otro nivel",
                            "value": {"detail": "El nombre del nivel económico ya está en uso"},
                        }
                    }
                }
            }
        },
        404: {
            "description": "Nivel económico no encontrado",
            "content": {
                "application/json": {
                    "examples": {
                        "no_encontrado": {
                            "summary": "Nivel económico inexistente",
                            "value": {"detail": "EconomicLevel not found"},
                        }
                    }
                }
            }
        }
    }
)
def update_economic_level(
    economic_level_id: int, economic_level_in: EconomicLevelUpdate, db: Session = Depends(get_db)
) -> Response:
    economic_level = economic_level_service.get_economic_level(db, economic_level_id)
    if economic_level is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="EconomicLevel not found")
    economic_level_service.update_economic_level(db, economic_level, economic_level_in)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete(
    "/{economic_level_id}", 
    status_code=status.HTTP_204_NO_CONTENT, 
    summary="Eliminar nivel económico",
    description="""
Elimina físicamente un nivel económico del sistema.

**Requiere:** Rol `ADMIN` o `SUPER_ADMIN`.

**Reglas de negocio:**
- **Integridad referencial:** No se puede eliminar si existen estudiantes asociados.
- **Integridad referencial:** No se puede eliminar si existen montos de catálogo de cobros asociados.
""",
    responses={
        204: {"description": "Nivel económico eliminado exitosamente"},
        400: {
            "description": "Regla de negocio violada",
            "content": {
                "application/json": {
                    "examples": {
                        "tiene_estudiantes": {
                            "summary": "Dependencia con estudiantes",
                            "value": {"detail": "No se puede eliminar porque tiene estudiantes asociados"},
                        },
                        "tiene_cobros": {
                            "summary": "Dependencia con cobros",
                            "value": {"detail": "No se puede eliminar porque tiene cobros asociados"},
                        }
                    }
                }
            }
        },
        404: {
            "description": "Nivel económico no encontrado",
            "content": {
                "application/json": {
                    "examples": {
                        "no_encontrado": {
                            "summary": "Nivel económico inexistente",
                            "value": {"detail": "EconomicLevel not found"},
                        }
                    }
                }
            }
        }
    }
)
def delete_economic_level(
    economic_level_id: int, db: Session = Depends(get_db)
) -> Response:
    economic_level = economic_level_service.get_economic_level(db, economic_level_id)
    if economic_level is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="EconomicLevel not found")

    economic_level_service.delete_economic_level(db, economic_level)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
