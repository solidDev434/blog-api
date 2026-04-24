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


async def activate_user(db: AsyncSession, user_id: int):
    # statement = select(User).where(User.id == user_id)
    # user = (await db.execute(statement)).scalar_one_or_none()

    # if user:
    #     user.is_active = True
    #     user.updated_at = datetime.now()

    #     db.commit()
    #     db.refresh(user)
    #     return user

    statement = (update(User).where(User.id == user_id).values(is_active=True))
    await db.execute(statement)
    await db.commit()


async def deactivate_user(db: AsyncSession, user_id: int):
    statement = (update(User).where(
        User.id == user_id).values(is_active=False))
    await db.execute(statement)
    await db.commit()
