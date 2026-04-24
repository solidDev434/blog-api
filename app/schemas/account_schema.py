from pydantic import BaseModel, EmailStr, Field, field_validator

from .user_schema import (
    UserRead,
    UserCreate,
    UserRole
)


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class SignupDto(BaseModel):
    email: EmailStr
    role: UserRole = Field(..., examples=[UserRole.READER])
    username: str = Field(..., min_length=5)
    password: str = Field(..., min_length=8,
                          description="Password must be at least 8 characters long")

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
