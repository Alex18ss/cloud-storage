from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class FileBase(BaseModel):
    filename: str
    file_size: int
    file_type: Optional[str] = None


class FileCreate(FileBase):
    s3_key: str  # ключ в MinIO
    user_id: int


class FileResponse(FileBase):
    id: int
    s3_key: str
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True