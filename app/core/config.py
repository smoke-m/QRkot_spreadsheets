from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = 'deaful'
    app_description: str = 'deaful'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    credentials_file: Optional[str] = None
    email: Optional[str] = None
    spreadsheets: Optional[str] = None
    drive: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()

DT_FORMAT = "%Y/%m/%d %H:%M:%S"
MIN_ANYSTR_LENGTH = 1
MAX_NAME_LENGTH = 100
INVISTED_AMOUNT_DEAFUL = 0
SHEET_ID = 0
SHEET_TITLE = 'Лист1'
SHEET_ROW_COUNT = 100
SHEET_COLUM_COUNT = 10
