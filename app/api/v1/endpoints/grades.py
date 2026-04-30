from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.services import grade_service
from app.dependencies import get_db, check_admin_or_super_admin
from app.schemas.grade import GradeCreate, GradeRead, GradeUpdate


router = APIRouter(dependencies=[Depends(check_admin_or_super_admin)])


@router.get(
    "/{grade_id}",
    response_model=GradeRead,
    summary="Obtener grado por ID",
    description="""
Retorna los datos de un grado académico específico.

**Requiere:** Rol `ADMIN` o `SUPER_ADMIN`.
""",
    responses={
        200: {"description": "Grado encontrado"},
        404: {"description": "Grado no encontrado"},
    },
)
def get_grade(
    grade_id: int, db: Session = Depends(get_db)
) -> GradeRead:
    grade = grade_service.get_grade(db, grade_id)
    if grade is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grade not found")
    return grade


@router.get(
    "",
    response_model=list[GradeRead],
    summary="Listar grados",
    description="""
Retorna la lista paginada de todos los grados académicos configurados en el sistema.

**Requiere:** Rol `ADMIN` o `SUPER_ADMIN`.

**Paginación:**
- `skip`: Número de registros a omitir (por defecto `0`).
- `limit`: Máximo de registros a retornar (por defecto `100`).
""",
    responses={
        200: {"description": "Lista de grados retornada exitosamente"},
    },
)
def get_grades(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[GradeRead]:
    grades = grade_service.get_grades(db, skip=skip, limit=limit)
    return list(grades)


@router.post(
    "",
    response_model=GradeRead,
    status_code=status.HTTP_201_CREATED,
    summary="Crear grado",
    description="""
Crea un nuevo grado académico y lo vincula a un nivel educativo.

**Requiere:** Rol `ADMIN` o `SUPER_ADMIN`.

**Reglas de negocio:**
- El nivel asociado (`level_id`) debe existir.
- **Protección de Nivel Regular:** No se permite crear grados en niveles de tipo `REGULAR` (su estructura es estática).
- El abreviatura o etiqueta (`tag`) debe ser única en todo el sistema.
- El nombre (`name`) debe ser único dentro del mismo nivel educativo.
""",
    responses={
        201: {"description": "Grado creado exitosamente"},
        400: {
            "description": "Regla de negocio violada",
            "content": {
                "application/json": {
                    "examples": {
                        "nivel_regular": {
                            "summary": "Nivel es REGULAR",
                            "value": {"detail": "No se permite crear grados en un nivel de tipo Regular"},
                        },
                    }
                }
            },
        },
        404: {"description": "Nivel educativo no encontrado"},
        409: {
            "description": "Conflicto de unicidad",
            "content": {
                "application/json": {
                    "examples": {
                        "tag_duplicado": {
                            "summary": "Tag duplicado",
                            "value": {"detail": "Ya existe un grado con este tag"},
                        },
                        "nombre_duplicado": {
                            "summary": "Nombre duplicado en el nivel",
                            "value": {"detail": "Ya existe un grado con este nombre en el nivel especificado"},
                        },
                    }
                }
            },
        },
    },
)
def create_grade(
    grade_in: GradeCreate, db: Session = Depends(get_db)
) -> GradeRead:
    grade = grade_service.create_grade(db, grade_in)
    return grade


@router.put(
    "/{grade_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Actualizar grado",
    description="""
Actualiza los datos de un grado académico existente. La actualización es parcial.

*Nota: Por diseño, no es posible cambiar un grado de nivel una vez creado.*

**Requiere:** Rol `ADMIN` o `SUPER_ADMIN`.

**Reglas de negocio:**
- **Protección de Nivel Regular:** No se permite editar grados que pertenecen a un nivel de tipo `REGULAR`.
- Si se envía un nuevo `tag`, debe ser único en todo el sistema.
- Si se envía un nuevo `name`, debe ser único dentro del mismo nivel educativo al que pertenece.
""",
    responses={
        204: {"description": "Grado actualizado exitosamente"},
        400: {
            "description": "Regla de negocio violada",
            "content": {
                "application/json": {
                    "examples": {
                        "nivel_regular": {
                            "summary": "Pertenece a nivel REGULAR",
                            "value": {"detail": "No se permite editar o actualizar grados que pertenecen a un nivel de tipo Regular"},
                        },
                    }
                }
            },
        },
        404: {"description": "Grado no encontrado"},
        409: {
            "description": "Conflicto de unicidad",
            "content": {
                "application/json": {
                    "examples": {
                        "tag_duplicado": {
                            "summary": "Tag duplicado",
                            "value": {"detail": "Ya existe un grado con este tag"},
                        },
                        "nombre_duplicado": {
                            "summary": "Nombre duplicado en el nivel",
                            "value": {"detail": "Ya existe un grado con este nombre en este nivel"},
                        },
                    }
                }
            },
        },
    },
)
def update_grade(
    grade_id: int, grade_in: GradeUpdate, db: Session = Depends(get_db)
) -> Response:
    grade = grade_service.get_grade(db, grade_id)
    if grade is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grade not found")
    grade_service.update_grade(db, grade, grade_in)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete(
    "/{grade_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar grado",
    description="""
Elimina permanentemente un grado académico del sistema.

**Requiere:** Rol `ADMIN` o `SUPER_ADMIN`.

**Reglas de negocio:**
- **Protección de Nivel Regular:** No se permite eliminar grados que pertenecen a un nivel de tipo `REGULAR`.
- **Integridad Referencial:** No se puede eliminar el grado si tiene secciones académicas (`sections`) asociadas. Se deben eliminar o reasignar las secciones primero.
""",
    responses={
        204: {"description": "Grado eliminado exitosamente"},
        400: {
            "description": "Regla de negocio violada o dependencia existente",
            "content": {
                "application/json": {
                    "examples": {
                        "nivel_regular": {
                            "summary": "Pertenece a nivel REGULAR",
                            "value": {"detail": "No se permite eliminar grados que pertenecen a un nivel de tipo Regular"},
                        },
                        "tiene_secciones": {
                            "summary": "Tiene secciones asociadas",
                            "value": {"detail": "No se puede eliminar el grado porque tiene secciones asociadas"},
                        },
                    }
                }
            },
        },
        404: {"description": "Grado no encontrado"},
    },
)
def delete_grade(
    grade_id: int, db: Session = Depends(get_db)
) -> Response:
    grade = grade_service.get_grade(db, grade_id)
    if grade is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grade not found")

    grade_service.delete_grade(db, grade)
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
