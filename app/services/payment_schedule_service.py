from collections.abc import Sequence
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.models.payment_schedule import PaymentSchedule
from app.schemas.payment_schedule import PaymentScheduleCreate, PaymentScheduleUpdate
from app.crud import payment_schedule_crud


def get_payment_schedule(db: Session, payment_schedule_id: int | str) -> PaymentSchedule | None:
    return payment_schedule_crud.get_payment_schedule(db, payment_schedule_id)


def get_payment_schedules(db: Session, skip: int = 0, limit: int = 100) -> Sequence[PaymentSchedule]:
    return payment_schedule_crud.get_payment_schedules(db, skip=skip, limit=limit)


def create_payment_schedule(db: Session, payment_schedule: PaymentScheduleCreate) -> PaymentSchedule:
    return payment_schedule_crud.create_payment_schedule(db, payment_schedule)


def update_payment_schedule(db: Session, payment_schedule: PaymentSchedule, payment_schedule_in: PaymentScheduleUpdate) -> PaymentSchedule:
    return payment_schedule_crud.update_payment_schedule(db, payment_schedule, payment_schedule_in)


def delete_payment_schedule(db: Session, payment_schedule: PaymentSchedule) -> None:
    payment_schedule_crud.delete_payment_schedule(db, payment_schedule)
