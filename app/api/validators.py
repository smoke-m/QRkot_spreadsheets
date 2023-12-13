from typing import Tuple

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import SHEET_COLUM_COUNT, SHEET_ROW_COUNT
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


async def check_range(table_values: list) -> Tuple[int, int]:
    rows = len(table_values)
    colums = max(len(row) for row in table_values)
    if rows > SHEET_ROW_COUNT or colums > SHEET_COLUM_COUNT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f'Таблица: {SHEET_ROW_COUNT} строк, '
                f'{SHEET_COLUM_COUNT} столбцов. '
                f'Переданно {rows} строк, {colums} столбцов.'
            ),
        )
    return rows, colums
