from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.dependencies import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserLogin

# 1. IMPORT OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordRequestForm

from app.services.auth import (
    hash_password,
    verify_password,
    create_access_token
)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/login")
async def login_user(
    # 2. SWAP UserLogin FOR THE FORM DEPENDENCY
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # 3. USE form_data.username INSTEAD OF user.email
    # (Swagger sends the email into the 'username' field of the form)
    existing_user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # 4. USE form_data.password INSTEAD OF user.password
    valid_password = verify_password(
        form_data.password,
        existing_user.password
    )

    if not valid_password:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={
            "user_id": existing_user.id,
            "email": existing_user.email
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/me")
async def get_me(
    current_user = Depends(get_current_user)
):
    return {
        "user": current_user
    }