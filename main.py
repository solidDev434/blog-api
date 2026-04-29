import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.redis import redis_client

# Routers
from app.routers.account import router as account_router
from app.routers.user import router as user_router

# Middlewares
from app.middlewares.log_request_time import log_request_time

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    logger.info(msg="Server is starting")
    await redis_client.connect()

    yield
    # Shutdown code
    logger.error(msg="Server is shutting down...")
    await redis_client.disconnect()

app = FastAPI(
    title="Blog API",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/health", tags=["Health Check"])
async def health_check():
    return {"status": "healthy"}

# Register Routes
app.include_router(account_router)
app.include_router(user_router)

# Middlewares
app.middleware("http")(log_request_time)
