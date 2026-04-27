from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration settings."""
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    JWT_REFRESH_KEY: str

    SERVER_URL: str

    # Mail
    MAIL_USER: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_HOST: str
    MAIL_STARTTLS: bool
    MAIL_SSL_TLS: bool

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
