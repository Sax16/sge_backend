from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.services import charge_service
from app.dependencies import get_db, check_admin_or_super_admin
from app.schemas.charge import ChargeCreate, ChargeRead, ChargeUpdate


router = APIRouter(dependencies=[Depends(check_admin_or_super_admin)])


@router.get("/{charge_id}", response_model=ChargeRead, description="Get a charge by ID")
def get_charge(
    charge_id: int, db: Session = Depends(get_db)
) -> ChargeRead:
    charge = charge_service.get_charge(db, charge_id)
    if charge is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Charge not found")
    return charge


@router.get("", response_model=list[ChargeRead], description="List all charges")
def get_charges(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[ChargeRead]:
    charges = charge_service.get_charges(db, skip=skip, limit=limit)
    return list(charges)


@router.post(
    "", response_model=ChargeRead, status_code=status.HTTP_201_CREATED,
    description="Create a new charge"
)
def create_charge(
    charge_in: ChargeCreate, db: Session = Depends(get_db)
) -> ChargeRead:
    charge = charge_service.create_charge(db, charge_in)
    return charge


@router.put(
    "/{charge_id}", status_code=status.HTTP_204_NO_CONTENT,
    description="Update a charge by ID"
)
def update_charge(
    charge_id: int, charge_in: ChargeUpdate, db: Session = Depends(get_db)
) -> Response:
    charge = charge_service.get_charge(db, charge_id)
    if charge is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Charge not found")
    charge_service.update_charge(db, charge, charge_in)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/{charge_id}", status_code=status.HTTP_204_NO_CONTENT, description="Delete a charge by ID")
def delete_charge(
    charge_id: int, db: Session = Depends(get_db)
) -> Response:
    charge = charge_service.get_charge(db, charge_id)
    if charge is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Charge not found")

    try:
        charge_service.delete_charge(db, charge)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se puede eliminar porque tiene registros relacionados.")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
