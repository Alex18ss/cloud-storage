# ☁️ Cloud Storage API

Облачное хранилище файлов с REST API, поддержкой S3 (MinIO) и JWT аутентификацией.

## 📋 О проекте

Проект представляет собой бэкенд для облачного хранилища файлов. Пользователи могут:
- Регистрироваться и входить в систему
- Загружать, скачивать и удалять файлы
- Получать статистику по файлам

### 🛠 Технологии

| Компонент | Технология |
|-----------|------------|
| **API** | FastAPI |
| **База данных** | PostgreSQL |
| **Хранилище файлов** | MinIO (S3-совместимое) |
| **Аутентификация** | JWT + bcrypt |
| **Контейнеризация** | Docker + Docker Compose |
| **Валидация** | Pydantic |
| **ORM** | SQLAlchemy |

### 📁 Структура проекта
```
cloud-storage/
├── api/
│   ├── __init__.py
│   ├── auth.py
│   └── file_downloader.py
├── core/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   └── security.py
├── models/
│   ├── __init__.py
│   ├── user.py
│   └── file.py
├── schemas/
│   ├── __init__.py
│   ├── user_pydantic.py
│   └── file_pydantic.py
├── services/
│   ├── __init__.py
│   └── s3_service.py
├── .env
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```


## 🚀 Быстрый старт

### 1. Клонирование репозитория

```bash
git clone https://github.com/yourusername/cloud-storage.git
cd cloud-storage
```
### 2. Настройка окружения
Создай файл .env:
# PostgreSQL
```
POSTGRES_DB=cloudstorage
POSTGRES_USER=admin
POSTGRES_PASSWORD=your_password
```

# MinIO
```
MINIO_ROOT_USER=minio-admin
MINIO_ROOT_PASSWORD=your_minio_password
MINIO_ENDPOINT=minio:9000
MINIO_BUCKET=cloud-storage
```

# JWT
```
SECRET_KEY=your_super_secret_key
```
### 3. ЗАпуск через докер
```bash
docker compose up -d --build
```

### 4. Проверка работы
API документация: http://localhost:8000/docs

MinIO Console: http://localhost:9001 (логин: minio-admin)

Health check: http://localhost:8000/health

📚 API Эндпоинты

🔐 Аутентификация
```
Метод	Эндпоинт	Описание
POST	/auth/register	Регистрация нового пользователя
POST	/auth/login	Вход в систему (возвращает JWT токен)
GET	/auth/me	Получить информацию о текущем пользователе
PUT	/auth/change-password	Смена пароля
```
📁 Файлы
```
Метод	Эндпоинт	Описание
POST	/files/upload	Загрузить файл (требует JWT)
GET	/files/	Получить список всех файлов
GET	/files/user/{user_id}	Получить файлы пользователя
GET	/files/{file_id}	Информация о файле
GET	/files/download/{file_id}	Скачать файл
DELETE	/files/{file_id}	Удалить файл
```
