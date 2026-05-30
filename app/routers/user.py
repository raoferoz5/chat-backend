from fastapi import APIRouter, Depends, HTTPException, status
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


# === NEW REGISTRATION ENDPOINT ===
@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate, 
    db: Session = Depends(get_db)
):
    """
    Register a brand new user profile into the database.
    """
    # 1. Check if a user with this email already exists
    existing_by_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_by_email:
        raise HTTPException(
            status_code=400,
            detail="A user with this email is already registered."
        )

    # 2. Check if a user with this username already exists (optional but recommended)
    existing_by_username = db.query(User).filter(User.username == user_data.username).first()
    if existing_by_username:
        raise HTTPException(
            status_code=400,
            detail="This username is already taken."
        )

    # 3. Hash the plain password safely before saving
    secure_password = hash_password(user_data.password)

    # 4. Save the fresh account into your PostgreSQL table
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        password=secure_password  # Storing the securely encrypted hash string
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully!",
        "user_id": new_user.id,
        "email": new_user.email,
        "username": new_user.username
    }


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
            "email": existing_user.email,
            "username": existing_user.username
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
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username
    }