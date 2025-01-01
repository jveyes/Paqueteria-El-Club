# ========================================
# PAQUETES EL CLUB v3.1 - Esquemas de Anuncio de Paquetes
# ========================================

from pydantic import BaseModel, validator
from typing import Optional, Union
from datetime import datetime
from uuid import UUID
from .base import BaseSchema
from ..utils.security import validate_customer_name, validate_phone_number, validate_guide_number, is_safe_input

class AnnouncementBase(BaseModel):
    """Esquema base de anuncio"""
    customer_name: str
    phone_number: str
    guide_number: str

class AnnouncementCreate(AnnouncementBase):
    """Esquema para crear anuncio"""
    @validator('customer_name')
    def validate_customer_name(cls, v):
        # Verificar si es seguro
        if not is_safe_input(v):
            raise ValueError('El nombre contiene caracteres no permitidos')
        
        # Validar y sanitizar usando la función de seguridad
        try:
            return validate_customer_name(v)
        except ValueError as e:
            raise ValueError(str(e))
    
    @validator('phone_number')
    def validate_phone_number(cls, v):
        # Verificar si es seguro
        if not is_safe_input(v):
            raise ValueError('El teléfono contiene caracteres no permitidos')
        
        # Validar y limpiar usando la función de seguridad
        try:
            return validate_phone_number(v)
        except ValueError as e:
            raise ValueError(str(e))
    
    @validator('guide_number')
    def validate_guide_number(cls, v):
        # Verificar si es seguro
        if not is_safe_input(v):
            raise ValueError('El número de guía contiene caracteres no permitidos')
        
        # Validar y limpiar usando la función de seguridad
        try:
            return validate_guide_number(v)
        except ValueError as e:
            raise ValueError(str(e))

class AnnouncementUpdate(BaseModel):
    """Esquema para actualizar anuncio"""
    customer_name: Optional[str] = None
    phone_number: Optional[str] = None
    guide_number: Optional[str] = None
    tracking_code: Optional[str] = None
    is_active: Optional[bool] = None
    is_processed: Optional[bool] = None
    
    @validator('customer_name')
    def validate_customer_name(cls, v):
        if v is not None:
            if not is_safe_input(v):
                raise ValueError('El nombre contiene caracteres no permitidos')
            try:
                return validate_customer_name(v)
            except ValueError as e:
                raise ValueError(str(e))
        return v
    
    @validator('phone_number')
    def validate_phone_number(cls, v):
        if v is not None:
            if not is_safe_input(v):
                raise ValueError('El teléfono contiene caracteres no permitidos')
            try:
                return validate_phone_number(v)
            except ValueError as e:
                raise ValueError(str(e))
        return v
    
    @validator('guide_number')
    def validate_guide_number(cls, v):
        if v is not None:
            if not is_safe_input(v):
                raise ValueError('El número de guía contiene caracteres no permitidos')
            try:
                return validate_guide_number(v)
            except ValueError as e:
                raise ValueError(str(e))
        return v

class AnnouncementResponse(BaseModel):
    """Esquema de respuesta de anuncio"""
    id: Union[str, UUID]  # Permitir tanto string como UUID
    customer_name: str
    phone_number: str
    guide_number: str
    tracking_code: str
    is_active: bool
    is_processed: bool
    announced_at: datetime
    processed_at: Optional[datetime] = None
    status: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        # Configuración para manejar UUIDs
        json_encoders = {
            UUID: str
        }
