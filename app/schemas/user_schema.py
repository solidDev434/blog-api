from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator
from app.models.user_model import UserRole


class UserBase(BaseModel):
    email: EmailStr = Field(..., example="john.doc@example.com")
    username: str = Field(..., min_length=3, max_length=50, example="johndoe")
    full_name: str | None = Field(None, max_length=100, example="John Doe")
    avatar_url: str | None = None

    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    role: UserRole = Field(default=UserRole.READER, example="reader")


class UserCreateWithoutHash(UserCreate):
    password: str = Field(..., min_length=8, max_length=128,
                          example="P@$$w0rd123")

    @field_validator("role")
    def validate_role(cls, v):
        allowed_roles = {UserRole.AUTHOR, UserRole.READER}

        if v not in allowed_roles:
            raise ValueError(f"Role '{v}' is not allowed for sign-up")
        return v

    @field_validator("password")
    def validate_password(cls, v):
        if not any(char.isupper() for char in v):
            raise ValueError(
                "Password must contain at least one uppercase letter")
        if not any(char.islower() for char in v):
            raise ValueError(
                'Password must contain at least one lowercase letter')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        if not any(char in "!@#$%^&*()-_=+[]{}|;:,.<>?/" for char in v):
            raise ValueError(
                'Password must contain at least one special character')
        return v


class UserCreateWithHash(UserCreate):
    hashed_password: str = Field(...)


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: UserRole
    is_active: bool


class CurrentUserResponse(BaseModel):
    user: UserResponse
    token: str
