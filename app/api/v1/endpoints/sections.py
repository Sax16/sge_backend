from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.services import section_service
from app.dependencies import get_db, check_admin_or_super_admin
from app.schemas.section import SectionCreate, SectionRead, SectionUpdate


router = APIRouter(dependencies=[Depends(check_admin_or_super_admin)])


@router.get(
    "/{section_id}",
    response_model=SectionRead,
    summary="Obtener sección por ID",
    description="""
Retorna los datos de una sección específica (ej. `SR-001`).

**Requiere:** Rol `ADMIN` o `SUPER_ADMIN`.
""",
    responses={
        200: {"description": "Sección encontrada"},
        404: {"description": "Sección no encontrada"},
    },
)
def get_section(
    section_id: str, db: Session = Depends(get_db)
) -> SectionRead:
    section = section_service.get_section(db, section_id)
    if section is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Section not found")
    return section


@router.get(
    "",
    response_model=list[SectionRead],
    summary="Listar secciones",
    description="""
Retorna la lista paginada de todas las secciones del colegio.

**Requiere:** Rol `ADMIN` o `SUPER_ADMIN`.

**Paginación:**
- `skip`: Número de registros a omitir (por defecto `0`).
- `limit`: Máximo de registros a retornar (por defecto `100`).
""",
    responses={
        200: {"description": "Lista de secciones retornada exitosamente"},
    },
)
def get_sections(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[SectionRead]:
    sections = section_service.get_sections(db, skip=skip, limit=limit)
    return list(sections)


@router.post(
    "",
    response_model=SectionRead,
    status_code=status.HTTP_201_CREATED,
    summary="Crear sección",
    description="""
Crea una nueva sección dentro de un grado específico.

**Requiere:** Rol `ADMIN` o `SUPER_ADMIN`.

**Reglas de negocio:**
- El ID se genera automáticamente (ej. `SR-001` para Regular, `SE-001` para Extraordinaria).
- El `name` (ej. 'A', 'Unica') y el `tag` deben ser **únicos** dentro del mismo grado (ignorando mayúsculas y minúsculas).
- El `grade_id` debe existir en la base de datos.
""",
    responses={
        201: {"description": "Sección creada exitosamente"},
        400: {
            "description": "Regla de negocio violada",
            "content": {
                "application/json": {
                    "examples": {
                        "nombre_duplicado": {
                            "summary": "Nombre o Tag duplicado en el grado",
                            "value": {"detail": "Ya existe una sección con ese nombre en este grado."},
                        },
                    }
                }
            },
        },
        404: {"description": "Grado no encontrado"},
    },
)
def create_section(
    section_in: SectionCreate, db: Session = Depends(get_db)
) -> SectionRead:
    section = section_service.create_section(db, section_in)
    return section


@router.put(
    "/{section_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Actualizar sección",
    description="""
Actualiza los datos de una sección existente.

**Requiere:** Rol `ADMIN` o `SUPER_ADMIN`.

**Reglas de negocio:**
- Solo se permite modificar el `name` y el `tag`.
- No se permite transferir la sección a otro grado.
- Se verifica nuevamente la unicidad del `name` y `tag` dentro del grado.
""",
    responses={
        204: {"description": "Sección actualizada exitosamente"},
        400: {
            "description": "Regla de negocio violada",
            "content": {
                "application/json": {
                    "examples": {
                        "nombre_duplicado": {
                            "summary": "Nombre o Tag duplicado",
                            "value": {"detail": "Ya existe una sección con ese tag en este grado."},
                        },
                    }
                }
            },
        },
        404: {"description": "Sección no encontrada"},
    },
)
def update_section(
    section_id: str, section_in: SectionUpdate, db: Session = Depends(get_db)
) -> Response:
    section = section_service.get_section(db, section_id)
    if section is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Section not found")
    section_service.update_section(db, section, section_in)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete(
    "/{section_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar sección",
    description="""
Elimina permanentemente una sección del sistema.

**Requiere:** Rol `ADMIN` o `SUPER_ADMIN`.

**Regla de negocio:**
- No se puede eliminar una sección si tiene **alumnos matriculados** en ella.
""",
    responses={
        204: {"description": "Sección eliminada exitosamente"},
        400: {
            "description": "Dependencias existentes",
            "content": {
                "application/json": {
                    "examples": {
                        "tiene_matriculas": {
                            "summary": "Tiene alumnos matriculados",
                            "value": {"detail": "No se puede eliminar la sección porque tiene alumnos matriculados."},
                        },
                    }
                }
            },
        },
        404: {"description": "Sección no encontrada"},
    },
)
def delete_section(
    section_id: str, db: Session = Depends(get_db)
) -> Response:
    section = section_service.get_section(db, section_id)
    if section is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Section not found")
    
    section_service.delete_section(db, section)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
