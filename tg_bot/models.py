from django.db import models


class BotUser(models.Model):

    user_chat_id = models.IntegerField(
        verbose_name='ID пользовател бота в Телеграм',
        help_text='Введите ID пользовател бота в Телеграм',
    )
    active = models.BooleanField(
        verbose_name='Подписан ли пользователь на обновления',
        help_text='Выберите активен ли пользователь для уведомлений или нет',
        default=True
    )

    def __str__(self):
        return f'{self.telegram_user_id} - {self.active}'

    class Meta:
        verbose_name = 'Пользователь БОТА'
        verbose_name_plural = 'Пользователи БОТА'
