# Yatube API

REST API для социальной сети блогов с возможностью публикации постов, комментирования, подписок и управления сообществами.

## Технологии

- Python 3.9
- Django 3.2.16
- Django REST Framework 3.12.4
- Simple JWT 4.7.2
- Pillow 9.3.0+ (для работы с изображениями)

## Установка

1. Клонировать репозиторий и перейти в него в командной строке:
```bash
git clone https://github.com/frenky19/api_final_yatube.git

cd yatube_api

2. Cоздать и активировать виртуальное окружение:
python -m venv env

source env/bin/activate (Linux)
source env/scripts/activate (Windows)

3. Установить зависимости:
python -m pip install --upgrade pip

pip install -r requirements.txt

4. Выполнить миграции:
python manage.py migrate

5. Запустить проект:
python3 manage.py runserver


