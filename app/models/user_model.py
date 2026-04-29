from sqlmodel import SQLModel, Field
from app.schemas.user_schema import UserRole
from datetime import datetime


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
    is_verified: bool = Field(default=False)

    email_verified_at: datetime | None = Field(default=None, nullable=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now())
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now())
    last_login_at: datetime | None = Field(default=None, nullable=True)

    # Relationships
    author_profile: Optional["AuthorProfile"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"cascade": "all, delete-orphan"})

    def __repr__(self) -> str:
        return f"User(id={self.id}, email={self.email}, username={self.username})"
