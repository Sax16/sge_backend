from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.crud.user import (
    create_user_crud,
    delete_user_crud,
    get_user_crud,
    get_users_crud,
    update_user_crud,
)
from app.dependencies import get_db
from app.schemas.user import UserCreate, UserRead, UserUpdate


router = APIRouter()


@router.get("/{user_id}", response_model=UserRead, description="Get a user by ID")
def get_user(
    user_id: int, db: Session = Depends(get_db)
) -> UserRead:
    user = get_user_crud(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.get("", response_model=list[UserRead], description="Get all users")
def get_users(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[UserRead]:
    users = get_users_crud(db, skip=skip, limit=limit) 
    return list(users)


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED, description="Create a new user")
def create_user(
    user_in: UserCreate, db: Session = Depends(get_db)
) -> UserRead:
    user = create_user_crud(db, user_in)
    return user


@router.put("/{user_id}", response_model=UserRead, description="Update a user by ID")
def update_user(
    user_id: int, user_in: UserUpdate, db: Session = Depends(get_db)
) -> UserRead:
    user = get_user_crud(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    updated = update_user_crud(db, user, user_in)
    return updated


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, description="Delete a user by ID")
def delete_user(
    user_id: int, db: Session = Depends(get_db)
) -> Response:
    user = get_user_crud(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    delete_user_crud(db, user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
