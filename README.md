# pythonProject_Django

САЙТ "FLOWER DELIVERY" С ДОСТАВКОЙ ЦВЕТОВ И ПОЛУЧЕНИЕ ЗАКАЗОВ ЧЕРЕЗ TELEGRAM-БОТА 

ЦЕЛЬ ПРОЕКТА:

Создание простого веб-сайта для заказа доставки цветов с базовой интеграцией заказов через Telegram бота.

ОБЩАЯ ИНФОРМАЦИЯ О ПРОЕКТЕ:

Проект включает разработку простого веб-сайта для заказа цветов и простого Telegram бота для приема заказов.

УСТАНОВКА И НАСТРОЙКА:

Требования:

Python 3.10+;
Встроенная база данных SQLite (используется Django);
Создание файла requirements.txt после завершения проекта.

Создание файла requirements.txt:

pip freeze > requirements.txt

ЗАПУСК ПРОЕКТА:

Применить миграции базы данных:

python manage.py makemigrations;
python manage.py migrate

Создать учетную запись администратора:

python manage.py createsuperuser

Запустить сервер разработки:

python manage.py runserver

Проект будет доступен по адресу: http://127.0.0.1.8000