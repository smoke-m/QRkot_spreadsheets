from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import DonatsInProjs


class CRUDDonatsInProjs(CRUDBase):
    async def get_info_donat(
            self,
            donation_id: int,
            session: AsyncSession,
    ) -> list:
        info_list = await session.execute(
            select([
                DonatsInProjs.ivisted,
                # DonatsInProjs.charityproject,
                DonatsInProjs.donation,
            ]).where(DonatsInProjs.donation_id == donation_id)
        )
        return info_list.all()


donats_in_projs_crud = CRUDDonatsInProjs(DonatsInProjs)
