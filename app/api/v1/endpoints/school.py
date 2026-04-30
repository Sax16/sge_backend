from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.services import school_service
from app.dependencies import get_db, check_admin_or_super_admin
from app.schemas.school import SchoolCreate, SchoolRead, SchoolUpdate


router = APIRouter(dependencies=[Depends(check_admin_or_super_admin)])


@router.post(
    "",
    response_model=SchoolRead,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar colegio",
    description="""
Registra la información general de la institución educativa.
Solo se permite **un único registro** de colegio en el sistema.

**Requiere:** Rol `ADMIN` o `SUPER_ADMIN`.

**Reglas de negocio:**
- No puede existir más de un colegio registrado.
- El `headmasterId` debe corresponder a un empleado existente con
    posición `DIRECTOR`.
- El `deputyDirectorId` (opcional) debe corresponder a un empleado
    existente con posición `SUBDIRECTOR`.
- El director y el subdirector no pueden ser la misma persona.
- El `ruc` debe ser un número de 11 dígitos que comience con `10` o `20`.
""",
    responses={
        201: {"description": "Colegio registrado exitosamente"},
        400: {
            "description": "Regla de negocio violada",
            "content": {
                "application/json": {
                    "examples": {
                        "colegio_existente": {
                            "summary": "Ya existe un colegio",
                            "value": {"detail": "Ya existe un colegio registrado. Solo se permite un registro de colegio."},
                        },
                        "director_no_es_director": {
                            "summary": "Empleado no tiene posición DIRECTOR",
                            "value": {"detail": "El empleado asignado como director no tiene el rol de director"},
                        },
                        "subdirector_no_es_subdirector": {
                            "summary": "Empleado no tiene posición SUBDIRECTOR",
                            "value": {"detail": "El empleado asignado como subdirector no tiene el rol de subdirector"},
                        },
                        "misma_persona": {
                            "summary": "Director y subdirector iguales",
                            "value": {"detail": "El director y el subdirector no pueden ser la misma persona."},
                        },
                    }
                }
            },
        },
        404: {
            "description": "Empleado referenciado no encontrado",
            "content": {
                "application/json": {
                    "examples": {
                        "director_no_existe": {
                            "summary": "Director no encontrado",
                            "value": {"detail": "El empleado asignado como director no existe"},
                        },
                        "subdirector_no_existe": {
                            "summary": "Subdirector no encontrado",
                            "value": {"detail": "El empleado asignado como subdirector no existe"},
                        },
                    }
                }
            },
        },
    },
)
def create_school(
    school_in: SchoolCreate, db: Session = Depends(get_db)
) -> SchoolRead:
    school = school_service.create_school(db, school_in)
    return school


@router.get(
    "/{school_id}",
    response_model=SchoolRead,
    summary="Obtener colegio por ID",
    description="""
Retorna la información completa del colegio, incluyendo datos
fiscales, directivos asignados y timestamps.

**Requiere:** Rol `ADMIN` o `SUPER_ADMIN`.
""",
    responses={
        200: {"description": "Colegio encontrado"},
        404: {"description": "Colegio no encontrado"},
    },
)
def get_school(
    school_id: int, db: Session = Depends(get_db)
) -> SchoolRead:
    school = school_service.get_school(db, school_id)
    if school is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="School not found")
    return school


@router.put(
    "/{school_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Actualizar colegio",
    description="""
Actualiza los datos del colegio. Solo se modifican los campos
enviados (actualización parcial).

**Requiere:** Rol `ADMIN` o `SUPER_ADMIN`.

**Reglas de negocio:**
- Si se cambia el `headmasterId`, el nuevo empleado debe existir y
    tener posición `DIRECTOR`.
- Si se cambia el `deputyDirectorId`, el nuevo empleado debe existir
    y tener posición `SUBDIRECTOR`.
- El director y el subdirector no pueden ser la misma persona
    (se valida contra el valor actual si solo se cambia uno de los dos).
""",
    responses={
        204: {"description": "Colegio actualizado exitosamente"},
        400: {
            "description": "Regla de negocio violada",
            "content": {
                "application/json": {
                    "examples": {
                        "director_no_es_director": {
                            "summary": "Empleado no tiene posición DIRECTOR",
                            "value": {"detail": "El empleado asignado como director no tiene el rol de director"},
                        },
                        "subdirector_no_es_subdirector": {
                            "summary": "Empleado no tiene posición SUBDIRECTOR",
                            "value": {"detail": "El empleado asignado como subdirector no tiene el rol de subdirector"},
                        },
                        "misma_persona": {
                            "summary": "Director y subdirector iguales",
                            "value": {"detail": "El director y el subdirector no pueden ser la misma persona."},
                        },
                    }
                }
            },
        },
        404: {
            "description": "Recurso no encontrado",
            "content": {
                "application/json": {
                    "examples": {
                        "colegio_no_existe": {
                            "summary": "Colegio no encontrado",
                            "value": {"detail": "School not found"},
                        },
                        "director_no_existe": {
                            "summary": "Director no encontrado",
                            "value": {"detail": "El empleado asignado como director no existe"},
                        },
                        "subdirector_no_existe": {
                            "summary": "Subdirector no encontrado",
                            "value": {"detail": "El empleado asignado como subdirector no existe"},
                        },
                    }
                }
            },
        },
    },
)
def update_school(
    school_id: int, school_in: SchoolUpdate, db: Session = Depends(get_db)
) -> Response:
    school = school_service.get_school(db, school_id)
    if school is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="School not found")
    school_service.update_school(db, school, school_in)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
