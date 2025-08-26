# ========================================
# PAQUETES EL CLUB v3.0 - Esquemas de Usuario
# ========================================

from pydantic import BaseModel, EmailStr
from typing import Optional
from ..models.user import UserRole
from .base import BaseSchemaWithTimestamps

class UserBase(BaseModel):
    """Esquema base de usuario"""
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    phone: Optional[str] = None
    role: UserRole = UserRole.USER

class UserCreate(UserBase):
    """Esquema para crear usuario"""
    password: str

class UserUpdate(BaseModel):
    """Esquema para actualizar usuario"""
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None

class UserResponse(BaseSchemaWithTimestamps, UserBase):
    """Esquema de respuesta de usuario"""
    is_active: bool
    last_login: Optional[str] = None

class UserLogin(BaseModel):
    """Esquema para login"""
    username: str
    password: str
