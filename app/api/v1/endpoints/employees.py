from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.services import employee_service
from app.dependencies import get_db, check_admin_or_super_admin
from app.schemas.employee import EmployeeCreate, EmployeeRead, EmployeeUpdate


router = APIRouter(dependencies=[Depends(check_admin_or_super_admin)])


@router.get(
    "/{employee_id}",
    response_model=EmployeeRead,
    summary="Obtener empleado por ID",
    description="""
Retorna los datos completos de un empleado específico.

**Campos retornados:**
- Datos personales: nombre, apellido, DNI, RUC, género, fecha de nacimiento
- Contacto: teléfono, email, dirección
- Laboral: cargo (`position`), estado activo (`isActive`)
- Auditoría: `createdAt`, `updatedAt`

**Cargos posibles** (`position`):
`Docente` · `Auxiliar` · `Secretaria` · `Director` · `Subdirector` · `Psicologo` · `Promotor` · `Administrativo` · `Otro`
""",
    response_description="Datos completos del empleado",
    responses={
        404: {
            "description": "Empleado no encontrado",
            "content": {
                "application/json": {
                    "example": {"detail": "Employee not found"}
                }
            },
        },
        401: {"description": "No autenticado — token JWT ausente o inválido"},
        403: {"description": "Sin permisos — requiere rol `ADMIN` o `SUPER_ADMIN`"},
    },
)
def get_employee(
    employee_id: int, db: Session = Depends(get_db)
) -> EmployeeRead:
    employee = employee_service.get_employee(db, employee_id)
    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return employee


