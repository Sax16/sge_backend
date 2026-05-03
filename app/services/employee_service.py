from collections.abc import Sequence
from datetime import date

from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.core.enums import UserRole, EmployeePosition
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate
from app.crud import employee_crud


def _validate_minimum_age(birth_date: date | None, min_age: int = 18) -> None:
    """Regla de negocio: el empleado debe ser mayor de `min_age` años."""
    if birth_date is None:
        return
    today = date.today()
    age = today.year - birth_date.year - (
        (today.month, today.day) < (birth_date.month, birth_date.day)
    )
    if age < min_age:
        raise HTTPException(
            status_code=422,
            detail=f"El empleado debe ser mayor de {min_age} años"
        )


def get_employee(db: Session, employee_id: int) -> Employee | None:
    return employee_crud.get_employee(db, employee_id)


def get_employees(db: Session, skip: int = 0, limit: int = 100) -> Sequence[Employee]:
    return employee_crud.get_employees(db, skip=skip, limit=limit)


def create_employee(db: Session, employee: EmployeeCreate) -> Employee:
    # 1. Regla de negocio: edad mínima
    if employee.birth_date is not None:
        _validate_minimum_age(employee.birth_date)

    # 2. Verificar si el DNI ya existe
    existing_employee = employee_crud.get_employee_by_dni(db, employee.dni)
    if existing_employee:
        raise HTTPException(status_code=400, detail="Ya existe un empleado con el mismo DNI")

    # 2. Verificar si el RUC ya existe
    if employee.ruc:
        existing_by_ruc = employee_crud.get_employee_by_ruc(db, employee.ruc)
        if existing_by_ruc:
            raise HTTPException(status_code=400, detail="Ya existe un empleado con el mismo RUC")

    # 3. Verificar si el Email ya existe
    if employee.email:
        existing_by_email = employee_crud.get_employee_by_email(db, employee.email)
        if existing_by_email:
            raise HTTPException(status_code=400, detail="Ya existe un empleado con el mismo Email")

    return employee_crud.create_employee(db, employee)


def update_employee(db: Session, employee: Employee, employee_in: EmployeeUpdate) -> Employee:
    # 1. Regla de negocio: edad mínima
    if employee_in.birth_date is not None:
        _validate_minimum_age(employee_in.birth_date)

    # 2. Verificar si el DNI ya existe
    if employee_in.dni is not None and employee_in.dni != employee.dni:
        existing_employee = employee_crud.get_employee_by_dni(db, employee_in.dni)
        if existing_employee:
            raise HTTPException(status_code=400, detail="Ya existe otro empleado con el mismo DNI")

    # 2. Verificar si el RUC ya existe
    if employee_in.ruc is not None and employee_in.ruc != employee.ruc:
        existing_by_ruc = employee_crud.get_employee_by_ruc(db, employee_in.ruc)
        if existing_by_ruc:
            raise HTTPException(status_code=400, detail="Ya existe otro empleado con el mismo RUC")

    # 3. Verificar si el Email ya existe
    if employee_in.email is not None and employee_in.email != employee.email:
        existing_by_email = employee_crud.get_employee_by_email(db, employee_in.email)
        if existing_by_email:
            raise HTTPException(status_code=400, detail="Ya existe otro empleado con el mismo Email")

    # 4. Regla de negocio: No desactivar si tiene cargos críticos activos
    if employee_in.is_active is False and employee.is_active is True:
        if employee.school_as_headmaster:
            raise HTTPException(
                status_code=400, 
                detail="No se puede desactivar al empleado porque actualmente es Director de un colegio."
            )
        if employee.school_as_deputy_director:
            raise HTTPException(
                status_code=400, 
                detail="No se puede desactivar al empleado porque actualmente es Subdirector de un colegio."
            )

    # 4.1. Regla de negocio: El director o subdirector no puede cambiar de posición si tiene cargos activos en schools.
    if employee_in.position is not None and employee.position in [EmployeePosition.DIRECTOR, EmployeePosition.SUBDIRECTOR] and employee.school_as_headmaster:
        raise HTTPException(
            status_code=400, 
            detail="No se puede cambiar la posición del empleado porque actualmente es Director o subdirector del colegio."
        )
    
    # 5. Regla de negocio: Coherencia de roles al cambiar de posición
    if employee_in.position is not None and employee_in.position != employee.position:
        if employee.user:
            new_position = employee_in.position
            allowed_admin_positions = [
                EmployeePosition.PROMOTOR, 
                EmployeePosition.SUBDIRECTOR, 
                EmployeePosition.DIRECTOR, 
                EmployeePosition.SECRETARIA
            ]
            if employee.user.role == UserRole.SUPER_ADMIN and new_position != EmployeePosition.ADMINISTRATIVO:
                raise HTTPException(
                    status_code=400, 
                    detail="No se puede cambiar la posición: el empleado tiene un usuario " + UserRole.SUPER_ADMIN.value + " y requiere ser " + EmployeePosition.ADMINISTRATIVO.value + "."
                )
            elif employee.user.role == UserRole.ADMIN and new_position not in allowed_admin_positions:
                raise HTTPException(
                    status_code=400, 
                    detail="No se puede cambiar la posición: la nueva posición no tiene permisos para el rol " + UserRole.ADMIN.value + " de su usuario asociado."
                )

    return employee_crud.update_employee(db, employee, employee_in)


def delete_employee(db: Session, employee: Employee) -> None:
    # Validar que no sea director ni subdirector antes de eliminar
    if employee.school_as_headmaster or employee.school_as_deputy_director:
        raise HTTPException(
            status_code=400, 
            detail="No se puede eliminar al empleado porque tiene cargos directivos asignados."
        )
    employee_crud.delete_employee(db, employee)
