from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_projects_time_close(
            self,
            session: AsyncSession,
    ) -> list:
        projects = await session.execute(
            select([
                CharityProject.name,
                (
                    func.julianday(CharityProject.close_date) -
                    func.julianday(CharityProject.create_date)
                ).label('time'),
                CharityProject.description
            ]).where(
                CharityProject.fully_invested
            ).order_by(
                'time'
            )
        )
        return projects.all()


charity_project_crud = CRUDCharityProject(CharityProject)
