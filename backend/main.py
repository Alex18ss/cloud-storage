from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from models.user import User
from schemas.user import UserResponse

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Backend is working!"}

# 🔍 ТЕСТОВЫЙ ЭНДПОИНТ - потом удалишь!
@app.get("/test/users", response_model=list[UserResponse])
def test_users(db: Session = Depends(get_db)):
    """Проверка: возвращает всех пользователей"""
    users = db.query(User).all()
    return users