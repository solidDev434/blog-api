from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.schemas.user_schema import (
    UserCreateWithoutHash,
    UserCreateWithHash
)
from app.services.user_service import (
    create_user,
    get_user_by_email,
    get_user_by_username,
    get_user_by_email_or_username
)
from app.core.security import (
    verify_password,
    hash_password,
    create_access_token,
    create_refresh_token
)


async def register_user(db: AsyncSession, payload: UserCreateWithoutHash):
    """Checks if user exists and creates user if all criteria's are met"""
    existing = await get_user_by_email_or_username(db, payload.email, payload.username)
    if existing:
        if existing.email == payload.email:
            detail = "Email already registered"
        else:
            detail = "Username already taken"

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )

    existing_username = await get_user_by_username(db, payload.username)
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This username is already taken"
        )

    # Hash user password
    hashed_password = hash_password(payload.password)

    new_user_payload = UserCreateWithHash(
        **payload.model_dump(exclude={"password"}),
        hashed_password=hashed_password,
    )

    # Create new user
    return await create_user(db, new_user_payload)


def login_user():
    """Verifies if user account is active before returning authentication tokens"""


def verify_email():
    """Verifies user email"""


def forgot_password():
    """Checks if user exists and proceeds to send unique passowrd verification link"""


def reset_password():
    """Updates user password"""
