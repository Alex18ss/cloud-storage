from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=20)
    is_active: bool = True


# ✅ ИСПРАВЛЕНО: UserCreate должен наследоваться от UserBase
class UserCreate(UserBase):  # ← было BaseModel, стало UserBase
    password: str = Field(..., min_length=6)


class UserResponse(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)