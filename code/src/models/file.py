# ========================================
# PAQUETES EL CLUB v3.0 - Modelo de Archivos
# ========================================

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime

from .base import BaseModel
from ..database.database import Base
from ..config import settings

class File(BaseModel, Base):
    """Modelo de archivos subidos"""
    __tablename__ = "files"
    
    if settings.database_url.startswith("sqlite"):
        package_id = Column(String(36), ForeignKey("packages.id"), nullable=True)
        uploaded_by_user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    else:
        package_id = Column(UUID(as_uuid=True), ForeignKey("packages.id"), nullable=True)
        uploaded_by_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=False)
    mime_type = Column(String(100), nullable=False)
    upload_date = Column(DateTime, default=datetime.now)
    
    # Relaciones
    package = relationship("Package", back_populates="files")
    uploaded_by_user = relationship("User", back_populates="files")
    
    def __repr__(self):
        return f"<File {self.filename} - {self.file_size} bytes>"
