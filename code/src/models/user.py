# ========================================
# PAQUETES EL CLUB v3.1 - Modelo de Usuario
# ========================================

from sqlalchemy import Column, String, Boolean, Enum, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

from .base import BaseModel
from ..database.database import Base
from ..utils.datetime_utils import get_colombia_now
from ..config import settings

class UserRole(str, enum.Enum):
    """Roles de usuario del sistema"""
    ADMIN = "admin"
    OPERATOR = "operator"

class User(BaseModel, Base):
    """Modelo de usuario del sistema"""
    __tablename__ = "users"
    
    # Información básica
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    full_name = Column(String(100), nullable=False)
    
    # Autenticación
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    
    # Rol y permisos
    role = Column(Enum(UserRole), default=UserRole.OPERATOR, nullable=False)
    
    # Información adicional
    phone = Column(String(20), nullable=True)
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=get_colombia_now, nullable=False)
    updated_at = Column(DateTime, default=get_colombia_now, onupdate=get_colombia_now, nullable=False)
    
    # Relaciones
    announcements = relationship("PackageAnnouncement", back_populates="created_by")
    packages = relationship("Package", back_populates="created_by")
    password_reset_tokens = relationship("PasswordResetToken", back_populates="user")
    files = relationship("File", back_populates="uploaded_by_user")
    notifications = relationship("Notification", back_populates="user")
    messages = relationship("Message", back_populates="sender")
    
    def __repr__(self):
        return f"<User {self.username} - {self.role}>"
    
    @property
    def is_admin(self):
        """Verifica si el usuario es administrador"""
        return self.role == UserRole.ADMIN
    
    @property
    def is_operator(self):
        """Verifica si el usuario es operador"""
        return self.role == UserRole.OPERATOR
    
    def can_manage_users(self):
        """Verifica si el usuario puede gestionar otros usuarios"""
        return self.is_admin
    
    def can_view_all_packages(self):
        """Verifica si el usuario puede ver todos los paquetes"""
        return self.is_admin or self.is_operator
    
    def __repr__(self):
        return f"<User {self.username} - {self.role}>"
    
    @property
    def is_admin(self):
        """Verifica si el usuario es administrador"""
        return self.role == UserRole.ADMIN
    
    @property
    def is_operator(self):
        """Verifica si el usuario es operador"""
        return self.role == UserRole.OPERATOR
    
    def can_manage_users(self):
        """Verifica si el usuario puede gestionar otros usuarios"""
        return self.is_admin
    
    def can_view_all_packages(self):
        """Verifica si el usuario puede ver todos los paquetes"""
        return self.is_admin or self.is_operator
