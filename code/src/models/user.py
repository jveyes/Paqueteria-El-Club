# ========================================
# PAQUETES EL CLUB v3.0 - Modelo de Usuario
# ========================================

from sqlalchemy import Column, String, Boolean, DateTime, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum
from datetime import datetime

from .base import BaseModel
from ..database.database import Base

class UserRole(str, enum.Enum):
    """Roles de usuario"""
    ADMIN = "admin"
    OPERATOR = "operator"
    USER = "user"

class User(BaseModel, Base):
    """Modelo de usuario"""
    __tablename__ = "users"
    
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    phone = Column(String(20), nullable=True)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(UserRole), default=UserRole.USER)
    permissions = Column(JSON, default=dict)
    last_login = Column(DateTime, nullable=True)
    
    # Relaciones
    notifications = relationship("Notification", back_populates="user")
    messages = relationship("Message", back_populates="sender")
    files = relationship("File", back_populates="uploaded_by_user")
    
    def __repr__(self):
        return f"<User {self.username}>"
