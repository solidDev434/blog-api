import logging
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.schemas.user_schema import UserCreateWithoutHash
from app.services.account_service import (
    register_user,
    login_user,
    verify_user_mail,
    resend_mail
)
from app.schemas.account_schema import (
    LoginUser,
    VerifyEmail,
    ResendVerificationMail
)
from app.db.dependencies import get_db

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
async def create_new_user(payload: LoginUser, db: AsyncSession = Depends(get_db)):
    try:
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
