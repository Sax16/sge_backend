from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.services import guardian_service
from app.dependencies import get_db, check_admin_or_super_admin
from app.schemas.guardian import GuardianCreate, GuardianRead, GuardianUpdate


router = APIRouter(dependencies=[Depends(check_admin_or_super_admin)])


@router.get("/{guardian_id}", response_model=GuardianRead, description="Get a guardian by ID")
def get_guardian(
    guardian_id: int, db: Session = Depends(get_db)
) -> GuardianRead:
    guardian = guardian_service.get_guardian(db, guardian_id)
    if guardian is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Guardian not found")
    return guardian


@router.get("", response_model=list[GuardianRead], description="List all guardians")
def get_guardians(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[GuardianRead]:
    guardians = guardian_service.get_guardians(db, skip=skip, limit=limit)
    return list(guardians)


@router.post(
    "", response_model=GuardianRead, status_code=status.HTTP_201_CREATED,
    description="Create a new guardian"
)
def create_guardian(
    guardian_in: GuardianCreate, db: Session = Depends(get_db)
) -> GuardianRead:
    guardian = guardian_service.create_guardian(db, guardian_in)
    return guardian


@router.put(
    "/{guardian_id}", status_code=status.HTTP_204_NO_CONTENT,
    description="Update a guardian by ID"
)
def update_guardian(
    guardian_id: int, guardian_in: GuardianUpdate, db: Session = Depends(get_db)
) -> Response:
    guardian = guardian_service.get_guardian(db, guardian_id)
    if guardian is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Guardian not found")
    guardian_service.update_guardian(db, guardian, guardian_in)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/{guardian_id}", status_code=status.HTTP_204_NO_CONTENT, description="Delete a guardian by ID")
def delete_guardian(
    guardian_id: int, db: Session = Depends(get_db)
) -> Response:
    guardian = guardian_service.get_guardian(db, guardian_id)
    if guardian is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Guardian not found")

    try:
        guardian_service.delete_guardian(db, guardian)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se puede eliminar porque tiene registros relacionados.")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
