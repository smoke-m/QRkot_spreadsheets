from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = 'deaful'
    app_description: str = 'deaful'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    email: Optional[str] = None
    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: Optional[str] = None
    token_uri: Optional[str] = None
    auth_provider_x509_cert_url: Optional[str] = None
    client_x509_cert_url: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()

DT_FORMAT = "%Y/%m/%d %H:%M:%S"
MIN_ANYSTR_LENGTH = 1
MAX_NAME_LENGTH = 100
INVISTED_AMOUNT_DEAFUL = 0
INDEX_SORT = 1
SHEET_ID = 0
SHEET_TITLE = 'Лист1'
SHEET_ROW_COUNT = 20
SHEET_COLUM_COUNT = 5
SHEET_RANGE = 'R1C1:R{}C{}'

SHEET_BODY = dict(
    properties=dict(title='', locale='ru_RU'),
    sheets=[dict(
        properties=dict(
            sheetType='GRID',
            sheetId=SHEET_ID,
            title=SHEET_TITLE,
            gridProperties=dict(
                rowCount=SHEET_ROW_COUNT,
                columnCount=SHEET_COLUM_COUNT,
            )))])

TABLE_VALUES = [
    ['Отчёт от', ''],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]
