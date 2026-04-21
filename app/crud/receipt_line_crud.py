from collections.abc import Sequence

from sqlalchemy.orm import Session

from app.models.receipt_line import ReceiptLine
from app.schemas.receipt_line import ReceiptLineCreate, ReceiptLineUpdate


def create_receipt_line(db: Session, receipt_line_in: ReceiptLineCreate) -> ReceiptLine:
    receipt_line = ReceiptLine(**receipt_line_in.model_dump())
    db.add(receipt_line)
    db.commit()
    db.refresh(receipt_line)
    return receipt_line


def get_receipt_line(db: Session, receipt_line_id: int | str) -> ReceiptLine | None:
    return db.query(ReceiptLine).filter(ReceiptLine.id == receipt_line_id).first()


def get_receipt_lines(db: Session, skip: int = 0, limit: int = 100) -> Sequence[ReceiptLine]:
    return db.query(ReceiptLine).order_by(ReceiptLine.id).offset(skip).limit(limit).all()


def update_receipt_line(
    db: Session, receipt_line: ReceiptLine, receipt_line_in: ReceiptLineUpdate
) -> ReceiptLine:
    data = receipt_line_in.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(receipt_line, key, value)
    db.add(receipt_line)
    db.commit()
    db.refresh(receipt_line)
    return receipt_line


def delete_receipt_line(db: Session, receipt_line: ReceiptLine) -> None:
    db.delete(receipt_line)
    db.commit()
