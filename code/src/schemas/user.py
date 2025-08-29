# ========================================
# PAQUETES EL CLUB v3.1 - Schemas de Usuario
# ========================================

from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime
from uuid import UUID
import enum

from .base import BaseSchemaWithTimestamps

class UserRole(str, enum.Enum):
    """Roles de usuario del sistema"""
    ADMIN = "admin"
    OPERATOR = "operator"

class UserBase(BaseModel):
    """Schema base para usuarios"""
    username: str
    email: EmailStr
    full_name: str
    phone: Optional[str] = None
    notes: Optional[str] = None
    role: UserRole = UserRole.OPERATOR
    is_active: bool = True

class UserCreate(UserBase):
    """Schema para crear usuario"""
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('La contraseña debe tener al menos 8 caracteres')
        return v
    
    @validator('username')
    def validate_username(cls, v):
        if len(v) < 3:
            raise ValueError('El nombre de usuario debe tener al menos 3 caracteres')
        if not v.isalnum():
            raise ValueError('El nombre de usuario solo puede contener letras y números')
        return v.lower()

class UserUpdate(BaseModel):
    """Schema para actualizar usuario"""
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    notes: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    
    @validator('username')
    def validate_username(cls, v):
        if v is not None:
            if len(v) < 3:
                raise ValueError('El nombre de usuario debe tener al menos 3 caracteres')
            if not v.isalnum():
                raise ValueError('El nombre de usuario solo puede contener letras y números')
            return v.lower()
        return v

class UserResponse(UserBase, BaseSchemaWithTimestamps):
    """Schema para respuesta de usuario"""
    id: UUID
    is_verified: bool
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    """Schema para login de usuario"""
    username: str
    password: str

class UserChangePassword(BaseModel):
    """Schema para cambio de contraseña"""
    current_password: str
    new_password: str
    
    @validator('new_password')
    def validate_new_password(cls, v):
        if len(v) < 8:
            raise ValueError('La contraseña debe tener al menos 8 caracteres')
        return v

class UserResetPassword(BaseModel):
    """Schema para restablecimiento de contraseña"""
    token: str
    new_password: str
    
    @validator('new_password')
    def validate_new_password(cls, v):
        if len(v) < 8:
            raise ValueError('La contraseña debe tener al menos 8 caracteres')
        return v

class UserRequestReset(BaseModel):
    """Schema para solicitar restablecimiento de contraseña"""
    email: EmailStr

class TokenResponse(BaseModel):
    """Schema para respuesta de token JWT"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class PasswordResetTokenResponse(BaseModel):
    """Schema para respuesta de token de restablecimiento"""
    message: str
    expires_at: datetime
