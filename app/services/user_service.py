from fastapi import HTTPException, status
from collections.abc import Sequence

from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.crud import user_crud, employee_crud


def get_user(db: Session, user_id: int) -> User | None:
    return user_crud.get_user(db, user_id)


def get_users(db: Session, skip: int = 0, limit: int = 100) -> Sequence[User]:
    return user_crud.get_users(db, skip=skip, limit=limit)


def get_user_by_username(db: Session, username: str) -> User | None:
    return user_crud.get_user_by_username(db, username)


def create_user(db: Session, user: UserCreate) -> User:
    # Validate that the username does not exist
    existing_user = user_crud.get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    # Validate that the employee exists
    existing_employee = employee_crud.get_employee(db, user.employee_id)
    if existing_employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")

    # Validate that the employee is not already assigned to a user
    existing_user = user_crud.get_user_by_employee_id(db, user.employee_id)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Employee already assigned to a user")

    # Hash the password
    user.password = get_password_hash(user.password)
    
    return user_crud.create_user(db, user)


def update_user(db: Session, user: User, user_in: UserUpdate) -> User:
    # Validate that if the username exists, it's the same user
    existing_user = user_crud.get_user_by_username(db, user_in.username)
    if existing_user and existing_user.id != user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    # Hash the password if it exists
    if user_in.password:
        user_in.password = get_password_hash(user_in.password)
    
    return user_crud.update_user(db, user, user_in)


def delete_user(db: Session, user: User) -> None:
    user_crud.delete_user(db, user)