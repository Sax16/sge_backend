from fastapi import HTTPException, status
from collections.abc import Sequence

from sqlalchemy.orm import Session

from app.core.enums import UserRole, EmployeePosition
from app.core.security import get_password_hash
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.services import employee_service
from app.crud import user_crud


def get_user(db: Session, user_id: int) -> User | None:
    return user_crud.get_user(db, user_id)


def get_users(db: Session, skip: int = 0, limit: int = 100) -> Sequence[User]:
    return user_crud.get_users(db, skip=skip, limit=limit)


def get_user_by_username(db: Session, username: str) -> User | None:
    return user_crud.get_user_by_username(db, username)


def create_user(db: Session, user: UserCreate) -> User:
    # Validate that the username does not exist
    existing_user = user_crud.get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    # Validate that the employee exists
    existing_employee = employee_service.get_employee(db, user.employee_id)
    if existing_employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")

    # Validate that the employee is active
    if not existing_employee.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Employee is not active")

    # Validate that the employee is not already assigned to a user
    existing_user = user_crud.get_user_by_employee_id(db, user.employee_id)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Employee already assigned to a user")

    # Validate Role Coherence
    allowed_admin_positions = [
        EmployeePosition.PROMOTOR, 
        EmployeePosition.SUBDIRECTOR, 
        EmployeePosition.DIRECTOR, 
        EmployeePosition.SECRETARIA
    ]
    if user.role == UserRole.SUPER_ADMIN and existing_employee.position != EmployeePosition.ADMINISTRATIVO:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Solo los empleados con posición " + EmployeePosition.ADMINISTRATIVO.value + " pueden ser " + UserRole.SUPER_ADMIN.value + "."
        )
    elif user.role == UserRole.ADMIN and existing_employee.position not in allowed_admin_positions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="El empleado no tiene una posición permitida para ser " + UserRole.ADMIN.value + "."
        )

    # Hash the password
    user.password = get_password_hash(user.password)
    
    return user_crud.create_user(db, user)


def update_user(db: Session, user: User, user_in: UserUpdate) -> User:
    # Validate that if the username exists, it's the same user
    existing_user = user_crud.get_user_by_username(db, user_in.username)
    if existing_user and existing_user.id != user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    # Validate Zombie Reactivation
    if user_in.is_active is True and not user.is_active:
        if not user.employee.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="No se puede activar el usuario porque el empleado asociado está inactivo."
            )

    # Validate Role Coherence
    new_role = user_in.role if user_in.role else user.role
    employee = user.employee

    allowed_admin_positions = [
        EmployeePosition.PROMOTOR, 
        EmployeePosition.SUBDIRECTOR, 
        EmployeePosition.DIRECTOR, 
        EmployeePosition.SECRETARIA,
        EmployeePosition.ADMINISTRATIVO
    ]
    if new_role == UserRole.SUPER_ADMIN and employee.position != EmployeePosition.ADMINISTRATIVO:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Solo los empleados con posición " + EmployeePosition.ADMINISTRATIVO.value + " pueden ser " + UserRole.SUPER_ADMIN.value + "."
        )
    elif new_role == UserRole.ADMIN and employee.position not in allowed_admin_positions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="El empleado no tiene una posición permitida para ser " + UserRole.ADMIN.value + "."
        )

    # Validate Super Admin Lockout
    if user.role == UserRole.SUPER_ADMIN and (user_in.is_active is False or (user_in.role and user_in.role != UserRole.SUPER_ADMIN)):
        super_admins_count = db.query(User).filter(User.role == UserRole.SUPER_ADMIN, User.is_active == True).count()
        if super_admins_count <= 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se puede modificar o desactivar al último " + UserRole.SUPER_ADMIN.value + " activo del sistema."
            )

    # Hash the password if it exists
    if user_in.password:
        user_in.password = get_password_hash(user_in.password)
    
    return user_crud.update_user(db, user, user_in)


def delete_user(db: Session, user: User) -> None:
    # Validate Super Admin Lockout
    if user.role == UserRole.SUPER_ADMIN:
        super_admins_count = db.query(User).filter(User.role == UserRole.SUPER_ADMIN, User.is_active == True).count()
        if super_admins_count <= 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se puede eliminar al último " + UserRole.SUPER_ADMIN.value + " activo del sistema."
            )

    # Verify if user has associated operations before deleting
    if user.expenses or user.enrollments or user.charges or user.receipts or user.employee_payments:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="No se puede eliminar el usuario porque tiene transacciones financieras u operativas asociadas. Proceda a desactivarlo."
        )
    user_crud.delete_user(db, user)