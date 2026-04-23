from typing import AsyncGenerator
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from .db import async_engine


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async_session = sessionmaker(
        bind=async_engine,
        expire_on_commit=False,
        class_=AsyncSession
    )

    async with async_session() as session:
        yield session
