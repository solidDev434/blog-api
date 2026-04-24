import logging
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.schemas.user_schema import UserCreateWithoutHash
from app.services.account_service import (
    register_user
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

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or username already exists"
        )

    except Exception as e:
        logger.error(f"Signup error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )
