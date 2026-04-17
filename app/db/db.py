from sqlmodel import SQLModel, create_engine
from ..core.settings import settings

DATABASE_URL = settings.DATABASE_URL
engine = create_engine(DATABASE_URL, echo=True)
