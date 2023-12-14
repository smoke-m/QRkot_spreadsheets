from copy import deepcopy
from datetime import datetime as dt
from typing import Tuple, Union

from aiogoogle import Aiogoogle

from app.api.validators import check_range
from app.core.config import (DT_FORMAT, INDEX_SORT, SHEET_BODY, SHEET_RANGE,
                             TABLE_VALUES, settings)


def edit_array_value(
        array: Union[Tuple, list, dict],
        value: str,
        keys: Tuple,
):
    new_array = deepcopy(array)
    sub_array = new_array
    for key in keys[:-1]:
        sub_array = sub_array[key]
    sub_array[keys[-1]] = value
    return new_array


async def spreadsheets_create(
        wrapper_services: Aiogoogle,
) -> str:
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = edit_array_value(
        SHEET_BODY, f'Отчёт от {dt.now().strftime(DT_FORMAT)}',
        ('properties', 'title')
    )
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId']


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheetid: str,
        charity_projects: list,
        wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = edit_array_value(
        TABLE_VALUES, str(dt.now().strftime(DT_FORMAT)), (0, 1)
    )

    new_rows = []
    for project in charity_projects:
        new_row = [
            str(project.name),
            str(project.close_date - project.create_date),
            str(project.description)
        ]
        new_rows.append(new_row)
    new_rows.sort(key=lambda x: x[INDEX_SORT])
    table_values.extend(new_rows)

    rows, colums = await check_range(table_values)

    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range=SHEET_RANGE.format(rows, colums),
            valueInputOption='USER_ENTERED',
            json={
                'majorDimension': 'ROWS',
                'values': table_values
            }))
    print(f'https://docs.google.com/spreadsheets/d/{spreadsheetid}')
