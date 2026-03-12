from pydantic_settings import BaseSettings
"""
BaseSettings — класс из библиотеки pydantic-settings, 
который умеет читать настройки из .env файла и 
переменных окружения
"""
from functools import lru_cache
"""
lru_cache — декоратор из стандартной библиотеки Python
для кеширования результатов функции 
(чтобы не создавать объект настроек каждый раз заново)
"""

class Settings(BaseSettings):
    # Эти переменные автоматически подхватятся из .env
    # База данных
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    # MinIO
    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: str
    MINIO_ENDPOINT: str = "minio:9000"
    MINIO_BUCKET: str = "cloud-storage"

    """
    наследуется от BaseSettings — получает возможность чтения из .env
    каждая переменная — это обязательное поле, которое будет прочитано из .env
    если после : указано значение (как = "minio:9000"), это значение по умолчанию
    """

    # Собираем строку подключения
    @property
    def DATABASE_URL(self) -> str:
        """Строка подключения к PostgreSQL"""
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@db:5432/{self.POSTGRES_DB}"

    @property
    def MINIO_URL(self) -> str:
        """Полный URL для подключения к MinIO"""
        return f"http://{self.MINIO_ENDPOINT}"

    """
    @property — делает метод доступным как атрибут (без скобок)
    Эти методы вычисляют значения на основе других переменных
    DATABASE_URL собирает строку подключения из частей
    MINIO_URL добавляет протокол к эндпоинту
"""

    class Config:
        env_file = ".env"
        case_sensitive = False
    """
    env_file = ".env" — берет переменные из файла .env
    case_sensitive = False — имена переменных регистронезависимы (POSTGRES_DB = postgres_db)
    """


@lru_cache()
def get_settings():
    return Settings()