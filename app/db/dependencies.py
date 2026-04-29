from fastapi import Depends
from redis.asyncio import Redis
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from .db import async_engine
from app.core.redis import redis_client
from app.services.cache_service import CacheService


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async_session = sessionmaker(
        bind=async_engine,
        expire_on_commit=False,
        class_=AsyncSession
    )

    async with async_session() as session:
        yield session


async def get_redis() -> Redis:
    return redis_client.get_client()


async def get_cache(redis: Redis = Depends(get_redis)) -> CacheService:
    return CacheService(redis)
