from django.shortcuts import render

from .models import Order


def analytics(request):
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
