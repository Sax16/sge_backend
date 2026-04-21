from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.services import charge_catalog_amount_service
from app.dependencies import get_db, check_admin_or_super_admin
from app.schemas.charge_catalog_amount import ChargeCatalogAmountCreate, ChargeCatalogAmountRead, ChargeCatalogAmountUpdate


router = APIRouter(dependencies=[Depends(check_admin_or_super_admin)])


@router.get("/{charge_catalog_amount_id}", response_model=ChargeCatalogAmountRead, description="Get a charge_catalog_amount by ID")
def get_charge_catalog_amount(
    charge_catalog_amount_id: int, db: Session = Depends(get_db)
) -> ChargeCatalogAmountRead:
    charge_catalog_amount = charge_catalog_amount_service.get_charge_catalog_amount(db, charge_catalog_amount_id)
    if charge_catalog_amount is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ChargeCatalogAmount not found")
    return charge_catalog_amount


@router.get("", response_model=list[ChargeCatalogAmountRead], description="List all charge_catalog_amounts")
def get_charge_catalog_amounts(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[ChargeCatalogAmountRead]:
    charge_catalog_amounts = charge_catalog_amount_service.get_charge_catalog_amounts(db, skip=skip, limit=limit)
    return list(charge_catalog_amounts)


@router.post(
    "", response_model=ChargeCatalogAmountRead, status_code=status.HTTP_201_CREATED,
    description="Create a new charge_catalog_amount"
)
def create_charge_catalog_amount(
    charge_catalog_amount_in: ChargeCatalogAmountCreate, db: Session = Depends(get_db)
) -> ChargeCatalogAmountRead:
    charge_catalog_amount = charge_catalog_amount_service.create_charge_catalog_amount(db, charge_catalog_amount_in)
    return charge_catalog_amount


@router.put(
    "/{charge_catalog_amount_id}", status_code=status.HTTP_204_NO_CONTENT,
    description="Update a charge_catalog_amount by ID"
)
def update_charge_catalog_amount(
    charge_catalog_amount_id: int, charge_catalog_amount_in: ChargeCatalogAmountUpdate, db: Session = Depends(get_db)
) -> Response:
    charge_catalog_amount = charge_catalog_amount_service.get_charge_catalog_amount(db, charge_catalog_amount_id)
    if charge_catalog_amount is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ChargeCatalogAmount not found")
    charge_catalog_amount_service.update_charge_catalog_amount(db, charge_catalog_amount, charge_catalog_amount_in)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/{charge_catalog_amount_id}", status_code=status.HTTP_204_NO_CONTENT, description="Delete a charge_catalog_amount by ID")
def delete_charge_catalog_amount(
    charge_catalog_amount_id: int, db: Session = Depends(get_db)
) -> Response:
    charge_catalog_amount = charge_catalog_amount_service.get_charge_catalog_amount(db, charge_catalog_amount_id)
    if charge_catalog_amount is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ChargeCatalogAmount not found")

    try:
        charge_catalog_amount_service.delete_charge_catalog_amount(db, charge_catalog_amount)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se puede eliminar porque tiene registros relacionados.")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
