from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.services import receipt_line_service
from app.dependencies import get_db, check_admin_or_super_admin
from app.schemas.receipt_line import ReceiptLineCreate, ReceiptLineRead, ReceiptLineUpdate


router = APIRouter(dependencies=[Depends(check_admin_or_super_admin)])


@router.get("/{receipt_line_id}", response_model=ReceiptLineRead, description="Get a receipt_line by ID")
def get_receipt_line(
    receipt_line_id: int, db: Session = Depends(get_db)
) -> ReceiptLineRead:
    receipt_line = receipt_line_service.get_receipt_line(db, receipt_line_id)
    if receipt_line is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ReceiptLine not found")
    return receipt_line


@router.get("", response_model=list[ReceiptLineRead], description="List all receipt_lines")
def get_receipt_lines(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[ReceiptLineRead]:
    receipt_lines = receipt_line_service.get_receipt_lines(db, skip=skip, limit=limit)
    return list(receipt_lines)


@router.post(
    "", response_model=ReceiptLineRead, status_code=status.HTTP_201_CREATED,
    description="Create a new receipt_line"
)
def create_receipt_line(
    receipt_line_in: ReceiptLineCreate, db: Session = Depends(get_db)
) -> ReceiptLineRead:
    receipt_line = receipt_line_service.create_receipt_line(db, receipt_line_in)
    return receipt_line


@router.put(
    "/{receipt_line_id}", status_code=status.HTTP_204_NO_CONTENT,
    description="Update a receipt_line by ID"
)
def update_receipt_line(
    receipt_line_id: int, receipt_line_in: ReceiptLineUpdate, db: Session = Depends(get_db)
) -> Response:
    receipt_line = receipt_line_service.get_receipt_line(db, receipt_line_id)
    if receipt_line is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ReceiptLine not found")
    receipt_line_service.update_receipt_line(db, receipt_line, receipt_line_in)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/{receipt_line_id}", status_code=status.HTTP_204_NO_CONTENT, description="Delete a receipt_line by ID")
def delete_receipt_line(
    receipt_line_id: int, db: Session = Depends(get_db)
) -> Response:
    receipt_line = receipt_line_service.get_receipt_line(db, receipt_line_id)
    if receipt_line is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ReceiptLine not found")

    try:
        receipt_line_service.delete_receipt_line(db, receipt_line)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se puede eliminar porque tiene registros relacionados.")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
