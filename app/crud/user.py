from collections.abc import Sequence

from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


def get_user_crud(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def get_users_crud(db: Session, skip: int = 0, limit: int = 100) -> Sequence[User]:
    return db.query(User).order_by(User.id).offset(skip).limit(limit).all()


def create_user_crud(db: Session, user_in: UserCreate) -> User:
    user = User(**user_in.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user_crud(
    db: Session, user: User, user_in: UserUpdate
) -> User:
    data = user_in.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(user, key, value)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def delete_user_crud(db: Session, user: User) -> None:
    db.delete(user)
    db.commit()