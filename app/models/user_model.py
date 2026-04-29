from sqlmodel import SQLModel, Field, Relationship
from enum import Enum
from typing import Optional
from datetime import datetime

from .author_profiles_model import AuthorProfile


class UserRole(str, Enum):
    ADMIN = "admin"
    AUTHOR = "author"
    READER = "reader"


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

    # Relationships
    author_profile: Optional["AuthorProfile"] = Relationship(
        back_populates="user", cascade_delete=True)

    def __repr__(self) -> str:
        return f"User(id={self.id}, email={self.email}, username={self.username})"
