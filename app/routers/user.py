from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db as get_async_db  #  Points cleanly to your updated file
from app.models.user import User
from app.schemas.user import UserCreate
from app.limiter import limiter  # Importing our rate limiter instance
from app.services.dependencies import get_current_user
from app.services.auth import (
    hash_password,
    verify_password,
    create_access_token
)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# === REGISTRATION ENDPOINT ===
@router.post("/register", status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")  # Protects against registration bot spam
async def register_user(
    request: Request,  # Required by SlowAPI to track requester IP
    user_data: UserCreate, 
    db: AsyncSession = Depends(get_async_db)
):
    """
    Register a brand new user profile into the database asynchronously.
    """
    # 1. Check if a user with this email already exists
    result = await db.execute(select(User).filter(User.email == user_data.email))
    existing_by_email = result.scalars().first()
    if existing_by_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email is already registered."
        )

    # 2. Check if a user with this username already exists
    result = await db.execute(select(User).filter(User.username == user_data.username))
    existing_by_username = result.scalars().first()
    if existing_by_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This username is already taken."
        )

    # 3. Hash the plain password safely before saving
    secure_password = hash_password(user_data.password)

    # 4. Save the fresh account into your PostgreSQL table
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        password=secure_password
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return {
        "id": new_user.id,
        "email": new_user.email,
        "username": new_user.username
    }


# === LOGIN ENDPOINT ===
@router.post("/login")
@limiter.limit("10/minute")  # Protects against brute-force password cracking
async def login_user(
    request: Request,  # Required by SlowAPI to track requester IP
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_async_db)  # Updated to AsyncSession!
):
    """
    Authenticate user via OAuth2 Form data and provide a JWT Access Token.
    """
    # 1. Asynchronously fetch user by email (passed to form_data.username by Swagger)
    result = await db.execute(select(User).filter(User.email == form_data.username))
    existing_user = result.scalars().first()

    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # 2. Verify password hash matches
    valid_password = verify_password(
        form_data.password,
        existing_user.password
    )

    if not valid_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # 3. Generate token containing key details
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


# === PROFILE ENDPOINT ===
@router.get("/me")
async def get_me(
    current_user = Depends(get_current_user)
):
    """
    Retrieve authenticated user details based on incoming JWT bearer token.
    """
    return {
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username
    }