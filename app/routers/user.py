from fastapi import APIRouter, Depends
from app.core.security import (
    get_current_user,
    require_role
)
from app.schemas.user_schema import UserResponse

router = APIRouter(
    prefix="/users", tags=["Users"])


@router.get("/me")
async def get_authenticated_user(current_user: UserResponse = Depends(get_current_user)):
    return current_user
