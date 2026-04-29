import logging
from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.schemas.user_schema import (
    UserCreateWithoutHash, CurrentUserResponse)
from app.services.account_service import (
    register_user,
    login_user,
    verify_user_mail,
    resend_mail,
    forgot_password,
    reset_password,
    logout_authenticated_user
)
from app.schemas.account_schema import (
    LoginUser,
    VerifyEmail,
    ResendVerificationMail,
    ForgotPassword,
    ResetPassword
)
from app.db.dependencies import (
    get_db,
    get_cache
)
from app.core.security import get_current_user
from app.services.cache_service import CacheService

router = APIRouter(prefix="/account", tags=["Authentication"])
logger = logging.getLogger(__name__)


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_new_user(payload: UserCreateWithoutHash, db: AsyncSession = Depends(get_db)):
    try:
        await register_user(db, payload)
        return {"message": "User successfully created"}

    except HTTPException as e:
        raise e

    except Exception as e:
        logger.error(f"Signup error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )


@router.post("/login", status_code=status.HTTP_200_OK)
async def create_new_user(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    try:
        payload = LoginUser(email=form_data.username,
                            password=form_data.password)
        return await login_user(db, payload)

    except HTTPException as e:
        raise e

    except Exception as e:
        logger.error(f"Login error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )


@router.post("/verify-email", status_code=status.HTTP_200_OK)
async def verify_email(payload: VerifyEmail, db: AsyncSession = Depends(get_db)):
    try:
        await verify_user_mail(db, payload)
        return {"message": "Email successfully verified"}

    except HTTPException as e:
        raise e

    except Exception as e:
        logger.error(f"Email Verification error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )


@router.post("/resend-verification-mail", status_code=status.HTTP_200_OK)
async def resend_verification_mail(payload: ResendVerificationMail, db: AsyncSession = Depends(get_db)):
    try:
        await resend_mail(db, payload)
        return {"message": "Email successfully sent"}

    except HTTPException as e:
        raise e

    except Exception as e:
        logger.error(f"Failed Email Resend error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )


@router.post("/forgot-password", status_code=status.HTTP_202_ACCEPTED)
async def request_reset_password(payload: ForgotPassword, db: AsyncSession = Depends(get_db)):
    try:
        token = await forgot_password(db, payload)
        return {"message": "If an account exists with the email, a reset link has been sent.", "token": token}

    except HTTPException as e:
        raise e

    except Exception as e:
        logger.error(
            f"Failed Reset Password Request error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )


@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_user_password(payload: ResetPassword, db: AsyncSession = Depends(get_db)):
    try:
        await reset_password(db, payload)
        return {"message": "Reset Password successful"}

    except HTTPException as e:
        raise e

    except Exception as e:
        logger.error(
            f"Failed Reset Password Request error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout_user(cache: CacheService = Depends(get_cache), res: CurrentUserResponse = Depends(get_current_user)):
    try:
        await logout_authenticated_user(res.token, cache)
        return {"message": "Logged out user"}

    except HTTPException as e:
        raise e

    except Exception as e:
        logger.error(
            f"Failed to Logout user error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )
