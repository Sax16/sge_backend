from collections.abc import Sequence
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.models.receipt_line import ReceiptLine
from app.schemas.receipt_line import ReceiptLineCreate, ReceiptLineUpdate
from app.crud import receipt_line_crud


def get_receipt_line(db: Session, receipt_line_id: int | str) -> ReceiptLine | None:
    return receipt_line_crud.get_receipt_line(db, receipt_line_id)


def get_receipt_lines(db: Session, skip: int = 0, limit: int = 100) -> Sequence[ReceiptLine]:
    return receipt_line_crud.get_receipt_lines(db, skip=skip, limit=limit)


def create_receipt_line(db: Session, receipt_line: ReceiptLineCreate) -> ReceiptLine:
    return receipt_line_crud.create_receipt_line(db, receipt_line)


def update_receipt_line(db: Session, receipt_line: ReceiptLine, receipt_line_in: ReceiptLineUpdate) -> ReceiptLine:
    return receipt_line_crud.update_receipt_line(db, receipt_line, receipt_line_in)


def delete_receipt_line(db: Session, receipt_line: ReceiptLine) -> None:
    receipt_line_crud.delete_receipt_line(db, receipt_line)
