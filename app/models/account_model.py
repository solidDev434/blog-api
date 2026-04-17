from sqlmodel import SQLModel, Field
from app.schemas.user_schema import UserRole
from datetime import datetime


class Account(SQLModel, table=True):
    __tablename__ = "account"
    id: int | None = Field(default=None, unique=True, primary_key=True)
    email: str = Field(..., unique=True, index=True)
    username: str = Field(..., unique=True, index=True)
    full_name: str | None = Field(None)
    avatar_url: str | None = Field(None)
    hashed_password: str = Field(...)
    role: str = Field(default=UserRole.READER)
    is_active: bool = Field(default=True)
    created_at: str | None = Field(default=datetime.now)
    updated_at: str | None = Field(default=datetime.now)

    def __repr__(self) -> str:
        return f"Account(id={self.id}, email={self.email}, username={self.username})"
