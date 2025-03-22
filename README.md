### README.md

```markdown
API для Yatube

Описание

Этот проект представляет собой API для блога, в котором пользователи
могут создавать посты, подписываться друг на друга, оставлять
комментарии и объединяться в группы. API реализовано с использованием
Django REST Framework и Djoser для аутентификации.

Основные функции:
- Создание и управление постами (текст, изображения,
дата публикации, автор)
- Комментирование постов
- Подписка на авторов
- Группы для объединения пользователей
- Аутентификация через JWT-токены
```
Установка

### 1. Клонирование репозитория:
```sh
git clone https://github.com/Awesome-autumn-weirdo/api_final_yatube.git
```

### 2. Создание и активация виртуального окружения:
```sh
python3 -m venv venv # Для Linux и MacOS
python -m venv venv # Для Windows
source venv/bin/activate  # Для Linux и MacOS
source venv/Scripts/activate  # Для Windows
```

### 3. Установка зависимостей:
```sh
pip install -r requirements.txt
```

### 4. Применение миграций и запуск сервера:
```sh
python manage.py migrate
python manage.py runserver
```

### 5. Создание суперпользователя (по желанию):
```sh
python manage.py createsuperuser
```

## Примеры запросов

### 1. Получение списка постов:
```http
GET /api/v1/posts/
```
Ответ:
```json
[
    {
        "id": 1,
        "author": "user123",
        "text": "Первый пост!",
        "pub_date": "2025-03-22T12:34:56Z",
        "image": null,
        "group": null
    }
]
```

### 2. Создание поста (авторизация требуется):
```http
POST /api/v1/posts/
Content-Type: application/json
Authorization: Bearer <your_token>
```
Тело запроса:
```json
{
    "text": "Новый пост!",
    "group": 1
}
```

### 3. Получение списка комментариев к посту:
```http
GET /api/v1/posts/1/comments/
```

### 4. Подписка на пользователя:
```http
POST /api/v1/follow/
Content-Type: application/json
Authorization: Bearer <your_token>
```
Тело запроса:
```json
{
    "following": "user456"
}
```

### 5. Получение токена для авторизации:
```http
POST /api/token/
```
Тело запроса:
```json
{
    "username": "user123",
    "password": "yourpassword"
}
```
Ответ:
```json
{
    "access": "your_access_token",
    "refresh": "your_refresh_token"
}
```

## Технологии
- Django REST Framework
- Djoser (JWT-аутентификация)
- SQLite (по умолчанию) или PostgreSQL

## Лицензия
Проект распространяется под лицензией MIT.
