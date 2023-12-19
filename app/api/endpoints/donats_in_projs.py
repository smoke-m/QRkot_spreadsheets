from pprint import pprint

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.donats_in_projs import donats_in_projs_crud

router = APIRouter()


@router.get(
    '/{donation_id}',
)
async def get_all_charity_projects(
    donation_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    choto = await donats_in_projs_crud.get_info_donat(donation_id, session)
    pprint(choto)
