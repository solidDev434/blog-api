from pydantic import BaseModel, EmailStr


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
