from logging import Logger
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
    ResendVerificationMail,
    ForgotPassword,
    ResetPassword
)
from app.services.user_service import (
    create_user,
    get_user_by_email,
    get_user_by_username,
    get_user_by_email_or_username,
    update_user_password,
    verify_user,
    store_user_login_time
)
from app.core.security import (
    verify_password,
    verify_token,
    hash_password,
    create_temporary_token,
    create_access_token,
    create_refresh_token
)
from .email_service import send_verify_mail
from .cache_service import CacheService

logger = Logger(__name__)


async def verify_and_check_user_is_inactive(db: AsyncSession, email: str):
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


async def verify_if_user_exists_and_is_active(db: AsyncSession, email: str):
    user = await get_user_by_email(db, email)

    if user == None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentail"
        )

    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verify mail to have access"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User account isn't activated"
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
    print("New Payload", new_user_payload)

    # Create email verification token
    token = create_temporary_token(data={"email": payload.email})

    # Create new user
    user = await create_user(db, new_user_payload)

    # Send verification mail
    logger.info(f"Send verifcation mail to {payload.email}")
    await send_verify_mail(payload.email, token)

    return user


async def login_user(db: AsyncSession, payload: LoginUser):
    """Verifies if user account is active before returning authentication tokens"""
    user = await verify_if_user_exists_and_is_active(db, payload.email)

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

    # Store user login timestamp
    await store_user_login_time(db, user.id)

    return Token(access_token=access_token, refresh_token=refresh_token)


async def verify_user_mail(db: AsyncSession, payload: VerifyEmail):
    """Verifies user email"""
    token_payload = verify_token(payload.token)
    user = await verify_and_check_user_is_inactive(db, token_payload["email"])

    # Activate user account
    await verify_user(db, user.id)


async def resend_mail(db: AsyncSession, payload: ResendVerificationMail):
    """Resends verification mail to user"""
    await verify_and_check_user_is_inactive(db, payload.email)

    token = create_temporary_token(data={"email": payload.email}, minutes=7)
    await send_verify_mail(payload.email, token)


async def forgot_password(db: AsyncSession, payload: ForgotPassword):
    """Checks if user exists and proceeds to send unique passowrd verification link"""
    user = await get_user_by_email(db, payload.email)

    if user == None:
        raise HTTPException(
            status_code=status.HTTP_202_ACCEPTED
        )

    token = create_temporary_token(data={"email": payload.email}, minutes=5)
    print(f"Temporary Token {token}")

    return token


async def reset_password(db: AsyncSession, payload: ResetPassword):
    """Updates user password"""
    token_payload = verify_token(payload.token)
    user = await verify_if_user_exists_and_is_active(db, token_payload["email"])

    # Check if password is similar
    verify_new_password = verify_password(
        payload.new_password, user.hashed_password)
    if verify_new_password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Password can't be the same, use something else"
        )

    # Hash password
    hashed_password = hash_password(payload.new_password)

    # Update user
    await update_user_password(db, user.id, hashed_password)


async def logout_authenticated_user(token: str, cache: CacheService):
    key = f"bl:{token}"
    cached_token = await cache.get(key)
    if cached_token:
        return

    # Blacklist token
    await cache.set(key, token)
