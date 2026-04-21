from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.services import economic_level_service
from app.dependencies import get_db, check_admin_or_super_admin
from app.schemas.economic_level import EconomicLevelCreate, EconomicLevelRead, EconomicLevelUpdate


router = APIRouter(dependencies=[Depends(check_admin_or_super_admin)])


@router.get("/{economic_level_id}", response_model=EconomicLevelRead, description="Get a economic_level by ID")
def get_economic_level(
    economic_level_id: int, db: Session = Depends(get_db)
) -> EconomicLevelRead:
    economic_level = economic_level_service.get_economic_level(db, economic_level_id)
    if economic_level is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="EconomicLevel not found")
    return economic_level


@router.get("", response_model=list[EconomicLevelRead], description="List all economic_levels")
def get_economic_levels(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[EconomicLevelRead]:
    economic_levels = economic_level_service.get_economic_levels(db, skip=skip, limit=limit)
    return list(economic_levels)


@router.post(
    "", response_model=EconomicLevelRead, status_code=status.HTTP_201_CREATED,
    description="Create a new economic_level"
)
def create_economic_level(
    economic_level_in: EconomicLevelCreate, db: Session = Depends(get_db)
) -> EconomicLevelRead:
    economic_level = economic_level_service.create_economic_level(db, economic_level_in)
    return economic_level


@router.put(
    "/{economic_level_id}", status_code=status.HTTP_204_NO_CONTENT,
    description="Update a economic_level by ID"
)
def update_economic_level(
    economic_level_id: int, economic_level_in: EconomicLevelUpdate, db: Session = Depends(get_db)
) -> Response:
    economic_level = economic_level_service.get_economic_level(db, economic_level_id)
    if economic_level is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="EconomicLevel not found")
    economic_level_service.update_economic_level(db, economic_level, economic_level_in)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/{economic_level_id}", status_code=status.HTTP_204_NO_CONTENT, description="Delete a economic_level by ID")
def delete_economic_level(
    economic_level_id: int, db: Session = Depends(get_db)
) -> Response:
    economic_level = economic_level_service.get_economic_level(db, economic_level_id)
    if economic_level is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="EconomicLevel not found")

    try:
        economic_level_service.delete_economic_level(db, economic_level)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se puede eliminar porque tiene registros relacionados.")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
