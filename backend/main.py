from fastapi import FastAPI
from schemas.user_pudantic import UserResponse  # теперь файл называется user.py
from api.auth import router # импортируем роутер из auth.py

app = FastAPI(title="Cloud Storage API")

app.include_router(router)


@app.get("/")
def root():
    return {"message": "Backend is working!"}