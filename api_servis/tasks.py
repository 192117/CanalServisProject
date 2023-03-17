from datetime import date

import requests
from django.urls import reverse

from api_servis.celery import app
from api_servis.models import Order
from api_servis.utils import get_data_spreadsheet, insert_update_db


@app.task
def parse_google_sheets():
    insert_update_db(get_data_spreadsheet())


@app.task
def check_date_delivery_task():
    now = date.today()
    list_overdue_date_delivery = Order.objects.filter(date_delivery__lte=now)
    for value in list_overdue_date_delivery:
        bot_url = reverse('bot_notifications')
        data = {
            'message': f'Поставка с № заказ: {value.invoice_number} и сроком поставки: {value.date_delivery} просрочена!'
        }
        requests.post(bot_url, data=data)
