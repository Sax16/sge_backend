from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.services import payment_employee_service
from app.dependencies import get_db, check_admin_or_super_admin
from app.schemas.payment_employee import PaymentEmployeeCreate, PaymentEmployeeRead, PaymentEmployeeUpdate


router = APIRouter(dependencies=[Depends(check_admin_or_super_admin)])


@router.get("/{payment_employee_id}", response_model=PaymentEmployeeRead, description="Get a payment_employee by ID")
def get_payment_employee(
    payment_employee_id: int, db: Session = Depends(get_db)
) -> PaymentEmployeeRead:
    payment_employee = payment_employee_service.get_payment_employee(db, payment_employee_id)
    if payment_employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PaymentEmployee not found")
    return payment_employee


@router.get("", response_model=list[PaymentEmployeeRead], description="List all payment_employees")
def get_payment_employees(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[PaymentEmployeeRead]:
    payment_employees = payment_employee_service.get_payment_employees(db, skip=skip, limit=limit)
    return list(payment_employees)


@router.post(
    "", response_model=PaymentEmployeeRead, status_code=status.HTTP_201_CREATED,
    description="Create a new payment_employee"
)
def create_payment_employee(
    payment_employee_in: PaymentEmployeeCreate, db: Session = Depends(get_db)
) -> PaymentEmployeeRead:
    payment_employee = payment_employee_service.create_payment_employee(db, payment_employee_in)
    return payment_employee


@router.put(
    "/{payment_employee_id}", status_code=status.HTTP_204_NO_CONTENT,
    description="Update a payment_employee by ID"
)
def update_payment_employee(
    payment_employee_id: int, payment_employee_in: PaymentEmployeeUpdate, db: Session = Depends(get_db)
) -> Response:
    payment_employee = payment_employee_service.get_payment_employee(db, payment_employee_id)
    if payment_employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PaymentEmployee not found")
    payment_employee_service.update_payment_employee(db, payment_employee, payment_employee_in)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/{payment_employee_id}", status_code=status.HTTP_204_NO_CONTENT, description="Delete a payment_employee by ID")
def delete_payment_employee(
    payment_employee_id: int, db: Session = Depends(get_db)
) -> Response:
    payment_employee = payment_employee_service.get_payment_employee(db, payment_employee_id)
    if payment_employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PaymentEmployee not found")

    try:
        payment_employee_service.delete_payment_employee(db, payment_employee)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se puede eliminar porque tiene registros relacionados.")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
