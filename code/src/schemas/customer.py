# ========================================
# PAQUETES EL CLUB v3.0 - Esquemas de Cliente
# ========================================

from pydantic import BaseModel, validator
from typing import Optional
from .base import BaseSchemaWithTimestamps
from ..utils.validators import validate_international_phone_number

class CustomerBase(BaseModel):
    """Esquema base de cliente"""
    name: str
    phone: str
    tracking_number: str
    
    @validator('phone')
    def validate_phone_number(cls, v):
        if not v:
            raise ValueError('El número de teléfono es requerido')
        
        result = validate_international_phone_number(v)
        if not result['is_valid']:
            raise ValueError(result['error_message'])
        
        return result['formatted_number']

class CustomerCreate(CustomerBase):
    """Esquema para crear cliente"""
    pass

class CustomerUpdate(BaseModel):
    """Esquema para actualizar cliente"""
    name: Optional[str] = None
    phone: Optional[str] = None
    country_code: Optional[str] = None
    phone_formatted: Optional[str] = None
    phone_country: Optional[str] = None
    tracking_number: Optional[str] = None
    
    @validator('phone')
    def validate_phone_number(cls, v):
        if v is None:
            return v
        
        result = validate_international_phone_number(v)
        if not result['is_valid']:
            raise ValueError(result['error_message'])
        
        return result['formatted_number']

class CustomerResponse(BaseSchemaWithTimestamps, CustomerBase):
    """Esquema de respuesta de cliente"""
    pass

class CustomerSearch(BaseModel):
    """Esquema para búsqueda de clientes"""
    name: Optional[str] = None
    phone: Optional[str] = None
    tracking_number: Optional[str] = None
