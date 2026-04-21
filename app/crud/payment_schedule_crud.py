from collections.abc import Sequence

from sqlalchemy.orm import Session

from app.models.payment_schedule import PaymentSchedule
from app.schemas.payment_schedule import PaymentScheduleCreate, PaymentScheduleUpdate


def create_payment_schedule(db: Session, payment_schedule_in: PaymentScheduleCreate) -> PaymentSchedule:
    payment_schedule = PaymentSchedule(**payment_schedule_in.model_dump())
    db.add(payment_schedule)
    db.commit()
    db.refresh(payment_schedule)
    return payment_schedule


def get_payment_schedule(db: Session, payment_schedule_id: int | str) -> PaymentSchedule | None:
    return db.query(PaymentSchedule).filter(PaymentSchedule.id == payment_schedule_id).first()


def get_payment_schedules(db: Session, skip: int = 0, limit: int = 100) -> Sequence[PaymentSchedule]:
    return db.query(PaymentSchedule).order_by(PaymentSchedule.id).offset(skip).limit(limit).all()


def update_payment_schedule(
    db: Session, payment_schedule: PaymentSchedule, payment_schedule_in: PaymentScheduleUpdate
) -> PaymentSchedule:
    data = payment_schedule_in.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(payment_schedule, key, value)
    db.add(payment_schedule)
    db.commit()
    db.refresh(payment_schedule)
    return payment_schedule


def delete_payment_schedule(db: Session, payment_schedule: PaymentSchedule) -> None:
    db.delete(payment_schedule)
    db.commit()
