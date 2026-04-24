from pydantic import BaseModel, field_validator

from .user_schema import (
    UserCreateWithoutHash,
    UserRole
)


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class SignupDto(UserCreateWithoutHash):

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
