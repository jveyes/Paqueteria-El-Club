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
    USER = "user"

class User(BaseModel, Base):
    """Modelo de usuario del sistema"""
    __tablename__ = "users"
    
    # Información básica
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    full_name = Column(String(100), nullable=False)
    
    # Autenticación
    hashed_password = Column(String(255), nullable=True)  # Permitir nulo para usuarios sin acceso al dashboard
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Rol y permisos
    role = Column(Enum(UserRole), default=UserRole.OPERATOR, nullable=False)
    
    # Información adicional
    phone = Column(String(20), nullable=True)
    is_verified = Column(Boolean, default=True, nullable=False)
    notes = Column(Text, nullable=True)
    profile_photo = Column(String(500), nullable=True)  # Nueva columna para foto de perfil
    
    # Timestamps
    created_at = Column(DateTime, default=get_colombia_now, nullable=False)
    updated_at = Column(DateTime, default=get_colombia_now, onupdate=get_colombia_now, nullable=False)
    
    # Relaciones
    announcements = relationship("PackageAnnouncement", back_populates="created_by")
    password_reset_tokens = relationship("PasswordResetToken", back_populates="user")
    files = relationship("File", back_populates="uploaded_by_user")
    notifications = relationship("Notification", back_populates="user")
    messages = relationship("Message", foreign_keys="Message.sender_id", back_populates="sender")
    activity_logs = relationship("UserActivityLog", back_populates="user")  # Nueva relación
    
    def __repr__(self):
        return f"<User {self.username} - {self.role}>"
    
    @property
    def first_name(self):
        """Retorna el primer nombre del usuario"""
        return self.full_name.split()[0] if self.full_name else ""
    
    @property
    def last_name(self):
        """Retorna el apellido del usuario"""
        parts = self.full_name.split()
        return " ".join(parts[1:]) if len(parts) > 1 else ""
    
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
