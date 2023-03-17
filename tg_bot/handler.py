import os

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from .models import BotUser

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CanalServisProject.settings")


token = os.environ.get('TELEGRAM_TOKEN')

bot = Bot(token=token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_start(message: types.Message):
    user = BotUser.objects.create(user_chat_id=message.chat.id)
    await message.answer("Привет! Я сохраню тебя в базе данных для отправки уведомлений по статусам поставки.")


@dp.message_handler(commands=['stop'])
async def send_stop(message: types.Message):
    user = BotUser.objects.filter(user_chat_id=message.chat.id).update(active=False)
    await message.answer("Я отключил тебя от уведомлений по статусам поставки.")


async def send_notification(message: str):
    users = BotUser.objects.filter(active=True)
    for user in users:
        await bot.send_message(chat_id=user.user_chat_id, text=message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
