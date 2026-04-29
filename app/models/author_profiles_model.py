from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime


class AuthorProfile(SQLModel, table=True):
    __tablename__ = "author_profiles"
    id: int | None = Field(default=None, unique=True, primary_key=True)
    user_id: int = Field(
        foreign_key="users.id",
        unique=True,
        ondelete="CASCADE"
    )

    pen_name: Optional[str] = Field(default=None, max_length=100)
    website: Optional[str] = Field(default=None, max_length=500)
    twitter_handle: Optional[str] = Field(default=None, max_length=50)
    linkedin_url: Optional[str] = Field(default=None, max_length=500)
    posts_count: int = Field(default=0)
    is_featured: bool = Field(default=False)

    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: datetime = Field(default_factory=lambda: datetime.now())

    # Relationships
    user: Optional["AuthorProfile"] = Relationship(
        back_populates="author_profile")

    def __repr__(self) -> str:
        return f"AuthorProfile(user_id={self.user_id} pen_name={self.pen_name!r})"
