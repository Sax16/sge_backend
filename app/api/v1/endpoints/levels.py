from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.services import level_service
from app.dependencies import get_db, check_admin_or_super_admin
from app.schemas.level import LevelCreate, LevelRead, LevelUpdate


router = APIRouter(dependencies=[Depends(check_admin_or_super_admin)])


@router.get("/{level_id}", response_model=LevelRead, description="Get a level by ID")
def get_level(
    level_id: int, db: Session = Depends(get_db)
) -> LevelRead:
    level = level_service.get_level(db, level_id)
    if level is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Level not found")
    return level


@router.get("", response_model=list[LevelRead], description="List all levels")
def get_levels(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[LevelRead]:
    levels = level_service.get_levels(db, skip=skip, limit=limit)
    return list(levels)


@router.post(
    "", response_model=LevelRead, status_code=status.HTTP_201_CREATED,
    description="Create a new level"
)
def create_level(
    level_in: LevelCreate, db: Session = Depends(get_db)
) -> LevelRead:
    level = level_service.create_level(db, level_in)
    return level


@router.put(
    "/{level_id}", status_code=status.HTTP_204_NO_CONTENT,
    description="Update a level by ID"
)
def update_level(
    level_id: int, level_in: LevelUpdate, db: Session = Depends(get_db)
) -> Response:
    level = level_service.get_level(db, level_id)
    if level is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Level not found")
    level_service.update_level(db, level, level_in)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/{level_id}", status_code=status.HTTP_204_NO_CONTENT, description="Delete a level by ID")
def delete_level(
    level_id: int, db: Session = Depends(get_db)
) -> Response:
    level = level_service.get_level(db, level_id)
    if level is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Level not found")

    try:
        level_service.delete_level(db, level)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se puede eliminar porque tiene registros relacionados.")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
