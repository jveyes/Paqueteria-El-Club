# ========================================
# PAQUETES EL CLUB v3.0 - Esquemas de Cliente
# ========================================

from pydantic import BaseModel
from typing import Optional
from .base import BaseSchemaWithTimestamps

class CustomerBase(BaseModel):
    """Esquema base de cliente"""
    name: str
    phone: str
    tracking_number: str

class CustomerCreate(CustomerBase):
    """Esquema para crear cliente"""
    pass

class CustomerUpdate(BaseModel):
    """Esquema para actualizar cliente"""
    name: Optional[str] = None
    phone: Optional[str] = None
    tracking_number: Optional[str] = None

class CustomerResponse(BaseSchemaWithTimestamps, CustomerBase):
    """Esquema de respuesta de cliente"""
    pass

class CustomerSearch(BaseModel):
    """Esquema para búsqueda de clientes"""
    name: Optional[str] = None
    phone: Optional[str] = None
    tracking_number: Optional[str] = None
