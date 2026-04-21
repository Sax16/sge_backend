from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.services import student_service
from app.dependencies import get_db, check_admin_or_super_admin
from app.schemas.student import StudentCreate, StudentRead, StudentUpdate


router = APIRouter(dependencies=[Depends(check_admin_or_super_admin)])


@router.get("/{student_id}", response_model=StudentRead, description="Get a student by ID")
def get_student(
    student_id: int, db: Session = Depends(get_db)
) -> StudentRead:
    student = student_service.get_student(db, student_id)
    if student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return student


@router.get("", response_model=list[StudentRead], description="List all students")
def get_students(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[StudentRead]:
    students = student_service.get_students(db, skip=skip, limit=limit)
    return list(students)


@router.post(
    "", response_model=StudentRead, status_code=status.HTTP_201_CREATED,
    description="Create a new student"
)
def create_student(
    student_in: StudentCreate, db: Session = Depends(get_db)
) -> StudentRead:
    student = student_service.create_student(db, student_in)
    return student


@router.put(
    "/{student_id}", status_code=status.HTTP_204_NO_CONTENT,
    description="Update a student by ID"
)
def update_student(
    student_id: int, student_in: StudentUpdate, db: Session = Depends(get_db)
) -> Response:
    student = student_service.get_student(db, student_id)
    if student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    student_service.update_student(db, student, student_in)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT, description="Delete a student by ID")
def delete_student(
    student_id: int, db: Session = Depends(get_db)
) -> Response:
    student = student_service.get_student(db, student_id)
    if student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    try:
        student_service.delete_student(db, student)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se puede eliminar porque tiene registros relacionados.")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
