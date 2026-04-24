from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class VerifyEmail(BaseModel):
    token: str
    email: EmailStr


class ResendVerificationMail(BaseModel):
    email: EmailStr
