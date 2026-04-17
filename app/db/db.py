from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import text

from app.core.settings import settings

async_engine = create_async_engine(url=settings.DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    class_=AsyncSession
)


async def init_db():
    async with AsyncSessionLocal() as conn:
        statement = text("SELECT 'hello';")
        result = await conn.execute(statement)
        print(result.scalar())
