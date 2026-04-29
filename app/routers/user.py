from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.schemas.user_schema import (
    UserResponse,
    CurrentUserResponse
)

router = APIRouter(
    prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
async def get_authenticated_user(res: CurrentUserResponse = Depends(get_current_user)):
    return res.user
