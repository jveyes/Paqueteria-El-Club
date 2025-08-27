# ========================================
# PAQUETES EL CLUB v3.1 - Esquemas de Anuncio de Paquetes
# ========================================

from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime
from .base import BaseSchemaWithTimestamps

class AnnouncementBase(BaseModel):
    """Esquema base de anuncio"""
    customer_name: str
    phone_number: str
    guide_number: str

class AnnouncementCreate(AnnouncementBase):
    """Esquema para crear anuncio"""
    @validator('customer_name')
    def validate_customer_name(cls, v):
        if not v.strip():
            raise ValueError('El nombre del cliente es requerido')
        if len(v.strip()) < 2:
            raise ValueError('El nombre debe tener al menos 2 caracteres')
        return v.strip()
    
    @validator('phone_number')
    def validate_phone_number(cls, v):
        # Remover caracteres no numéricos
        digits = ''.join(filter(str.isdigit, v))
        if len(digits) < 7:
            raise ValueError('El teléfono debe tener al menos 7 dígitos')
        return v
    
    @validator('guide_number')
    def validate_guide_number(cls, v):
        if not v.strip():
            raise ValueError('El número de guía es requerido')
        if len(v.strip()) < 3:
            raise ValueError('El número de guía debe tener al menos 3 caracteres')
        return v.strip().upper()

class AnnouncementUpdate(BaseModel):
    """Esquema para actualizar anuncio"""
    customer_name: Optional[str] = None
    phone_number: Optional[str] = None
    guide_number: Optional[str] = None
    tracking_code: Optional[str] = None
    is_active: Optional[bool] = None
    is_processed: Optional[bool] = None

class AnnouncementResponse(BaseSchemaWithTimestamps, AnnouncementBase):
    """Esquema de respuesta de anuncio"""
    tracking_code: str
    is_active: bool
    is_processed: bool
    announced_at: datetime
    processed_at: Optional[datetime] = None
    status: str
