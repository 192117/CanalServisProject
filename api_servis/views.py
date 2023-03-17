from django.shortcuts import render
from django.views.decorators.http import require_GET

from .models import Order


@require_GET
def analytics(request):
    '''
        Возвращает шаблон с данными о заказах для анализа.

    :param request: Принимает GET запрос, возвращает шаблон с данными.
    :return: Шаблон 'analytics.html'
    '''
    orders = Order.objects.all().order_by('order_number')
    data = {}
    for order in orders:
        if order.date_delivery in data:
            data[order.date_delivery] += order.price
        else:
            data.setdefault(order.date_delivery, order.price)
    total_cost = sum(data.values())
    data = dict(sorted(data.items(), key=lambda x: x[0]))
    dates = list(map(str, data.keys()))
    costs = [str(i.amount) for i in data.values()]
    return render(request, 'analytics.html', context={'orders': orders[:15], 'total_cost': total_cost,
                                                      'dates': dates, 'costs': costs})
