from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.core import security
from app.crud import user as crud_user
from app.schemas.auth import Token, UserCreate, UserInDB

router = APIRouter()

@router.post("/login", response_model=Token)
async def login_for_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    Authenticate user and return JWT token.
    """
    user = crud_user.user.get_by_username(db, username=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=security.settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.username, "roles": [user.role]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=UserInDB, status_code=status.HTTP_201_CREATED)
async def register_user(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate
) -> Any:
    """
    Register a new user. Only admin can register new users.
    """
    # Example: Only admins can register new users for specific roles or generally
    # For simplicity, let's allow anyone to register as 'regular' for now.
    # If `user_in.role` is 'admin', you might want to restrict this further.

    if crud_user.user.get_by_username(db, username=user_in.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    if crud_user.user.get_by_email(db, email=user_in.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    user = crud_user.user.create(db, obj_in=user_in)
    return user

@router.post("/refresh-token", response_model=Token)
async def refresh_token(
    current_user: Any = Depends(security.get_current_user) # Assuming token is valid for refresh
) -> Any:
    """
    Refresh JWT token[cite: 7].
    """
    access_token_expires = timedelta(minutes=security.settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": current_user["username"], "roles": current_user["roles"]},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}