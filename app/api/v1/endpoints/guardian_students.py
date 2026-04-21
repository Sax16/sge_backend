from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.services import guardian_student_service
from app.dependencies import get_db, check_admin_or_super_admin
from app.schemas.guardian_student import GuardianStudentCreate, GuardianStudentRead, GuardianStudentUpdate


router = APIRouter(dependencies=[Depends(check_admin_or_super_admin)])


@router.get("/{guardian_student_id}", response_model=GuardianStudentRead, description="Get a guardian_student by ID")
def get_guardian_student(
    guardian_student_id: int, db: Session = Depends(get_db)
) -> GuardianStudentRead:
    guardian_student = guardian_student_service.get_guardian_student(db, guardian_student_id)
    if guardian_student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="GuardianStudent not found")
    return guardian_student


@router.get("", response_model=list[GuardianStudentRead], description="List all guardian_students")
def get_guardian_students(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[GuardianStudentRead]:
    guardian_students = guardian_student_service.get_guardian_students(db, skip=skip, limit=limit)
    return list(guardian_students)


@router.post(
    "", response_model=GuardianStudentRead, status_code=status.HTTP_201_CREATED,
    description="Create a new guardian_student"
)
def create_guardian_student(
    guardian_student_in: GuardianStudentCreate, db: Session = Depends(get_db)
) -> GuardianStudentRead:
    guardian_student = guardian_student_service.create_guardian_student(db, guardian_student_in)
    return guardian_student


@router.put(
    "/{guardian_student_id}", status_code=status.HTTP_204_NO_CONTENT,
    description="Update a guardian_student by ID"
)
def update_guardian_student(
    guardian_student_id: int, guardian_student_in: GuardianStudentUpdate, db: Session = Depends(get_db)
) -> Response:
    guardian_student = guardian_student_service.get_guardian_student(db, guardian_student_id)
    if guardian_student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="GuardianStudent not found")
    guardian_student_service.update_guardian_student(db, guardian_student, guardian_student_in)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/{guardian_student_id}", status_code=status.HTTP_204_NO_CONTENT, description="Delete a guardian_student by ID")
def delete_guardian_student(
    guardian_student_id: int, db: Session = Depends(get_db)
) -> Response:
    guardian_student = guardian_student_service.get_guardian_student(db, guardian_student_id)
    if guardian_student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="GuardianStudent not found")

    try:
        guardian_student_service.delete_guardian_student(db, guardian_student)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se puede eliminar porque tiene registros relacionados.")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
