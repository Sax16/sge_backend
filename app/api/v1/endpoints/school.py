from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.services import school_service
from app.dependencies import get_db, check_admin_or_super_admin
from app.schemas.school import SchoolCreate, SchoolRead, SchoolUpdate


router = APIRouter(dependencies=[Depends(check_admin_or_super_admin)])


@router.post(
    "", response_model=SchoolRead, status_code=status.HTTP_201_CREATED,
    description="Register the institution's general information. Only one allowing."
)
def create_school(
    school_in: SchoolCreate, db: Session = Depends(get_db)
) -> SchoolRead:
    school = school_service.create_school(db, school_in)
    return school


@router.get("/{school_id}", response_model=SchoolRead, description="Get the school information by ID")
def get_school(
    school_id: int, db: Session = Depends(get_db)
) -> SchoolRead:
    school = school_service.get_school(db, school_id)
    if school is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="School not found")
    return school


@router.put(
    "/{school_id}", status_code=status.HTTP_204_NO_CONTENT,
    description="Update the school information by ID"
)
def update_school(
    school_id: int, school_in: SchoolUpdate, db: Session = Depends(get_db)
) -> Response:
    school = school_service.get_school(db, school_id)
    if school is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="School not found")
    school_service.update_school(db, school, school_in)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
