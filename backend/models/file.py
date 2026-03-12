from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from core.database import Base
from datetime import datetime, timezone
from sqlalchemy.orm import relationship


class File(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    s3_key = Column(String(500), unique=True, nullable=False)
    file_size = Column(Integer, nullable=False)
    file_type = Column(String(100))
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    owner = relationship("User", back_populates="files")