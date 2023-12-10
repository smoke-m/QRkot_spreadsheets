from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def check_name_duplicate(
        room_name: str,
        session: AsyncSession,
) -> None:
    if await charity_project_crud.get_by_attribute('name', room_name, session):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_project_exist(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Проекта не существует',
        )
    return charity_project


async def check_invested_amount(
        project_id: int,
        session: AsyncSession,
) -> None:
    charity_project = await charity_project_crud.get(project_id, session)
    if charity_project.invested_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!',
        )


async def check_invested(
        full_amount_obj: int,
        invested_amount_db: int,
        fully_invested_db: int,
) -> None:
    if fully_invested_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!',
        )
    if full_amount_obj < invested_amount_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Сумма инвистиций должна быть больше, существующей!',
        )
