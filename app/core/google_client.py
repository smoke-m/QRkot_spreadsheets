import json

from aiogoogle import Aiogoogle
from aiogoogle.auth.creds import ServiceAccountCreds
from app.core.config import settings

SCOPES = [settings.spreadsheets, settings.drive]

cred = ServiceAccountCreds(
    scopes=SCOPES, **json.load(open(settings.credentials_file))
)


async def get_service():
    async with Aiogoogle(service_account_creds=cred) as aiogoogle:
        yield aiogoogle
