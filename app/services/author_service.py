from fastapi import HTTPException
from sqlmodel import select
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.schemas.author_schema import (
    AuthorProfileCreate, AuthorProfileUpdate)
from app.models.author_model import AuthorProfile
from app.schemas.user_schema import (UserResponse, UserRole)


async def get_author_profile_by_user_id(db: AsyncSession, user_id: int):
    statement = select(AuthorProfile).where(AuthorProfile.user_id == user_id)
    result = await db.execute(statement)
    return result.scalar_one_or_none()


async def get_author_profile_by_id(db: AsyncSession, id: int):
    statement = select(AuthorProfile).where(AuthorProfile.id == id)
    result = await db.execute(statement)
    return result.scalar_one_or_none()


async def check_if_pen_name_exists(db: AsyncSession, pen_name: str, user_id: int):
    statement = select(AuthorProfile).where(
        AuthorProfile.pen_name == pen_name,
        AuthorProfile.user_id == user_id
    )
    result = await db.execute(statement)
    return result.scalar_one_or_none()


async def create_new_author(
    db: AsyncSession,
    payload: AuthorProfileCreate,
    current_user: UserResponse
):
    # Check if profile already exists
    existing_profile = await get_author_profile_by_user_id(db, current_user.id)
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


async def update_profile(
    db: AsyncSession,
    payload: AuthorProfileUpdate,
    current_user: UserResponse
):
    # Check if profile already exists
    profile = await get_author_profile_by_user_id(db, current_user.id)
    if not profile:
        raise HTTPException(
            status_code=400,
            detail="Author profile not found"
        )

    updated_payload = payload.model_dump(exclude_unset=True)

    if "pen_name" in updated_payload:
        new_name = updated_payload["pen_name"]
        existing_name = await check_if_pen_name_exists(db, new_name, current_user.id)

        if existing_name:
            raise HTTPException(
                status_code=400,
                detail="Pen name already taken"
            )

    for key, value in updated_payload.items():
        setattr(profile, key, value)

    await db.commit()
    await db.refresh(profile)
    return profile


async def get_profile(db: AsyncSession, author_id: int):
    profile = await get_author_profile_by_id(db, author_id)
    if not profile:
        raise HTTPException(
            status_code=400,
            detail="Author profile not found"
        )

    return profile


async def list_authors(db: AsyncSession):
    statement = select(AuthorProfile)
    result = await db.execute(statement)
    return result.scalars().fetchall() or []
