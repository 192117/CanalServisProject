import re

import httplib2
import requests
from bs4 import BeautifulSoup
from djmoney.money import Money
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

from CanalServisProject.settings import GOOGLE_JSON, GOOGLE_SCOPES, SAMPLE_RANGE_NAME, SPREADSHEET_ID

from .models import Order


def get_rate_usd():
    url = 'https://www.cbr.ru/scripts/XML_daily.asp'
    xml = requests.get(url)
    soup = BeautifulSoup(xml.content, 'xml')
    return float(soup.find('CharCode', string='USD').find_next_sibling('Value').string.replace(',', '.'))


def get_data_spreadsheet():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_JSON, GOOGLE_SCOPES)
    http_auth = credentials.authorize(httplib2.Http())
    service = build('sheets', 'v4', http=http_auth)
    result = service.spreadsheets().values().batchGet(
        spreadsheetId=SPREADSHEET_ID,
        ranges=[SAMPLE_RANGE_NAME,]
    ).execute()
    return result.get('valueRanges')[0].get('values', [])


def insert_update_db(values):
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
