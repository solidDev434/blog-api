from fastapi import HTTPException
from sqlmodel import select
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.schemas.author_schema import AuthorProfileCreate
from app.models.author_model import AuthorProfile
from app.schemas.user_schema import (UserResponse, UserRole)


async def check_if_author_profile_exist(db: AsyncSession, user_id: int):
    statement = select(AuthorProfile).where(AuthorProfile.user_id == user_id)
    result = await db.execute(statement)
    return result.scalars().first()


async def create_new_author(db: AsyncSession, payload: AuthorProfileCreate, current_user: UserResponse):
    # Check if profile already exists
    existing_profile = await check_if_author_profile_exist(db, current_user.id)
    if existing_profile:
        raise HTTPException(
            status_code=400,
            detail="User already has an author profile."
        )

    # Check if ther user has the right permissions
    if current_user.role != UserRole.AUTHOR:
        raise HTTPException(
            status_code=403,
            detail="User does not have the Author role."
        )

    new_profile = AuthorProfile(
        **payload.model_dump(),
        user_id=current_user.id
    )

    db.add(new_profile)
    await db.commit()
    await db.refresh(new_profile)
