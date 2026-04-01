from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from core.database import get_db
from models.file import File as FileModel
from models.user import User
from schemas.file_pydantic import FileResponse
from services.s3_service import S3Service
from core.security import get_current_active_user

router = APIRouter(prefix='/files', tags=['files'])

s3_service = S3Service()


@router.post('/upload', response_model=FileResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    file_content = await file.read()

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    safe_filename = f'{timestamp}_{file.filename}'
    s3_key = f'users/{current_user.id}/{safe_filename}'

    try:
        await s3_service.upload_file(
            file_data=file_content,
            key=s3_key,
            content_type=file.content_type or 'application/octet-stream',
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Failed to upload file to storage: {str(exc)}',
        ) from exc

    db_file = FileModel(
        filename=file.filename,
        s3_key=s3_key,
        file_size=len(file_content),
        file_type=file.content_type,
        user_id=current_user.id,
    )

    db.add(db_file)
    db.commit()
    db.refresh(db_file)

    return db_file


@router.get('/', response_model=List[FileResponse])
def get_my_files(
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    files = (
        db.query(FileModel)
        .filter(FileModel.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return files


@router.get('/user/{user_id}', response_model=List[FileResponse])
def get_user_files(
    user_id: int,
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not enough permissions',
        )

    files = (
        db.query(FileModel)
        .filter(FileModel.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return files


@router.get('/{file_id}', response_model=FileResponse)
def get_file(
    file_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    file = db.query(FileModel).filter(FileModel.id == file_id).first()
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='File not found',
        )

    if file.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not enough permissions',
        )

    return file


@router.delete('/{file_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_file(
    file_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    file = db.query(FileModel).filter(FileModel.id == file_id).first()
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='File not found',
        )

    if file.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not enough permissions',
        )

    s3_service.delete_file(file.s3_key)

    db.delete(file)
    db.commit()

    return None


@router.get('/download/{file_id}')
def download_file(
    file_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    file = db.query(FileModel).filter(FileModel.id == file_id).first()
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='File not found',
        )

    if file.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not enough permissions',
        )

    try:
        download_url = s3_service.get_download_url(file.s3_key, expires_in=3600)
        return {'download_url': download_url, 'filename': file.filename}
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Failed to generate download link: {str(exc)}',
        ) from exc
