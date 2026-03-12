import sys
import os
# добавляем путь к корню backend, чтобы импорты работали
sys.path.append(os.path.dirname(__file__))

from core.database import engine, Base
from models.user import User  # noqa
from models.file import File  # noqa

# создание таблиц
Base.metadata.create_all(bind=engine)