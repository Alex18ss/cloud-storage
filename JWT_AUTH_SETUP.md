# JWT auth changes

## Что добавлено

- JWT access token на backend.
- Эндпоинт `GET /auth/me` для получения текущего пользователя.
- Эндпоинт `POST /auth/token` для Swagger / OAuth2 password flow.
- Защита файловых эндпоинтов через `Authorization: Bearer <token>`.
- Фронтенд теперь сохраняет реальный JWT вместо временного `temp-session-*`.

## Новые переменные окружения

Добавь в `.env`:

```env
SECRET_KEY=change-me-to-a-long-random-string
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

## Основные backend-эндпоинты

### Регистрация
`POST /auth/register`

```json
{
  "username": "ivan",
  "email": "ivan@example.com",
  "password": "secret123"
}
```

Ответ:

```json
{
  "access_token": "...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "ivan@example.com",
    "username": "ivan",
    "is_active": true,
    "created_at": "2026-04-01T12:00:00Z"
  }
}
```

### Логин
`POST /auth/login`

```json
{
  "email": "ivan@example.com",
  "password": "secret123"
}
```

### Текущий пользователь
`GET /auth/me`

Заголовок:

```http
Authorization: Bearer <access_token>
```

## Что изменилось в файловых ручках

Теперь эти ручки требуют JWT:

- `POST /files/upload`
- `GET /files/`
- `GET /files/user/{user_id}`
- `GET /files/{file_id}`
- `DELETE /files/{file_id}`
- `GET /files/download/{file_id}`

Пользователь теперь может работать только со своими файлами.
