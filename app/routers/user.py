from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.db.dependencies import get_db
from app.schemas.author_schema import AuthorProfileRead
from app.core.security import (
    get_current_user,
    require_role
)
from app.schemas.user_schema import (
    UserResponse, CurrentUserResponse, UserRole)
from app.services.author_service import get_author_profile_by_user_id

router = APIRouter(
    prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
async def get_authenticated_user(res: CurrentUserResponse = Depends(get_current_user)):
    return res.user


@router.get(
    "/me/author",
    response_model=AuthorProfileRead,
    dependencies=[Depends(require_role(UserRole.AUTHOR))]
)
async def get_user_author_profile(res: CurrentUserResponse = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await get_author_profile_by_user_id(db, res.user.id)
