from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.services import payment_schedule_service
from app.dependencies import get_db, check_admin_or_super_admin
from app.schemas.payment_schedule import PaymentScheduleCreate, PaymentScheduleRead, PaymentScheduleUpdate


router = APIRouter(dependencies=[Depends(check_admin_or_super_admin)])


@router.get("/{payment_schedule_id}", response_model=PaymentScheduleRead, description="Get a payment_schedule by ID")
def get_payment_schedule(
    payment_schedule_id: int, db: Session = Depends(get_db)
) -> PaymentScheduleRead:
    payment_schedule = payment_schedule_service.get_payment_schedule(db, payment_schedule_id)
    if payment_schedule is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PaymentSchedule not found")
    return payment_schedule


@router.get("", response_model=list[PaymentScheduleRead], description="List all payment_schedules")
def get_payment_schedules(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[PaymentScheduleRead]:
    payment_schedules = payment_schedule_service.get_payment_schedules(db, skip=skip, limit=limit)
    return list(payment_schedules)


@router.post(
    "", response_model=PaymentScheduleRead, status_code=status.HTTP_201_CREATED,
    description="Create a new payment_schedule"
)
def create_payment_schedule(
    payment_schedule_in: PaymentScheduleCreate, db: Session = Depends(get_db)
) -> PaymentScheduleRead:
    payment_schedule = payment_schedule_service.create_payment_schedule(db, payment_schedule_in)
    return payment_schedule


@router.put(
    "/{payment_schedule_id}", status_code=status.HTTP_204_NO_CONTENT,
    description="Update a payment_schedule by ID"
)
def update_payment_schedule(
    payment_schedule_id: int, payment_schedule_in: PaymentScheduleUpdate, db: Session = Depends(get_db)
) -> Response:
    payment_schedule = payment_schedule_service.get_payment_schedule(db, payment_schedule_id)
    if payment_schedule is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PaymentSchedule not found")
    payment_schedule_service.update_payment_schedule(db, payment_schedule, payment_schedule_in)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/{payment_schedule_id}", status_code=status.HTTP_204_NO_CONTENT, description="Delete a payment_schedule by ID")
def delete_payment_schedule(
    payment_schedule_id: int, db: Session = Depends(get_db)
) -> Response:
    payment_schedule = payment_schedule_service.get_payment_schedule(db, payment_schedule_id)
    if payment_schedule is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PaymentSchedule not found")

    try:
        payment_schedule_service.delete_payment_schedule(db, payment_schedule)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se puede eliminar porque tiene registros relacionados.")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
