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
    # Si el usuario no existe, lanzar una excepción
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Contraseña o usuario incorrecto!",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Si el usuario no está activo, lanzar una excepción
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Este usuario esta deshabilitado!",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Crear el token de acceso
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "Bearer"}


@router.get("/login/me", response_model=UserRead)
async def read_users_me(
    current_user: UserRead = Depends(get_current_user),
) -> UserRead:
    return current_user