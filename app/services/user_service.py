from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import select, or_, update
from app.models.user_model import User
from app.schemas.user_schema import (
    UserCreateWithHash,
)


async def create_user(db: AsyncSession, payload: UserCreateWithHash):
    # Create new user
    user = User(
        email=payload.email,
        full_name=payload.full_name,
        username=payload.username,
        role=payload.role,
        hashed_password=payload.hashed_password,
        is_active=False
    )

    # Add new user
    try:
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
    except Exception:
        await db.rollback()
        raise


async def get_user_by_username(db: AsyncSession, username: str):
    statement = select(User).where(User.username == username)
    result = await db.execute(statement)
    return result.scalar_one_or_none()


async def get_user_by_email(db: AsyncSession, email: str):
    statement = select(User).where(User.email == email)
    result = await db.execute(statement)
    return result.scalar_one_or_none()


async def get_user_by_email_or_username(db: AsyncSession, email: str, username: str):
    statement = select(User).where(
        or_(User.email == email, User.username == username))
    result = await db.execute(statement)
    return result.scalar_one_or_none()


async def get_user_by_id(db: AsyncSession, id: int):
    statement = select(User).where(
        or_(User.id == id))
    result = await db.execute(statement)
    return result.scalar_one_or_none()


async def activate_user(db: AsyncSession, user_id: int):
    statement = (update(User).where(User.id == user_id).values(is_active=True))
    await db.execute(statement)
    await db.commit()


async def deactivate_user(db: AsyncSession, user_id: int):
    statement = (update(User).where(
        User.id == user_id).values(is_active=False))
    await db.execute(statement)
    await db.commit()


async def update_user_password(db: AsyncSession, user_id: int, new_hashed_password: str):
    statement = (update(User).where(
        User.id == user_id).values(hashed_password=new_hashed_password))
    await db.execute(statement)
    await db.commit()
