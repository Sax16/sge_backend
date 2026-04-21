from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.services import charge_discount_service
from app.dependencies import get_db, check_admin_or_super_admin
from app.schemas.charge_discount import ChargeDiscountCreate, ChargeDiscountRead, ChargeDiscountUpdate


router = APIRouter(dependencies=[Depends(check_admin_or_super_admin)])


@router.get("/{charge_discount_id}", response_model=ChargeDiscountRead, description="Get a charge_discount by ID")
def get_charge_discount(
    charge_discount_id: int, db: Session = Depends(get_db)
) -> ChargeDiscountRead:
    charge_discount = charge_discount_service.get_charge_discount(db, charge_discount_id)
    if charge_discount is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ChargeDiscount not found")
    return charge_discount


@router.get("", response_model=list[ChargeDiscountRead], description="List all charge_discounts")
def get_charge_discounts(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[ChargeDiscountRead]:
    charge_discounts = charge_discount_service.get_charge_discounts(db, skip=skip, limit=limit)
    return list(charge_discounts)


@router.post(
    "", response_model=ChargeDiscountRead, status_code=status.HTTP_201_CREATED,
    description="Create a new charge_discount"
)
def create_charge_discount(
    charge_discount_in: ChargeDiscountCreate, db: Session = Depends(get_db)
) -> ChargeDiscountRead:
    charge_discount = charge_discount_service.create_charge_discount(db, charge_discount_in)
    return charge_discount


@router.put(
    "/{charge_discount_id}", status_code=status.HTTP_204_NO_CONTENT,
    description="Update a charge_discount by ID"
)
def update_charge_discount(
    charge_discount_id: int, charge_discount_in: ChargeDiscountUpdate, db: Session = Depends(get_db)
) -> Response:
    charge_discount = charge_discount_service.get_charge_discount(db, charge_discount_id)
    if charge_discount is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ChargeDiscount not found")
    charge_discount_service.update_charge_discount(db, charge_discount, charge_discount_in)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/{charge_discount_id}", status_code=status.HTTP_204_NO_CONTENT, description="Delete a charge_discount by ID")
def delete_charge_discount(
    charge_discount_id: int, db: Session = Depends(get_db)
) -> Response:
    charge_discount = charge_discount_service.get_charge_discount(db, charge_discount_id)
    if charge_discount is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ChargeDiscount not found")

    try:
        charge_discount_service.delete_charge_discount(db, charge_discount)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se puede eliminar porque tiene registros relacionados.")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
