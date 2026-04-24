from fastapi import FastAPI
from app.routers.account import router as account_router
from contextlib import asynccontextmanager
from app.db.db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    print("Server is starting")
    await init_db()

    yield
    # Shutdown code
    print("Server is shutting down...")

app = FastAPI(
    title="Blog API",
    version="1.0.0",
    lifespan=lifespan
)

# Register Routes
app.include_router(account_router)
