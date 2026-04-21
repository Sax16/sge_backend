from collections.abc import Sequence
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.models.receipt import Receipt
from app.schemas.receipt import ReceiptCreate, ReceiptUpdate
from app.crud import receipt_crud


def get_receipt(db: Session, receipt_id: int | str) -> Receipt | None:
    return receipt_crud.get_receipt(db, receipt_id)


def get_receipts(db: Session, skip: int = 0, limit: int = 100) -> Sequence[Receipt]:
    return receipt_crud.get_receipts(db, skip=skip, limit=limit)


def create_receipt(db: Session, receipt: ReceiptCreate) -> Receipt:
    return receipt_crud.create_receipt(db, receipt)


def update_receipt(db: Session, receipt: Receipt, receipt_in: ReceiptUpdate) -> Receipt:
    return receipt_crud.update_receipt(db, receipt, receipt_in)


def delete_receipt(db: Session, receipt: Receipt) -> None:
    receipt_crud.delete_receipt(db, receipt)
