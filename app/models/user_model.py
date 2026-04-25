from sqlmodel import SQLModel, Field
from app.schemas.user_schema import UserRole
from datetime import datetime, timezone


class User(SQLModel, table=True):
    __tablename__ = "users"
    id: int | None = Field(default=None, unique=True, primary_key=True)
    email: str = Field(unique=True, index=True)
    username: str = Field(unique=True, index=True)
    full_name: str | None = Field(None)
    avatar_url: str | None = Field(None)
    hashed_password: str = Field(...)

    role: UserRole = Field(default=UserRole.READER)
    is_active: bool = Field(default=False)

    created_at: datetime = Field(
        default_factory=lambda: datetime.now())
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now())

    def __repr__(self) -> str:
        return f"User(id={self.id}, email={self.email}, username={self.username})"
