from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.schemas.user_schema import (
    UserCreateWithoutHash,
    UserCreateWithHash
)
from app.schemas.account_schema import (
    Token,
    LoginUser,
    VerifyEmail,
    ResendVerificationMail
)
from app.services.user_service import (
    create_user,
    get_user_by_email,
    get_user_by_username,
    get_user_by_email_or_username,
    activate_user
)
from app.core.security import (
    verify_password,
    verify_token,
    hash_password,
    create_temporary_token,
    create_access_token,
    create_refresh_token
)


async def verify_user(db: AsyncSession, email: str):
    user = await get_user_by_email(db, email)

    if user == None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid credentail"
        )

    if user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User account is already verified"
        )

    return user


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

    # Create email verification token
    token = create_temporary_token(data={"email": payload.email}, minutes=7)
    print(f"Temporary Token {token}")
    # Send mail
    # https://domain.com/verify-email?token={token}

    # Create new user
    return await create_user(db, new_user_payload)


async def login_user(db: AsyncSession, payload: LoginUser):
    """Verifies if user account is active before returning authentication tokens"""
    print(payload)
    user = await get_user_by_email(db, payload.email)

    if user == None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentail"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User account isn't activated"
        )

    # Verify user password
    password_is_valid = verify_password(payload.password, user.hashed_password)
    if not password_is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentail"
        )

    # Generate tokens
    token_data = {
        "id": user.id,
        "email": user.email,
        "role": user.role
    }
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return Token(access_token=access_token, refresh_token=refresh_token)


async def verify_user_mail(db: AsyncSession, payload: VerifyEmail):
    """Verifies user email"""
    payload = verify_token(payload.token)
    user = await verify_user(db, payload["email"])

    # Activate user account
    await activate_user(db, user.id)


async def resend_mail(db: AsyncSession, payload: ResendVerificationMail):
    """Resends verification mail to user"""
    await verify_user(db, payload.email)

    token = create_temporary_token(data={"email": payload.email}, minutes=7)
    print(token)


def forgot_password():
    """Checks if user exists and proceeds to send unique passowrd verification link"""


def reset_password():
    """Updates user password"""
