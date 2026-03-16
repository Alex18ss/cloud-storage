#!/usr/bin/env python3
"""
Тестовый скрипт для проверки схем и моделей
Запуск: docker-compose exec backend python3 test_schemas.py
"""

from sqlalchemy import text
from core.database import SessionLocalFabric as SessionLocal
from models.user import User
from models.file import File
from schemas.user_pudantic import UserCreate, UserResponse
from schemas.file_pydantic import FileCreate, FileResponse
from core.security import get_password_hash
import sys


def check_db_connection():
    """Проверяет подключение к БД"""
    print("\n🔍 Проверка подключения к БД...")
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        print("  ✅ Подключение к БД работает")
        db.close()
        return True
    except Exception as e:
        print(f"  ❌ Ошибка подключения к БД: {e}")
        return False


def test_user_schemas():
    """Тестирует схемы пользователя и создает тестовые данные"""
    print("\n🔍 Тестирование User схем...")
    db = SessionLocal()

    try:
        # Тест UserCreate
        user_data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "secret123"
        }
        user_create = UserCreate(**user_data)
        print("  ✅ UserCreate работает")
        # ИСПРАВЛЕНО: используем правильные имена полей
        print(f"     Данные: email={user_create.email}, username={user_create.username}")

        # Проверяем, есть ли пользователь в БД
        user = db.query(User).first()
        if not user:
            print("  ⚠️ Нет пользователей в БД, создаю тестового...")
            hashed = get_password_hash("secret123")
            new_user = User(
                email="test@example.com",
                username="testuser",
                hashed_password=hashed,
                is_active=True
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            user = new_user
            print(f"  ✅ Создан пользователь: {user.email} (ID: {user.id})")

        # Тест UserResponse
        if user:
            user_response = UserResponse.model_validate(user)
            print(f"  ✅ UserResponse работает")
            print(f"     Пользователь: {user_response.email}, ID: {user_response.id}")
            return user.id
        else:
            print("  ❌ Не удалось создать пользователя")
            return None

    except Exception as e:
        print(f"  ❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        return None
    finally:
        db.close()


def test_file_schemas(user_id):
    """Тестирует схемы файлов и создает тестовые данные"""
    print("\n🔍 Тестирование File схем...")
    db = SessionLocal()

    try:
        # Тест FileCreate
        file_data = {
            "filename": "test.jpg",
            "file_size": 1024,
            "file_type": "image/jpeg",
            "s3_key": f"users/{user_id}/test.jpg",
            "user_id": user_id
        }
        file_create = FileCreate(**file_data)
        print("  ✅ FileCreate работает")
        print(f"     Данные: {file_create.filename}, size={file_create.file_size}")

        # Проверяем, есть ли файлы в БД
        file = db.query(File).first()
        if not file and user_id:
            print("  ⚠️ Нет файлов в БД, создаю тестовый...")
            new_file = File(
                filename="test_image.jpg",
                s3_key=f"users/{user_id}/test_image.jpg",
                file_size=2048,
                file_type="image/png",
                user_id=user_id
            )
            db.add(new_file)
            db.commit()
            db.refresh(new_file)
            file = new_file
            print(f"  ✅ Создан файл: {file.filename} (ID: {file.id})")

        # Тест FileResponse
        if file:
            file_response = FileResponse.model_validate(file)
            print(f"  ✅ FileResponse работает")
            print(f"     Файл: {file_response.filename}, владелец: {file_response.user_id}")
            return True
        else:
            print("  ⚠️ Файл не создан")
            return False

    except Exception as e:
        print(f"  ❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        return False
    finally:
        db.close()


def show_all_data():
    """Показывает все данные в БД"""
    print("\n📊 ТЕКУЩИЕ ДАННЫЕ В БД:")
    db = SessionLocal()
    try:
        users = db.query(User).all()
        files = db.query(File).all()

        print(f"\n👥 Пользователи ({len(users)}):")
        for user in users:
            print(f"  - ID: {user.id}, Email: {user.email}, Username: {user.username}")
            user_files = [f for f in files if f.user_id == user.id]
            if user_files:
                print(f"    Файлы: {len(user_files)}")
                for f in user_files:
                    print(f"      • {f.filename} ({f.file_size} bytes)")

        print(f"\n📁 Всего файлов: {len(files)}")

    except Exception as e:
        print(f"  ❌ Ошибка при чтении данных: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 60)
    print("🧪 ТЕСТИРОВАНИЕ СХЕМ И ДОБАВЛЕНИЕ ТЕСТОВЫХ ДАННЫХ")
    print("=" * 60)

    if check_db_connection():
        user_id = test_user_schemas()
        if user_id:
            if test_file_schemas(user_id):
                show_all_data()
                print("\n✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ! Тестовые данные добавлены в БД.")
            else:
                print("\n⚠️ ТЕСТЫ USER ПРОЙДЕНЫ, НО FILE ИМЕЮТ ПРОБЛЕМЫ")
        else:
            print("\n❌ ОШИБКА ПРИ ТЕСТИРОВАНИИ USER")
    else:
        print("\n❌ НЕТ ПОДКЛЮЧЕНИЯ К БД")

    print("=" * 60)