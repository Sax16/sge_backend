from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.services import grade_service
from app.dependencies import get_db, check_admin_or_super_admin
from app.schemas.grade import GradeCreate, GradeRead, GradeUpdate


router = APIRouter(dependencies=[Depends(check_admin_or_super_admin)])


@router.get("/{grade_id}", response_model=GradeRead, description="Get a grade by ID")
def get_grade(
    grade_id: int, db: Session = Depends(get_db)
) -> GradeRead:
    grade = grade_service.get_grade(db, grade_id)
    if grade is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grade not found")
    return grade


@router.get("", response_model=list[GradeRead], description="List all grades")
def get_grades(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[GradeRead]:
    grades = grade_service.get_grades(db, skip=skip, limit=limit)
    return list(grades)


@router.post(
    "", response_model=GradeRead, status_code=status.HTTP_201_CREATED,
    description="Create a new grade"
)
def create_grade(
    grade_in: GradeCreate, db: Session = Depends(get_db)
) -> GradeRead:
    grade = grade_service.create_grade(db, grade_in)
    return grade


@router.put(
    "/{grade_id}", status_code=status.HTTP_204_NO_CONTENT,
    description="Update a grade by ID"
)
def update_grade(
    grade_id: int, grade_in: GradeUpdate, db: Session = Depends(get_db)
) -> Response:
    grade = grade_service.get_grade(db, grade_id)
    if grade is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grade not found")
    grade_service.update_grade(db, grade, grade_in)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/{grade_id}", status_code=status.HTTP_204_NO_CONTENT, description="Delete a grade by ID")
def delete_grade(
    grade_id: int, db: Session = Depends(get_db)
) -> Response:
    grade = grade_service.get_grade(db, grade_id)
    if grade is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grade not found")

    try:
        grade_service.delete_grade(db, grade)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se puede eliminar porque tiene registros relacionados.")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
