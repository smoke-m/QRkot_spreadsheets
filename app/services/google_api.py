from copy import deepcopy
from datetime import datetime as dt

from aiogoogle import Aiogoogle

from app.api.validators import check_range
from app.core.config import (DT_FORMAT, INDEX_SORT, SHEET_BODY, SHEET_RANGE,
                             TABLE_VALUES, settings)


async def spreadsheets_create(
        wrapper_services: Aiogoogle,
        sheet_body: dict = SHEET_BODY,
) -> str:
    service = await wrapper_services.discover('sheets', 'v4')

    spreadsheet_body = deepcopy(sheet_body)
    spreadsheet_body['properties']['title'] = (
        f'Отчёт от {dt.now().strftime(DT_FORMAT)}'
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

    table_values = deepcopy(TABLE_VALUES)
    table_values[0][1] = dt.now().strftime(DT_FORMAT)

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
