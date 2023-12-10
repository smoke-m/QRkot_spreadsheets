from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = 'deaful'
    app_description: str = 'deaful'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()

MIN_ANYSTR_LENGTH = 1
MAX_NAME_LENGTH = 100
INVISTED_AMOUNT_DEAFUL = 0
