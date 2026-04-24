import jwt
from datetime import timedelta, datetime, timezone
from pwdlib import PasswordHash

from .settings import settings


password_hash = PasswordHash.recommended()
algorithm = "HS256"


class TokenError(Exception):
    """Custom base class for token errors"""
    pass


class TokenExpiredError(TokenError):
    pass


class TokenInvalidError(TokenError):
    pass


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
    return _generate_token(data, delta, settings.JWT_SECRET_KEY)


def verify_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY)
        return payload

    except jwt.ExpiredSignatureError:
        raise TokenExpiredError("Token has expired")

    except jwt.InvalidTokenError as e:
        raise TokenInvalidError(f"Invalid token {e}")
