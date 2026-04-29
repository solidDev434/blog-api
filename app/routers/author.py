from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.schemas.author_schema import (
    AuthorProfileCreate,
    AuthorProfileUpdate,
    AuthorProfileRead
)
from app.db.dependencies import get_db
from app.services.author_service import (
    create_new_author,
    update_profile,
    get_profile
)
from app.core.security import (get_current_user)
from app.schemas.user_schema import CurrentUserResponse

router = APIRouter(prefix="/authors", tags=["Authors"])


@router.get("/{author_id}", response_model=AuthorProfileRead)
async def get_author_profile(author_id: int, db: AsyncSession = Depends(get_db)):
    return await get_profile(db, author_id)


@router.post("/create")
async def create_author_profile(payload: AuthorProfileCreate, db: AsyncSession = Depends(get_db), res: CurrentUserResponse = Depends(get_current_user)):
    await create_new_author(db, payload, res.user)
    return {"message": "Author profile created"}


@router.patch("/me", response_model=AuthorProfileRead)
async def update_author_profile(
    payload: AuthorProfileUpdate,
    db: AsyncSession = Depends(get_db),
    res: CurrentUserResponse = Depends(get_current_user)
):
    return await update_profile(db, payload, res.user)
    return {"message": "Author profile created"}
