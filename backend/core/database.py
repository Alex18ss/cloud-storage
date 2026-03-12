import sqlalchemy as sqla
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from core.config import get_settings

settings = get_settings()

engine = sqla.create_engine(
    settings.DATABASE_URL,
    pool_size=3,
    echo=True
)
"""
pool_size=3 - временно
кол-во одновременно подключенных пользователей
"""

Base = declarative_base()
# oт этого класса будут наследоваться все модели (User, File)

SessionLocalFabric = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

"""
autocommit=False (не сохранять автоматически)
autoflush=False (не сбрасывать автоматически)
bind=engine (привязать к нашему движку)
"""

def get_db():
    """
    Создает и возвращает сессию базы данных.
    Автоматически закрывает сессию после использования.
    """
    db = SessionLocalFabric() # создали сессию
    try:
        yield db
    finally:
        db.close()