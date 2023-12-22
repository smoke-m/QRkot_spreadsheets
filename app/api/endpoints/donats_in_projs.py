from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.donation import donation_crud
from app.schemas.donats_in_projs import DonatsInProjsGet

router = APIRouter()


@router.get(
    '/{donation_id}',
    response_model=list[DonatsInProjsGet],
)
async def get_charity_projects_in_donate(
    donation_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    return await donation_crud.get_info_donat(donation_id, session)
