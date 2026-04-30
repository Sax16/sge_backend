from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.school import School
from app.schemas.school import SchoolCreate, SchoolUpdate
from app.crud import school_crud, employee_crud
from app.core.enums import EmployeePosition


def get_school(db: Session, school_id: int) -> School | None:
    return school_crud.get_school(db, school_id)


def _validate_employees(db: Session, headmaster_id: int | None, deputy_director_id: int | None):
    # Verify headmaster exists and has role 'DIRECTOR'
    if headmaster_id is not None:
        headmaster = employee_crud.get_employee(db, headmaster_id)
        if not headmaster:
            raise HTTPException(status_code=404, detail="El empleado asignado como director no existe")
        if headmaster.position != EmployeePosition.DIRECTOR:
            raise HTTPException(status_code=400, detail="El empleado asignado como director no tiene el rol de director")
    
    # Verify deputy director exists if provided and has role 'SUBDIRECTOR'
    if deputy_director_id is not None:
        deputy = employee_crud.get_employee(db, deputy_director_id)
        if not deputy:
            raise HTTPException(status_code=404, detail="El empleado asignado como subdirector no existe")
        if deputy.position != EmployeePosition.SUBDIRECTOR:
            raise HTTPException(status_code=400, detail="El empleado asignado como subdirector no tiene el rol de subdirector")


def create_school(db: Session, school_in: SchoolCreate) -> School:
    # Verify if ANY school already exists (since only one is allowed)
    existing_school = db.query(School).first()
    if existing_school:
        raise HTTPException(status_code=400, detail="Ya existe un colegio registrado. Solo se permite un registro de colegio.")

    # Validate employee associations
    _validate_employees(db, school_in.headmaster_id, school_in.deputy_director_id)

    return school_crud.create_school(db, school_in)


def update_school(db: Session, school: School, school_in: SchoolUpdate) -> School:
    # Check that they are not making the headmaster and deputy director the same person
    new_headmaster_id = school_in.headmaster_id if school_in.headmaster_id is not None else school.headmaster_id
    new_deputy_id = school_in.deputy_director_id if school_in.deputy_director_id is not None else school.deputy_director_id
    
    if new_deputy_id is not None and new_headmaster_id == new_deputy_id:
        raise HTTPException(status_code=400, detail="El director y el subdirector no pueden ser la misma persona.")

    # Validate employee associations
    _validate_employees(db, school_in.headmaster_id, school_in.deputy_director_id)

    return school_crud.update_school(db, school, school_in)
