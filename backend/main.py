from fastapi import FastAPI
from api import auth, file_downloader  # импортируем оба роутера
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(title="Cloud Storage API")
#запросы с фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React dev server
        "http://localhost:8080",  # Nginx
        "http://localhost:5173",  # Vite
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(auth.router)
app.include_router(file_downloader.router)

@app.get("/")
def root():
    return {"message": "Backend is working!"}