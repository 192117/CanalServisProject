# Тестовое задание для КаналСервис

[Описание тестового задания.](https://github.com/192117/CanalServisProject/blob/master/Task_descriptions.mht)

## Стек:

1. Python 3.11
2. Django/DRF
3. Celery
4. Redis
5. PostgreSQL
6. Gunicorn
7. Requests
8. BS4

## Описание работы:

1. Каждую минуту таска ходит за получением данных в Google Sheets, получает данные, просматривая ячейки A:D. 
Либо обновляет данные в БД, либо создает новые записи, данные, которые отсутствуют в Google Sheets, удаляет из БД.
2. По endpoint `analytics/` выводится график динамики стоимости (дата заказа - стоимость), итоговая стоимость всех 
заказов в БД и таблица с 15 первыми записями в БД. 
3. Каждый день в 9:15 работает таска, которая проверяет просроченный заказы на текущую дату и отправляет сообщения в
[канал](https://t.me/Notifications192117) (В вашем случае может быть другой зависит от TELEGRAM_CHANNEL в .env.docker)
4. Работа с каналом осуществляется через [API](https://api.telegram.org/)

## Реализация сервера:

Пакетным менеджером в проекте является Poetry.

База данных используется PostgreSQL. Уникальным полем для БД является invoice_number соответствующая столбцу B.
Переменные окружения находятся в файле .env, которые затем подгружаются в настройки с помощью django-environ. 

Для примера смотрите файл .env.docker.example 

## Разворачивание сервера:

Для быстрого разворачивания сервера используется Docker.

Для запуска сервера создайте файл .env.docker рядом с файлом .env.docker.example и аналогичный ему.
Запустите команду docker-compose up -d.
Можете начинать обращаться по соответствующим url'ам.

## Разворачивание сервера без Dockera

Предполагается, что у Вас уже установлен python, postgresql и redis.

Для запуска сервера создайте файл .env рядом с файлом .env.docker.example и аналогичный ему.
Укажите свои параметры

1. Склонируйте себе репозиторий командой `git clone https://github.com/192117/CanalServisProject.git`
2. Установите Poetry командой `pip install poetry`
3. Перейдите в папке с проектом и выполните команду `poetry install`
4. Активируйте виртуальное окружение `poetry shell`
5. Запустите проект командой `python manage.py runserver`
6. Запустите celery командой `celery -A api_servis worker --beat --loglevel=info`
 
Можете начинать обращаться по соответствующим url'ам.

## Доступ к серверу:

[Google Sheets](https://docs.google.com/spreadsheets/d/1o2YLMwD7-J-ZiHhuH2tFmklQdMfxPaiqb3hSI7wIt4Y/edit?usp=sharing)

[Страница с аналитикой](http://5.104.108.168:8005/analytics/)

[Телеграмм канал](https://t.me/Notifications192117)
