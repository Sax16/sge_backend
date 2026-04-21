from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.services import enrollment_service
from app.dependencies import get_db, check_admin_or_super_admin
from app.schemas.enrollment import EnrollmentCreate, EnrollmentRead, EnrollmentUpdate


router = APIRouter(dependencies=[Depends(check_admin_or_super_admin)])


@router.get("/{enrollment_id}", response_model=EnrollmentRead, description="Get a enrollment by ID")
def get_enrollment(
    enrollment_id: int, db: Session = Depends(get_db)
) -> EnrollmentRead:
    enrollment = enrollment_service.get_enrollment(db, enrollment_id)
    if enrollment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enrollment not found")
    return enrollment


@router.get("", response_model=list[EnrollmentRead], description="List all enrollments")
def get_enrollments(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[EnrollmentRead]:
    enrollments = enrollment_service.get_enrollments(db, skip=skip, limit=limit)
    return list(enrollments)


@router.post(
    "", response_model=EnrollmentRead, status_code=status.HTTP_201_CREATED,
    description="Create a new enrollment"
)
def create_enrollment(
    enrollment_in: EnrollmentCreate, db: Session = Depends(get_db)
) -> EnrollmentRead:
    enrollment = enrollment_service.create_enrollment(db, enrollment_in)
    return enrollment


@router.put(
    "/{enrollment_id}", status_code=status.HTTP_204_NO_CONTENT,
    description="Update a enrollment by ID"
)
def update_enrollment(
    enrollment_id: int, enrollment_in: EnrollmentUpdate, db: Session = Depends(get_db)
) -> Response:
    enrollment = enrollment_service.get_enrollment(db, enrollment_id)
    if enrollment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enrollment not found")
    enrollment_service.update_enrollment(db, enrollment, enrollment_in)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/{enrollment_id}", status_code=status.HTTP_204_NO_CONTENT, description="Delete a enrollment by ID")
def delete_enrollment(
    enrollment_id: int, db: Session = Depends(get_db)
) -> Response:
    enrollment = enrollment_service.get_enrollment(db, enrollment_id)
    if enrollment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enrollment not found")

    try:
        enrollment_service.delete_enrollment(db, enrollment)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se puede eliminar porque tiene registros relacionados.")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
