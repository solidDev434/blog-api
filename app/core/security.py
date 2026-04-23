import jwt
from datetime import timedelta, datetime, timezone
from pwdlib import PasswordHash

from .settings import settings


password_hash = PasswordHash.recommended()
algorithm = "HS256"


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a password against it's hash"""
    return password_hash.verify(password, hashed_password)


def hash_password(password: str):
    """Generate a hash for a possword"""
    return password_hash.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT.SECRET_KEY, algorithm=algorithm)

    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=60 * 24 * 7)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_REFRESH_KEY, algorithm=algorithm)

    return encoded_jwt
