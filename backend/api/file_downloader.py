from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import os
from datetime import datetime

from core.database import get_db
from core.config import get_settings
from models.file import File as FileModel
from models.user import User
from schemas.file_pydantic import FileCreate, FileResponse
from services.s3_service import S3Service

router = APIRouter(prefix='/files', tags=['files'])

# Инициализация S3 сервиса
s3_service = S3Service()
settings = get_settings()


@router.post('/upload', response_model=FileResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(
        file: UploadFile = File(...),
        user_id: int = 1,  # пока нет jwt
        db: Session = Depends(get_db)
):
    """
    Загружает файл в MinIO
    """
    # Проверяем, существует ли пользователь
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Читаем содержимое файла
    file_content = await file.read()

    # Генерируем уникальный ключ для MinIO
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_filename = f"{timestamp}_{file.filename}"
    s3_key = f"users/{user_id}/{safe_filename}"

    try:
        # Загружаем в MinIO
        await s3_service.upload_file(
            file_data=file_content,
            key=s3_key,
            content_type=file.content_type or 'application/octet-stream'
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload file to storage: {str(e)}"
        )

    # Создаем запись в БД
    db_file = FileModel(
        filename=file.filename,
        s3_key=s3_key,
        file_size=len(file_content),
        file_type=file.content_type,
        user_id=user_id
    )

    db.add(db_file)
    db.commit()
    db.refresh(db_file)

    return db_file


@router.get("/", response_model=List[FileResponse])
def get_all_files(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
):
    """
    Возвращает список всех файлов с пагинацией
    """
    files = db.query(FileModel).offset(skip).limit(limit).all()
    return files


@router.get("/user/{user_id}", response_model=List[FileResponse])
def get_user_files(
        user_id: int,
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
):
    """
    Возвращает файлы конкретного пользователя
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    files = db.query(FileModel).filter(
        FileModel.user_id == user_id
    ).offset(skip).limit(limit).all()
    return files


@router.get("/{file_id}", response_model=FileResponse)
def get_file(
        file_id: int,
        db: Session = Depends(get_db)
):
    """
    Возвращает информацию о файле по ID
    """
    file = db.query(FileModel).filter(FileModel.id == file_id).first()
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    return file


@router.delete("/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_file(
        file_id: int,
        user_id: int = 1,  # временно, пока нет JWT
        db: Session = Depends(get_db)
):
    """
    Удаляет файл из MinIO и из БД
    """
    # Ищем файл
    file = db.query(FileModel).filter(FileModel.id == file_id).first()
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )

    # Проверяем права (файл принадлежит пользователю)
    if file.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    # Удаляем из MinIO
    s3_service.delete_file(file.s3_key)

    # Удаляем запись из БД
    db.delete(file)
    db.commit()

    return None  # 204 No Content


@router.get("/download/{file_id}")
def download_file(
        file_id: int,
        db: Session = Depends(get_db)
):
    """
    Возвращает подписанную ссылку для скачивания файла
    """
    file = db.query(FileModel).filter(FileModel.id == file_id).first()
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )

    # Генерируем временную ссылку для скачивания
    try:
        download_url = s3_service.get_download_url(file.s3_key, expires_in=3600)
        return {"download_url": download_url, "filename": file.filename}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate download link: {str(e)}"
        )