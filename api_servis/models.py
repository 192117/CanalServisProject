from django.db import models
from djmoney.models.fields import MoneyField


class Order(models.Model):

    order_number = models.PositiveIntegerField(
        verbose_name='Порядковый номер заказа из Google Sheets',
        help_text='Введите порядковый номер заказа из Google Sheets',
    )
    invoice_number = models.PositiveIntegerField(
        verbose_name='Номер накладной из Google Sheets',
        help_text='Введите номер накладной из Google Sheets',
        unique=True,
    )
    price = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency='RUB',
        verbose_name='Итоговая стоимость заказа',
        help_text='Введите итоговая стоимость заказа',
    )
    date_delivery = models.DateField(
        verbose_name='Год выпуска',
        help_text='Введите год выпуска альбома',
    )

    def __str__(self):
        return f'{self.order_number} - {self.invoice_number} - {self.date_delivery}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
