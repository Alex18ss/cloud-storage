from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import or_
from sqlalchemy.orm import Session

from core.database import get_db
from core.security import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
    get_password_hash,
)
from models.user import User
from schemas.user_pudantic import AuthResponse, Token, UserCreate, UserLogin, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])


def build_auth_response(user: User) -> AuthResponse:
    access_token = create_access_token({"sub": str(user.id), "email": user.email})
    return AuthResponse(access_token=access_token, token_type="bearer", user=user)


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        or_(User.email == user_data.email, User.username == user_data.username)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or username already exists",
        )

    new_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=get_password_hash(user_data.password),
        is_active=True,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return build_auth_response(new_user)


@router.post("/login", response_model=AuthResponse)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, user_data.email, user_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is blocked",
        )

    return build_auth_response(user)


@router.post("/token", response_model=Token)
def login_for_access_token(
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

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is blocked",
        )

    access_token = create_access_token({"sub": str(user.id), "email": user.email})
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_active_user)):
    return current_user
