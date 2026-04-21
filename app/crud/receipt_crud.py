from collections.abc import Sequence

from sqlalchemy.orm import Session

from app.models.receipt import Receipt
from app.schemas.receipt import ReceiptCreate, ReceiptUpdate


def create_receipt(db: Session, receipt_in: ReceiptCreate) -> Receipt:
    receipt = Receipt(**receipt_in.model_dump())
    db.add(receipt)
    db.commit()
    db.refresh(receipt)
    return receipt


def get_receipt(db: Session, receipt_id: int | str) -> Receipt | None:
    return db.query(Receipt).filter(Receipt.id == receipt_id).first()


def get_receipts(db: Session, skip: int = 0, limit: int = 100) -> Sequence[Receipt]:
    return db.query(Receipt).order_by(Receipt.id).offset(skip).limit(limit).all()


def update_receipt(
    db: Session, receipt: Receipt, receipt_in: ReceiptUpdate
) -> Receipt:
    data = receipt_in.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(receipt, key, value)
    db.add(receipt)
    db.commit()
    db.refresh(receipt)
    return receipt


def delete_receipt(db: Session, receipt: Receipt) -> None:
    db.delete(receipt)
    db.commit()