@router.get(
    "",
    response_model=list[EmployeeRead],
    summary="Listar empleados",
    description="""
Retorna una lista paginada de todos los empleados registrados.

**Paginación:**
- `skip` — Registros a omitir (default: `0`)
- `limit` — Máximo de registros a retornar (default: `100`)

**Ejemplo:** `GET /employees?skip=0&limit=20` retorna los primeros 20 empleados.
    """,
    response_description="Lista de empleados",
    responses={
        401: {"description": "No autenticado — token JWT ausente o inválido"},
        403: {"description": "Sin permisos — requiere rol `ADMIN` o `SUPER_ADMIN`"},
    },
)
def get_employees(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[EmployeeRead]:
    employees = employee_service.get_employees(db, skip=skip, limit=limit)
    return list(employees)


@router.post(
    "",
    response_model=EmployeeRead,
    status_code=status.HTTP_201_CREATED,
    summary="Crear empleado",
    description="""
Registra un nuevo empleado en el sistema.

**Campos obligatorios:**
`firstName`, `lastName`, `dni`, `gender`, `phoneNumber`, `position`

**Campos opcionales:**
`ruc`, `birthDate`, `address`, `email`, `isActive` (default: `true`)

**Validaciones de unicidad (servicio):**
- `dni` — No puede repetirse entre empleados
- `ruc` — No puede repetirse si se proporciona
- `email` — No puede repetirse si se proporciona

**Validaciones de schema:**
- `firstName` / `lastName` — Solo letras y espacios, 2-50 caracteres
- `dni` — Solo dígitos, 8-15 caracteres
- `ruc` — Solo dígitos, exactamente 11 caracteres
- `phoneNumber` — Formato `+?\\d{6,14}`
- `birthDate` — Debe ser mayor de 18 años

**Cargos posibles** (`position`):
`Docente` · `Auxiliar` · `Secretaria` · `Director` · `Subdirector` · `Psicologo` · `Promotor` · `Administrativo` · `Otro`

**Género** (`gender`): `Masculino` · `Femenino`
    """,
    response_description="Empleado creado exitosamente",
    responses={
        400: {
            "description": "Error de validación de negocio",
            "content": {
                "application/json": {
                    "examples": {
                        "dni_duplicado": {
                            "summary": "DNI duplicado",
                            "value": {"detail": "Ya existe un empleado con el mismo DNI"},
                        },
                        "ruc_duplicado": {
                            "summary": "RUC duplicado",
                            "value": {"detail": "Ya existe un empleado con el mismo RUC"},
                        },
                        "email_duplicado": {
                            "summary": "Email duplicado",
                            "value": {"detail": "Ya existe un empleado con el mismo Email"},
                        },
                    }
                }
            },
        },
        422: {"description": "Error de validación de schema — campos con formato inválido"},
        401: {"description": "No autenticado — token JWT ausente o inválido"},
        403: {"description": "Sin permisos — requiere rol `ADMIN` o `SUPER_ADMIN`"},
    },
)
def create_employee(
    employee_in: EmployeeCreate, db: Session = Depends(get_db)
) -> EmployeeRead:
    employee = employee_service.create_employee(db, employee_in)
    return employee


@router.put(
    "/{employee_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Actualizar empleado",
    description="""
Actualiza parcialmente los datos de un empleado existente.
Solo se modifican los campos enviados en el body (partial update).

**Validaciones de unicidad:**
- `dni`, `ruc`, `email` — No pueden duplicarse con otros empleados

**Reglas de negocio:**
- **No se puede desactivar** si el empleado es Director o Subdirector de un colegio
- **Coherencia de cargo/rol:** Si el empleado tiene un usuario asociado:
  - Rol `SUPER_ADMIN` → cargo debe ser `Administrativo`
  - Rol `ADMIN` → cargo debe ser `Promotor`, `Subdirector`, `Director` o `Secretaria`
    """,
    response_description="Empleado actualizado — sin contenido en la respuesta",
    responses={
        400: {
            "description": "Error de validación de negocio",
            "content": {
                "application/json": {
                    "examples": {
                        "dni_duplicado": {
                            "summary": "DNI duplicado",
                            "value": {"detail": "Ya existe otro empleado con el mismo DNI"},
                        },
                        "desactivar_director": {
                            "summary": "No se puede desactivar Director",
                            "value": {
                                "detail": "No se puede desactivar al empleado porque actualmente es Director de un colegio."
                            },
                        },
                        "desactivar_subdirector": {
                            "summary": "No se puede desactivar Subdirector",
                            "value": {
                                "detail": "No se puede desactivar al empleado porque actualmente es Subdirector de un colegio."
                            },
                        },
                        "incoherencia_super_admin": {
                            "summary": "Cargo incoherente con SUPER_ADMIN",
                            "value": {
                                "detail": "No se puede cambiar la posición: el empleado tiene un usuario SUPER_ADMIN y requiere ser ADMINISTRATIVO."
                            },
                        },
                        "incoherencia_admin": {
                            "summary": "Cargo incoherente con ADMIN",
                            "value": {
                                "detail": "No se puede cambiar la posición: la nueva posición no tiene permisos para el rol ADMIN de su usuario asociado."
                            },
                        },
                    }
                }
            },
        },
        404: {
            "description": "Empleado no encontrado",
            "content": {
                "application/json": {
                    "example": {"detail": "Employee not found"}
                }
            },
        },
        422: {"description": "Error de validación de schema — campos con formato inválido"},
        401: {"description": "No autenticado — token JWT ausente o inválido"},
        403: {"description": "Sin permisos — requiere rol `ADMIN` o `SUPER_ADMIN`"},
    },
)
def update_employee(
    employee_id: int, employee_in: EmployeeUpdate, db: Session = Depends(get_db)
) -> Response:
    employee = employee_service.get_employee(db, employee_id)
    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    employee_service.update_employee(db, employee, employee_in)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete(
    "/{employee_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar empleado",
    description="""
Elimina permanentemente un empleado del sistema.

**Reglas de negocio:**
- **No se puede eliminar** si el empleado es Director o Subdirector de un colegio
- **No se puede eliminar** si tiene registros relacionados (usuario, pagos, etc.)

> ⚠️ Esta operación es **irreversible**. Considere desactivar (`isActive: false`) en lugar de eliminar.
    """,
    response_description="Empleado eliminado — sin contenido en la respuesta",
    responses={
        400: {
            "description": "No se puede eliminar por restricciones de negocio",
            "content": {
                "application/json": {
                    "examples": {
                        "cargos_directivos": {
                            "summary": "Tiene cargos directivos",
                            "value": {
                                "detail": "No se puede eliminar al empleado porque tiene cargos directivos asignados."
                            },
                        },
                        "registros_relacionados": {
                            "summary": "Tiene registros relacionados",
                            "value": {
                                "detail": "No se puede eliminar el empleado porque tiene registros relacionados."
                            },
                        },
                    }
                }
            },
        },
        404: {
            "description": "Empleado no encontrado",
            "content": {
                "application/json": {
                    "example": {"detail": "Employee not found"}
                }
            },
        },
        401: {"description": "No autenticado — token JWT ausente o inválido"},
        403: {"description": "Sin permisos — requiere rol `ADMIN` o `SUPER_ADMIN`"},
    },
)
def delete_employee(
    employee_id: int, db: Session = Depends(get_db)
) -> Response:
    employee = employee_service.get_employee(db, employee_id)
    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")

    try:
        employee_service.delete_employee(db, employee)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se puede eliminar el empleado porque tiene registros relacionados.")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
