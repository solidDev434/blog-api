from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.schemas.user_schema import (
    UserCreateWithHash,
)
from app.models.user_model import User


def create_user(db: AsyncSession, payload: UserCreateWithHash):
    # Create new user
    user = User(email=payload.email, full_name=payload.full_name,
                username=payload.username, role=payload.role, hashed_password=payload.hashed_password, is_active=False)

    # Add new user
    db.add(user)
    db.commit()
    # db.refresh(user)

    return user


def get_user_by_username(db: AsyncSession, username: str):
    statement = select(User).filter(User.username == username)
    result = db.execute(statement)
    print(result)
