import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.db import init_db

# Routers
from app.routers.account import router as account_router
from app.routers.user import router as user_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    logger.info(msg="Server is starting")
    await init_db()

    yield
    # Shutdown code
    logger.error(msg="Server is shutting down...")

app = FastAPI(
    title="Blog API",
    version="1.0.0",
    lifespan=lifespan
)

# Register Routes
app.include_router(account_router)
app.include_router(user_router)
