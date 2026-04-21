from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.services import discount_service
from app.dependencies import get_db, check_admin_or_super_admin
from app.schemas.discount import DiscountCreate, DiscountRead, DiscountUpdate


router = APIRouter(dependencies=[Depends(check_admin_or_super_admin)])


@router.get("/{discount_id}", response_model=DiscountRead, description="Get a discount by ID")
def get_discount(
    discount_id: int, db: Session = Depends(get_db)
) -> DiscountRead:
    discount = discount_service.get_discount(db, discount_id)
    if discount is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Discount not found")
    return discount


@router.get("", response_model=list[DiscountRead], description="List all discounts")
def get_discounts(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[DiscountRead]:
    discounts = discount_service.get_discounts(db, skip=skip, limit=limit)
    return list(discounts)


@router.post(
    "", response_model=DiscountRead, status_code=status.HTTP_201_CREATED,
    description="Create a new discount"
)
def create_discount(
    discount_in: DiscountCreate, db: Session = Depends(get_db)
) -> DiscountRead:
    discount = discount_service.create_discount(db, discount_in)
    return discount


@router.put(
    "/{discount_id}", status_code=status.HTTP_204_NO_CONTENT,
    description="Update a discount by ID"
)
def update_discount(
    discount_id: int, discount_in: DiscountUpdate, db: Session = Depends(get_db)
) -> Response:
    discount = discount_service.get_discount(db, discount_id)
    if discount is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Discount not found")
    discount_service.update_discount(db, discount, discount_in)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/{discount_id}", status_code=status.HTTP_204_NO_CONTENT, description="Delete a discount by ID")
def delete_discount(
    discount_id: int, db: Session = Depends(get_db)
) -> Response:
    discount = discount_service.get_discount(db, discount_id)
    if discount is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Discount not found")

    try:
        discount_service.delete_discount(db, discount)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se puede eliminar porque tiene registros relacionados.")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
