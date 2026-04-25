from pydantic import BaseModel, EmailStr, Field, field_validator


class Token(BaseModel):
    access_token: str
    refresh_token: str


class LoginUser(BaseModel):
    email: EmailStr
    password: str


class VerifyEmail(BaseModel):
    token: str
    email: EmailStr


class ResendVerificationMail(BaseModel):
    email: EmailStr


class ForgotPassword(BaseModel):
    email: EmailStr


class ResetPassword(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8, max_length=128,
                              example="P@$$w0rd123")

    @field_validator("new_password")
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
