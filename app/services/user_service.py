from collections.abc import Sequence

from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.crud import user_crud


def get_user(db: Session, user_id: int) -> User | None:
    return user_crud.get_user(db, user_id)


def get_users(db: Session, skip: int = 0, limit: int = 100) -> Sequence[User]:
    return user_crud.get_users(db, skip=skip, limit=limit)


def get_user_by_username(db: Session, user_name: str) -> User | None:
    return user_crud.get_user_by_username(db, user_name)


def create_user(db: Session, user: UserCreate) -> User:
    return user_crud.create_user(db, user)


def update_user(db: Session, user: User, user_in: UserUpdate) -> User:
    return user_crud.update_user(db, user, user_in)


def delete_user(db: Session, user: User) -> None:
    user_crud.delete_user(db, user)