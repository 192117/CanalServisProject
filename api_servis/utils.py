import re

import httplib2
import requests
from bs4 import BeautifulSoup
from djmoney.money import Money
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

from CanalServisProject.settings import GOOGLE_JSON, GOOGLE_SCOPES, SAMPLE_RANGE_NAME, SPREADSHEET_ID

from .models import Order


def get_rate_usd() -> float:
    '''
    Функция, которая получает курс USD к RUB из API ЦБ РФ. Возвращает курс.

    :return: Курс USD к RUB в формате float.
    '''
    url = 'https://www.cbr.ru/scripts/XML_daily.asp'
    xml = requests.get(url)
    soup = BeautifulSoup(xml.content, 'xml')
    return float(soup.find('CharCode', string='USD').find_next_sibling('Value').string.replace(',', '.'))


def get_data_spreadsheet() -> list:
    '''
    Функция, которая делает запрос к Google Sheets и получает данные в диапазоне ячеек A:D и возвращает список
    списков, сотоящие из строк Google Sheets.

    :return: Возвращает список списков, сотоящие из строк Google Sheets.
    '''
    credentials = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_JSON, GOOGLE_SCOPES)
    http_auth = credentials.authorize(httplib2.Http())
    service = build('sheets', 'v4', http=http_auth)
    result = service.spreadsheets().values().batchGet(
        spreadsheetId=SPREADSHEET_ID,
        ranges=[SAMPLE_RANGE_NAME,]
    ).execute()
    range_values_sheets = result.get('valueRanges')[0].get('values', [])
    return range_values_sheets


def insert_update_db(values: list) -> None:
    '''
    Функция, которая обновляет значения в БД, согласно полученным данным из Google Sheets. Записи в БД создаются,
    обновляются или удаляются, если их номер заказа (столбец B) отсутсовал в переданных данных values.

    :param values: Cписок списков, сотоящие из строк Google Sheets.
    :return: None
    '''
    pattern = r'(\d+).(\d+).(\d+)'
    rate = get_rate_usd()
    for value in values:
        date = re.sub(pattern, r'\3-\2-\1', value[3])
        order, created = Order.objects.update_or_create(
            order_number=int(value[0]),
            defaults={
                'invoice_number': int(value[1]),
                'price': Money(rate*int(value[2]), 'RUB'),
                'date_delivery': date
            },
        )
    order_numbers = [int(value[0]) for value in values]
    Order.objects.exclude(order_number__in=order_numbers).all().delete()
