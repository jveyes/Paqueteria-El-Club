# ========================================
# PAQUETES EL CLUB v3.1 - Esquemas de Autenticación
# ========================================

from pydantic import BaseModel, EmailStr
from typing import Optional

class ForgotPasswordRequest(BaseModel):
    """Esquema para solicitar recuperación de contraseña"""
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    """Esquema para restablecer contraseña"""
    token: str
    new_password: str

class LoginResponse(BaseModel):
    """Esquema para respuesta de login"""
    access_token: str
    token_type: str
    user: dict

class LogoutResponse(BaseModel):
    """Esquema para respuesta de logout"""
    message: str

class AuthCheckResponse(BaseModel):
    """Esquema para verificación de autenticación"""
    is_authenticated: bool
    user_name: Optional[str] = None
