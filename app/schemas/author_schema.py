from pydantic import BaseModel, Field
from typing import Optional
from app.models.author_model import AuthorProfileBase


class AuthorProfileCreate(AuthorProfileBase):
    pass


class AuthorProfileUpdate(BaseModel):
    pen_name: Optional[str] = Field(default=None, max_length=100)
    website: Optional[str] = Field(default=None, max_length=500)
    twitter_handle: Optional[str] = Field(default=None, max_length=50)
    linkedin_url: Optional[str] = Field(default=None, max_length=500)


class AuthorProfileRead(AuthorProfileBase):
    id: int
