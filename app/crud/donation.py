from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject, Donation, DonatsInProjs


class CRUDDonation(CRUDBase):
    @staticmethod
    async def get_info_donat(
            donation_id: int,
            session: AsyncSession,
    ) -> list:
        projects = await session.execute(
            select([
                DonatsInProjs.ivisted.label('donat'),
                CharityProject.name.label('charity_project'),
            ]).where(and_(
                # Donation.any == donation_any,
                # Donation.id == DonatsInProjs.donation_id,
                DonatsInProjs.donation_id == donation_id,
                CharityProject.id == DonatsInProjs.project_id
            )))
        return projects.all()


donation_crud = CRUDDonation(Donation)
