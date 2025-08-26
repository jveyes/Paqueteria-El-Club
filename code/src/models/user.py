# ========================================
# PAQUETES EL CLUB v3.0 - Modelo de Usuario
# ========================================

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
import uuid
import enum

from ..database.database import Base

class UserRole(str, enum.Enum):
    """Roles de usuario disponibles"""
    ADMIN = "ADMIN"
    OPERATOR = "OPERATOR"
    USER = "USER"

class User(Base):
    """Modelo de usuario del sistema"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relaciones
    notifications = relationship("Notification", back_populates="user")
    messages = relationship("Message", back_populates="sender")
    files = relationship("File", back_populates="uploaded_by_user")
    
    def __repr__(self):
        return f"<User {self.username}>"

class PasswordResetToken(Base):
    """Modelo para tokens de restablecimiento de contraseña"""
    __tablename__ = "password_reset_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(255), unique=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    used = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relación con el usuario
    user = relationship("User", backref="password_reset_tokens")
    
    def is_expired(self) -> bool:
        """Verificar si el token ha expirado"""
        return datetime.utcnow() > self.expires_at
    
    def is_valid(self) -> bool:
        """Verificar si el token es válido (no expirado y no usado)"""
        return not self.is_expired() and not self.used
