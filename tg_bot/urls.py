from django.urls import path

from .views import NotificationMessageView

urlpatterns = [
    path('notifications/', NotificationMessageView.as_view(), name='bot_notifications'),
]
