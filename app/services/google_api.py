from datetime import datetime

from aiogoogle import Aiogoogle

from app.api.validators import check_range
from app.core.config import (DT_FORMAT, INDEX_SORT, SHEET_COLUM_COUNT,
                             SHEET_ID, SHEET_RANGE, SHEET_ROW_COUNT,
                             SHEET_TITLE, settings)


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    now_date_time = datetime.now().strftime(DT_FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = {
        'properties': {'title': f'Отчёт от {now_date_time}',
                       'locale': 'ru_RU'},
        'sheets': [
            {'properties': {'sheetType': 'GRID',
                            'sheetId': SHEET_ID,
                            'title': SHEET_TITLE,
                            'gridProperties': {
                                'rowCount': SHEET_ROW_COUNT,
                                'columnCount': SHEET_COLUM_COUNT
                            }}}
        ]
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheetid = response['spreadsheetId']
    return spreadsheetid


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
    now_date_time = datetime.now().strftime(DT_FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')

    table_values = [
        ['Отчёт от', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]

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

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }

    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range=SHEET_RANGE.format(rows, colums),
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
    print(f'https://docs.google.com/spreadsheets/d/{spreadsheetid}')
