from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.services.auth_service import authenticate_user
from app.core.security import create_access_token
from app.schemas.token import Token
from app.schemas.user import UserRead

router = APIRouter()

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.user_name})
    return {"access_token": access_token, "token_type": "Bearer"}


@router.get("/login/me", response_model=UserRead)
async def read_users_me(
    current_user: UserRead = Depends(get_current_user),
) -> UserRead:
    return current_user