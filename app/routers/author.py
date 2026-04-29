from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from typing import List

from app.schemas.author_schema import (
    AuthorProfileCreate,
    AuthorProfileUpdate,
    AuthorProfileRead
)
from app.db.dependencies import get_db
from app.services.author_service import (
    create_new_author,
    update_profile,
    get_profile,
    list_authors,
    get_author_profile_by_user_id
)
from app.core.security import (
    get_current_user,
    require_role
)
from app.schemas.user_schema import (CurrentUserResponse, UserRole)

router = APIRouter(prefix="/authors", tags=["Authors"])


@router.get("", response_model=List[AuthorProfileRead])
async def get_all_authors(db: AsyncSession = Depends(get_db)):
    return await list_authors(db)


@router.get(
    "/me",
    response_model=AuthorProfileRead,
    dependencies=[Depends(require_role(UserRole.AUTHOR))]
)
async def get_user_author_profile(res: CurrentUserResponse = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await get_author_profile_by_user_id(db, res.user.id)


@router.get(
    "/{author_id}",
    response_model=AuthorProfileRead
)
async def get_author_profile(author_id: int, db: AsyncSession = Depends(get_db)):
    return await get_profile(db, author_id)


@router.post(
    "/create",
    dependencies=[Depends(require_role(UserRole.AUTHOR))]
)
async def create_author_profile(payload: AuthorProfileCreate, db: AsyncSession = Depends(get_db), res: CurrentUserResponse = Depends(get_current_user)):
    await create_new_author(db, payload, res.user)
    return {"message": "Author profile created"}


@router.patch(
    "/me",
    response_model=AuthorProfileRead,
    dependencies=[Depends(require_role(UserRole.AUTHOR))]
)
async def update_author_profile(
    payload: AuthorProfileUpdate,
    db: AsyncSession = Depends(get_db),
    res: CurrentUserResponse = Depends(get_current_user)
):
    return await update_profile(db, payload, res.user)
