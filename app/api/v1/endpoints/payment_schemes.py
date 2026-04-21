from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.services import payment_scheme_service
from app.dependencies import get_db, check_admin_or_super_admin
from app.schemas.payment_scheme import PaymentSchemeCreate, PaymentSchemeRead, PaymentSchemeUpdate


router = APIRouter(dependencies=[Depends(check_admin_or_super_admin)])


@router.get("/{payment_scheme_id}", response_model=PaymentSchemeRead, description="Get a payment_scheme by ID")
def get_payment_scheme(
    payment_scheme_id: int, db: Session = Depends(get_db)
) -> PaymentSchemeRead:
    payment_scheme = payment_scheme_service.get_payment_scheme(db, payment_scheme_id)
    if payment_scheme is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PaymentScheme not found")
    return payment_scheme


@router.get("", response_model=list[PaymentSchemeRead], description="List all payment_schemes")
def get_payment_schemes(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[PaymentSchemeRead]:
    payment_schemes = payment_scheme_service.get_payment_schemes(db, skip=skip, limit=limit)
    return list(payment_schemes)


@router.post(
    "", response_model=PaymentSchemeRead, status_code=status.HTTP_201_CREATED,
    description="Create a new payment_scheme"
)
def create_payment_scheme(
    payment_scheme_in: PaymentSchemeCreate, db: Session = Depends(get_db)
) -> PaymentSchemeRead:
    payment_scheme = payment_scheme_service.create_payment_scheme(db, payment_scheme_in)
    return payment_scheme


@router.put(
    "/{payment_scheme_id}", status_code=status.HTTP_204_NO_CONTENT,
    description="Update a payment_scheme by ID"
)
def update_payment_scheme(
    payment_scheme_id: int, payment_scheme_in: PaymentSchemeUpdate, db: Session = Depends(get_db)
) -> Response:
    payment_scheme = payment_scheme_service.get_payment_scheme(db, payment_scheme_id)
    if payment_scheme is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PaymentScheme not found")
    payment_scheme_service.update_payment_scheme(db, payment_scheme, payment_scheme_in)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/{payment_scheme_id}", status_code=status.HTTP_204_NO_CONTENT, description="Delete a payment_scheme by ID")
def delete_payment_scheme(
    payment_scheme_id: int, db: Session = Depends(get_db)
) -> Response:
    payment_scheme = payment_scheme_service.get_payment_scheme(db, payment_scheme_id)
    if payment_scheme is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PaymentScheme not found")

    try:
        payment_scheme_service.delete_payment_scheme(db, payment_scheme)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se puede eliminar porque tiene registros relacionados.")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
