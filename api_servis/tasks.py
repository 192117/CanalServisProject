import urllib.parse
from datetime import date

import requests

from api_servis.celery import app
from api_servis.models import Order
from api_servis.utils import get_data_spreadsheet, insert_update_db
from CanalServisProject.settings import TELEGRAM_CHANNEL, TELEGRAM_TOKEN


@app.task
def parse_google_sheets():
    '''
        Автоматическая таска, которая каждую минуту получает данные из Google Sheets с помощью функции
        get_data_spreadsheet и обновляет/удаляет/создает записи в БД с помощью функции insert_update_db.

    :return: None
    '''
    insert_update_db(get_data_spreadsheet())


@app.task
def check_date_delivery_task():
    '''
        Автоматическая таска, которая каждый день в 9:15 просматривает данные в БД на условие просрочки срока поставки и
        отправляет номер заказа и срок поставки на https://api.telegram.org/ .
    :return: None
    '''
    bot_url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={TELEGRAM_CHANNEL}&text='
    now = date.today()
    data = {}
    list_overdue_date_delivery = Order.objects.filter(date_delivery__lte=now)
    for value in list_overdue_date_delivery:
        data.setdefault(value.invoice_number, value.date_delivery)
    message = '\n'.join(
        [f'Поставка с № заказ: {key} и сроком поставки: {value} просрочена!' for key, value in data.items()]
    )
    encoded_text = urllib.parse.quote_plus(message)
    requests.get(bot_url+f'{encoded_text}')
