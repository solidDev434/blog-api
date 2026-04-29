from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.schemas.author_schema import AuthorProfileCreate
from app.db.dependencies import get_db
from app.services.author_service import (
    create_new_author
)
from app.core.security import (get_current_user)
from app.schemas.user_schema import CurrentUserResponse

router = APIRouter(prefix="/authors", tags=["Authors"])


@router.post("/create")
async def create_author_profile(payload: AuthorProfileCreate, db: AsyncSession = Depends(get_db), res: CurrentUserResponse = Depends(get_current_user)):
    await create_new_author(db, payload, res.user)
    return {"message": "Author profile created"}
