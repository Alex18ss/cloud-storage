from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from api import auth, file_downloader

# Настройка OAuth2 для Swagger
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

app = FastAPI(
    title="Cloud Storage API",
    description="API для облачного хранилища файлов",
    version="1.0.0",
    swagger_ui_parameters={
        "persistAuthorization": True,  # Сохранять авторизацию после обновления страницы
        "tryItOutEnabled": True,       # Включить режим тестирования
    }
)

# Настройка CORS (разрешаем запросы с фронтенда)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",   # React dev server
        "http://localhost:8080",   # Nginx
        "http://localhost:5173",   # Vite (альтернатива)
    ],
    allow_credentials=True,
    allow_methods=["*"],           # Разрешаем все методы (GET, POST, PUT, DELETE)
    allow_headers=["*"],           # Разрешаем все заголовки
)

# Подключаем роутеры
app.include_router(auth.router)
app.include_router(file_downloader.router)


@app.get("/")
def root():
    """Корневой эндпоинт для проверки работоспособности API"""
    return {
        "message": "Backend is working!",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
def health_check():
    """Эндпоинт для проверки здоровья сервиса"""
    return {"status": "healthy"}