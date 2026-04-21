from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.services import academic_period_service
from app.dependencies import get_db, check_admin_or_super_admin
from app.schemas.academic_period import AcademicPeriodCreate, AcademicPeriodRead, AcademicPeriodUpdate


router = APIRouter(dependencies=[Depends(check_admin_or_super_admin)])


@router.get("/{academic_period_id}", response_model=AcademicPeriodRead, description="Get a academic_period by ID")
def get_academic_period(
    academic_period_id: int, db: Session = Depends(get_db)
) -> AcademicPeriodRead:
    academic_period = academic_period_service.get_academic_period(db, academic_period_id)
    if academic_period is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AcademicPeriod not found")
    return academic_period


@router.get("", response_model=list[AcademicPeriodRead], description="List all academic_periods")
def get_academic_periods(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[AcademicPeriodRead]:
    academic_periods = academic_period_service.get_academic_periods(db, skip=skip, limit=limit)
    return list(academic_periods)


@router.post(
    "", response_model=AcademicPeriodRead, status_code=status.HTTP_201_CREATED,
    description="Create a new academic_period"
)
def create_academic_period(
    academic_period_in: AcademicPeriodCreate, db: Session = Depends(get_db)
) -> AcademicPeriodRead:
    academic_period = academic_period_service.create_academic_period(db, academic_period_in)
    return academic_period


@router.put(
    "/{academic_period_id}", status_code=status.HTTP_204_NO_CONTENT,
    description="Update a academic_period by ID"
)
def update_academic_period(
    academic_period_id: int, academic_period_in: AcademicPeriodUpdate, db: Session = Depends(get_db)
) -> Response:
    academic_period = academic_period_service.get_academic_period(db, academic_period_id)
    if academic_period is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AcademicPeriod not found")
    academic_period_service.update_academic_period(db, academic_period, academic_period_in)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/{academic_period_id}", status_code=status.HTTP_204_NO_CONTENT, description="Delete a academic_period by ID")
def delete_academic_period(
    academic_period_id: int, db: Session = Depends(get_db)
) -> Response:
    academic_period = academic_period_service.get_academic_period(db, academic_period_id)
    if academic_period is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AcademicPeriod not found")

    try:
        academic_period_service.delete_academic_period(db, academic_period)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se puede eliminar porque tiene registros relacionados.")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
