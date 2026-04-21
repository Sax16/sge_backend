from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.services import receipt_service
from app.dependencies import get_db, check_admin_or_super_admin
from app.schemas.receipt import ReceiptCreate, ReceiptRead, ReceiptUpdate


router = APIRouter(dependencies=[Depends(check_admin_or_super_admin)])


@router.get("/{receipt_id}", response_model=ReceiptRead, description="Get a receipt by ID")
def get_receipt(
    receipt_id: int, db: Session = Depends(get_db)
) -> ReceiptRead:
    receipt = receipt_service.get_receipt(db, receipt_id)
    if receipt is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Receipt not found")
    return receipt


@router.get("", response_model=list[ReceiptRead], description="List all receipts")
def get_receipts(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[ReceiptRead]:
    receipts = receipt_service.get_receipts(db, skip=skip, limit=limit)
    return list(receipts)


@router.post(
    "", response_model=ReceiptRead, status_code=status.HTTP_201_CREATED,
    description="Create a new receipt"
)
def create_receipt(
    receipt_in: ReceiptCreate, db: Session = Depends(get_db)
) -> ReceiptRead:
    receipt = receipt_service.create_receipt(db, receipt_in)
    return receipt


@router.put(
    "/{receipt_id}", status_code=status.HTTP_204_NO_CONTENT,
    description="Update a receipt by ID"
)
def update_receipt(
    receipt_id: int, receipt_in: ReceiptUpdate, db: Session = Depends(get_db)
) -> Response:
    receipt = receipt_service.get_receipt(db, receipt_id)
    if receipt is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Receipt not found")
    receipt_service.update_receipt(db, receipt, receipt_in)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/{receipt_id}", status_code=status.HTTP_204_NO_CONTENT, description="Delete a receipt by ID")
def delete_receipt(
    receipt_id: int, db: Session = Depends(get_db)
) -> Response:
    receipt = receipt_service.get_receipt(db, receipt_id)
    if receipt is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Receipt not found")

    try:
        receipt_service.delete_receipt(db, receipt)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se puede eliminar porque tiene registros relacionados.")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
