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
    ```
    ```bash
    cd yatube_api
    ```

2. Создать и активировать виртуальное окружение:

    ```bash
    python -m venv env
    ```
    ```bash
    source env/bin/activate  # Linux
    source env/scripts/activate  # Windows
    ```

3. Установить зависимости:

    ```bash
    python -m pip install --upgrade pip
    ```
    ```bash
    pip install -r requirements.txt
    ```

4. Выполнить миграции:

    ```bash
    python manage.py migrate
    ```

5. Запустить проект:

    ```bash
    python manage.py runserver
    ```

## Использование

После запуска сервера, API будет доступен по адресу `http://127.0.0.1:8000/api/v1/`. Можно использовать инструменты, такие как Postman, для взаимодействия с API.

## Примеры запросов

### Получение списка постов

```bash
GET http://127.0.0.1:8000/api/v1/posts/
```
Успешный ответ:
```json
{
  "count": 123,
  "next": "http://api.example.org/accounts/?offset=400&limit=100",
  "previous": "http://api.example.org/accounts/?offset=200&limit=100",
  "results": [
    {
      "id": 0,
      "author": "string",
      "text": "string",
      "pub_date": "2021-10-14T20:41:29.648Z",
      "image": "string",
      "group": 0
    }
  ]
}
```

### Создание нового поста
```bash
POST http://127.0.0.1:8000/api/v1/posts/
```
Успешный ответ:
```json
{
  "id": 0,
  "author": "string",
  "text": "string",
  "pub_date": "2025-03-14T15:26:43.223Z",
  "image": "string",
  "group": 0
}
```

### Получение списка комментариев
```bash
GET http://127.0.0.1:8000/api/v1/posts/1/comments/
```
Успешный ответ:
```json
[
  {
    "id": 0,
    "author": "string",
    "text": "string",
    "created": "2025-03-14T15:28:00.860Z",
    "post": 0
  }
]
```

### Создание нового комментария
```bash
POST http://127.0.0.1:8000/api/v1/posts/1/comments/
```
Успешный ответ:
```json
{
  "id": 0,
  "author": "string",
  "text": "string",
  "created": "2025-03-14T15:28:00.869Z",
  "post": 0
}
```

### Авторизация
Для авторизации используется JWT (JSON Web Token). Получить токен можно, отправив POST-запрос на /api/v1/jwt/create/ с данными пользователя.
```bash
POST http://127.0.0.1:8000/api/v1/jwt/create/
```
Успешный ответ:
```json
{
  "refresh": "string",
  "access": "string"
}
```

## Автор  
[Андрей Головушкин / Andrey Golovushkin](https://github.com/Frenky19)