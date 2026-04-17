from fastapi import FastAPI
from app.routes.account import router as account_router
from app.core.settings import settings

app = FastAPI(
    title="Blog API",
    version="1.0.0"
)

# Register Routes
app.include_router(account_router)

print(settings.DATABASE_URL, "DATABASE_URL")
