from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    AUTHOR = "author"
    READER = "reader"


class UserBase(BaseModel):
    email: EmailStr = Field(..., example="john.doc@example.com")
    username: str = Field(..., min_length=3, max_length=50, example="johndoe")
    full_name: str | None = Field(None, max_length=100, example="John Doe")
    avatar_url: str | None = None

    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=128,
                          example="SuperSecret123:")
    role: UserRole = Field(default=UserRole.READER, example="author")


class UserRead(UserBase):
    id: int
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime | None = None
