import jwt
import time
from sqlalchemy.ext.asyncio.session import AsyncSession
from jwt.exceptions import PyJWTError, ExpiredSignatureError
from typing import Annotated
from fastapi import Depends, HTTPException, status
from datetime import timedelta, datetime, timezone
from pwdlib import PasswordHash
from app.services.user_service import get_user_by_email
from fastapi.security import (
    OAuth2PasswordBearer
)

from .settings import settings
from app.db.dependencies import get_db
from app.models.user_model import User


class TokenError(Exception):
    """Custom base class for token errors"""
    pass


class TokenExpiredError(TokenError):
    pass


class TokenInvalidError(TokenError):
    pass


password_hash = PasswordHash.recommended()
algorithm = settings.JWT_ALGORITHM
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/account/login"
)


# Get Authenticated user
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY,
                             settings.JWT_ALGORITHM)
        email = payload.get("email")
        if email is None:
            raise credentials_exception

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WW-Authenticate": "Bearer"},
        )

    except PyJWTError:
        raise credentials_exception

    user = get_user_by_email(db, email)
    if user is None:
        raise credentials_exception

    return user


def require_role(required_role: str):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted"

            )
        return current_user
    return role_checker


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a password against it's hash"""
    return password_hash.verify(password, hashed_password)


def hash_password(password: str):
    """Generate a hash for a possword"""
    return password_hash.hash(password)


def _generate_token(data: dict, expires_delta: timedelta, secret_key: str) -> str:
    """Internal helper to calculate expiry and encode JWT."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta

    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode, secret_key, algorithm=algorithm)


def create_temporary_token(data: dict, minutes: int = 7) -> str:
    return _generate_token(data, timedelta(minutes=minutes), settings.JWT_SECRET_KEY)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    delta = expires_delta or timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return _generate_token(data, delta, settings.JWT_SECRET_KEY)


def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    delta = expires_delta or timedelta(days=7)
    return _generate_token(data, delta, settings.JWT_REFRESH_KEY)


def verify_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[algorithm])

        if round(time.time()) > payload["exp"]:
            raise TokenExpiredError("Token has expired")

        return payload

    except jwt.ExpiredSignatureError:
        raise TokenExpiredError("Token has expired")

    except jwt.InvalidTokenError as e:
        raise TokenInvalidError(f"Invalid token {e}")
