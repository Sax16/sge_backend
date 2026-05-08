from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.services import student_service
from app.dependencies import get_db, check_admin_or_super_admin
from app.schemas.student import StudentCreate, StudentRead, StudentUpdate


router = APIRouter(dependencies=[Depends(check_admin_or_super_admin)])


@router.get(
    "/{student_id}", 
    response_model=StudentRead, 
    summary="Obtener estudiante por ID",
    description="""
Recupera los detalles de un estudiante específico a partir de su ID.

**Requiere:** Rol `ADMIN` o `SUPER_ADMIN`.
""",
    responses={
        200: {"description": "Estudiante encontrado exitosamente"},
        404: {
            "description": "Estudiante no encontrado",
            "content": {
                "application/json": {
                    "examples": {
                        "no_encontrado": {
                            "summary": "Estudiante inexistente",
                            "value": {"detail": "Student not found"},
                        }
                    }
                }
            }
        }
    }
)
def get_student(
    student_id: int, db: Session = Depends(get_db)
) -> StudentRead:
    student = student_service.get_student(db, student_id)
    if student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return student


@router.get(
    "", 
    response_model=list[StudentRead], 
    summary="Listar estudiantes",
    description="""
Lista a todos los estudiantes registrados en el sistema, con soporte de paginación.

**Requiere:** Rol `ADMIN` o `SUPER_ADMIN`.
""",
    responses={
        200: {"description": "Lista de estudiantes devuelta exitosamente"}
    }
)
def get_students(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[StudentRead]:
    students = student_service.get_students(db, skip=skip, limit=limit)
    return list(students)


@router.post(
    "", 
    response_model=StudentRead, 
    status_code=status.HTTP_201_CREATED,
    summary="Registrar estudiante",
    description="""
Registra un nuevo estudiante en el sistema.

**Requiere:** Rol `ADMIN` o `SUPER_ADMIN`.

**Reglas de negocio:**
- **DNI Único**: El `dni` no puede estar registrado previamente en otro estudiante.
- **Edad Mínima**: La `birth_date` debe indicar que el estudiante tiene al menos 2 años de edad.
- **Nivel Económico**: El `economic_level_id` debe corresponder a un nivel económico existente.
- **Estado Automático**: El estado del estudiante será forzado a `PENDIENTE` automáticamente al crearse.
""",
    responses={
        201: {"description": "Estudiante registrado exitosamente"},
        400: {
            "description": "Regla de negocio violada",
            "content": {
                "application/json": {
                    "examples": {
                        "dni_duplicado": {
                            "summary": "DNI ya registrado",
                            "value": {"detail": "El DNI ya pertenece a otro estudiante"},
                        },
                        "edad_invalida": {
                            "summary": "Menor de 2 años",
                            "value": {"detail": "El estudiante debe tener al menos 2 años de edad"},
                        }
                    }
                }
            }
        },
        404: {
            "description": "Recurso relacionado no encontrado",
            "content": {
                "application/json": {
                    "examples": {
                        "nivel_economico_invalido": {
                            "summary": "Nivel económico no existe",
                            "value": {"detail": "El nivel económico especificado no existe"},
                        }
                    }
                }
            }
        }
    }
)
def create_student(
    student_in: StudentCreate, db: Session = Depends(get_db)
) -> StudentRead:
    student = student_service.create_student(db, student_in)
    return student


@router.put(
    "/{student_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Actualizar estudiante",
    description="""
Actualiza la información de un estudiante existente. Se admiten campos parciales.

**Requiere:** Rol `ADMIN` o `SUPER_ADMIN`.

**Reglas de negocio:**
- **DNI Único**: Si se actualiza el `dni`, este no puede pertenecer a otro estudiante diferente.
- **Edad Mínima**: Si se actualiza la `birth_date`, el estudiante debe mantener al menos 2 años de edad.
- **Nivel Económico**: Si se actualiza el `economic_level_id`, debe existir.
- **Transición de Estado**: Si se envía un nuevo `status`, SOLO puede ser `Retirado` o `Egresado`.
""",
    responses={
        204: {"description": "Estudiante actualizado exitosamente"},
        400: {
            "description": "Regla de negocio violada",
            "content": {
                "application/json": {
                    "examples": {
                        "dni_duplicado": {
                            "summary": "DNI ya registrado en otro",
                            "value": {"detail": "El DNI ya pertenece a otro estudiante"},
                        },
                        "edad_invalida": {
                            "summary": "Menor de 2 años",
                            "value": {"detail": "El estudiante debe tener al menos 2 años de edad"},
                        },
                        "estado_invalido": {
                            "summary": "Transición de estado no permitida",
                            "value": {"detail": "Al actualizar, el estado solo puede cambiarse a Retirado o Egresado"},
                        }
                    }
                }
            }
        },
        404: {
            "description": "Recurso no encontrado",
            "content": {
                "application/json": {
                    "examples": {
                        "estudiante_no_encontrado": {
                            "summary": "Estudiante inexistente",
                            "value": {"detail": "Student not found"},
                        },
                        "nivel_economico_invalido": {
                            "summary": "Nivel económico no existe",
                            "value": {"detail": "El nivel económico especificado no existe"},
                        }
                    }
                }
            }
        }
    }
)
def update_student(
    student_id: int, student_in: StudentUpdate, db: Session = Depends(get_db)
) -> Response:
    student = student_service.get_student(db, student_id)
    if student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    student_service.update_student(db, student, student_in)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete(
    "/{student_id}", 
    status_code=status.HTTP_204_NO_CONTENT, 
    summary="Eliminar estudiante (Lógico)",
    description="""
Elimina a un estudiante del sistema. 

**Nota de Arquitectura:** Por razones de integridad referencial e historial transaccional (matrículas, cobros), la eliminación es **lógica** (Soft Delete). El registro no se borra físicamente de la base de datos, sino que su estado pasa a `Inactivo`.

**Requiere:** Rol `ADMIN` o `SUPER_ADMIN`.
""",
    responses={
        204: {"description": "Estudiante eliminado lógicamente exitosamente"},
        404: {
            "description": "Estudiante no encontrado",
            "content": {
                "application/json": {
                    "examples": {
                        "no_encontrado": {
                            "summary": "Estudiante inexistente",
                            "value": {"detail": "Student not found"},
                        }
                    }
                }
            }
        }
    }
)
def delete_student(
    student_id: int, db: Session = Depends(get_db)
) -> Response:
    student = student_service.get_student(db, student_id)
    if student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    student_service.delete_student(db, student)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
