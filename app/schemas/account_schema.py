from pydantic import BaseModel

from .user_schema import (
    UserRead,
    UserCreate,
    UserRole
)


class Token(BaseModel):
    access_token: str
    token_type: str
