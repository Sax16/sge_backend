from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from app.services import user_service
from app.dependencies import get_db, check_super_admin
from app.schemas.user import UserCreate, UserRead, UserUpdate


router = APIRouter(dependencies=[Depends(check_super_admin)])


@router.get(
    "/{user_id}",
    response_model=UserRead,
    summary="Obtener usuario por ID",
    description="""
Retorna los datos de un usuario específico incluyendo el nombre
del empleado asociado.

**Requiere:** Rol `SUPER_ADMIN`.
""",
    responses={
        200: {"description": "Usuario encontrado"},
        404: {"description": "Usuario no encontrado"},
    },
)
def get_user(
    user_id: int, db: Session = Depends(get_db)
) -> UserRead:
    user = user_service.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.get(
    "",
    response_model=list[UserRead],
    summary="Listar usuarios",
    description="""
Retorna la lista paginada de todos los usuarios del sistema.

**Requiere:** Rol `SUPER_ADMIN`.

**Paginación:**
- `skip`: Número de registros a omitir (por defecto `0`).
- `limit`: Máximo de registros a retornar (por defecto `100`).
""",
    responses={
        200: {"description": "Lista de usuarios retornada exitosamente"},
    },
)
def get_users(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[UserRead]:
    users = user_service.get_users(db, skip=skip, limit=limit) 
    return list(users)


@router.post(
    "",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Crear usuario",
    description="""
Crea un nuevo usuario del sistema vinculado a un empleado existente.

**Requiere:** Rol `SUPER_ADMIN`.

**Reglas de negocio:**
- El `username` debe ser único (3-25 caracteres alfanuméricos o `_`).
- El `password` debe tener entre 4 y 15 caracteres (se hashea antes de almacenar).
- El empleado asociado debe existir y estar **activo**.
- Un empleado solo puede tener **un usuario** asignado.
- **Coherencia rol-posición:**
    - `SUPER_ADMIN` → solo empleados con posición `ADMINISTRATIVO`.
    - `ADMIN` → solo posiciones `PROMOTOR`, `SUBDIRECTOR`, `DIRECTOR`, `SECRETARIA`.
""",
    responses={
        201: {"description": "Usuario creado exitosamente"},
        400: {
            "description": "Regla de negocio violada",
            "content": {
                "application/json": {
                    "examples": {
                        "username_duplicado": {
                            "summary": "Username ya existe",
                            "value": {"detail": "Username already exists"},
                        },
                        "empleado_inactivo": {
                            "summary": "Empleado inactivo",
                            "value": {"detail": "Employee is not active"},
                        },
                        "empleado_asignado": {
                            "summary": "Empleado ya tiene usuario",
                            "value": {"detail": "Employee already assigned to a user"},
                        },
                        "coherencia_super_admin": {
                            "summary": "Posición incompatible con SUPER_ADMIN",
                            "value": {"detail": "Solo los empleados con posición ADMINISTRATIVO pueden ser SUPER_ADMIN."},
                        },
                        "coherencia_admin": {
                            "summary": "Posición incompatible con ADMIN",
                            "value": {"detail": "El empleado no tiene una posición permitida para ser ADMIN."},
                        },
                    }
                }
            },
        },
        404: {"description": "Empleado no encontrado"},
    },
)
def create_user(
    user_in: UserCreate, db: Session = Depends(get_db)
) -> UserRead:
    user = user_service.create_user(db, user_in)
    return user


@router.put(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Actualizar usuario",
    description="""
Actualiza los datos de un usuario existente. Solo se modifican
los campos enviados (actualización parcial).

**Requiere:** Rol `SUPER_ADMIN`.

**Reglas de negocio:**
- Si se cambia el `username`, el nuevo debe ser único.
- Si se cambia el `password`, se hashea antes de almacenar.
- **Anti-zombie:** No se puede reactivar un usuario cuyo empleado
    asociado está inactivo.
- **Coherencia rol-posición:** Se aplican las mismas reglas que en
    la creación.
- **Protección Super Admin:** No se puede desactivar ni cambiar el
    rol del último `SUPER_ADMIN` activo del sistema.
""",
    responses={
        204: {"description": "Usuario actualizado exitosamente"},
        400: {
            "description": "Regla de negocio violada",
            "content": {
                "application/json": {
                    "examples": {
                        "username_duplicado": {
                            "summary": "Username ya existe",
                            "value": {"detail": "Username already exists"},
                        },
                        "zombie": {
                            "summary": "Reactivación zombie",
                            "value": {"detail": "No se puede activar el usuario porque el empleado asociado está inactivo."},
                        },
                        "ultimo_super_admin": {
                            "summary": "Último SUPER_ADMIN protegido",
                            "value": {"detail": "No se puede modificar o desactivar al último SUPER_ADMIN activo del sistema."},
                        },
                    }
                }
            },
        },
        404: {"description": "Usuario no encontrado"},
    },
)
def update_user(
    user_id: int, user_in: UserUpdate, db: Session = Depends(get_db)
) -> Response:
    user = user_service.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user_service.update_user(db, user, user_in)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar usuario",
    description="""
Elimina permanentemente un usuario del sistema.

**Requiere:** Rol `SUPER_ADMIN`.

**Regla de negocio:**
- No se puede eliminar un usuario que tenga transacciones financieras
    u operativas asociadas (gastos, matrículas, cobros, recibos o pagos
    a empleados). En ese caso, se debe **desactivar** en lugar de eliminar.
""",
    responses={
        204: {"description": "Usuario eliminado exitosamente"},
        400: {
            "description": "Usuario con operaciones asociadas",
            "content": {
                "application/json": {
                    "examples": {
                        "tiene_operaciones": {
                            "summary": "Tiene transacciones asociadas",
                            "value": {"detail": "No se puede eliminar el usuario porque tiene transacciones financieras u operativas asociadas. Proceda a desactivarlo."},
                        },
                    }
                }
            },
        },
        404: {"description": "Usuario no encontrado"},
    },
)
def delete_user(
    user_id: int, db: Session = Depends(get_db)
) -> Response:
    user = user_service.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user_service.delete_user(db, user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
