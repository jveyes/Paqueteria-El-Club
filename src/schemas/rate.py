# ========================================
# PAQUETES EL CLUB v3.0 - Esquemas de Tarifas
# ========================================

from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime
from ..models.package import PackageType
from ..models.rate import RateType
from .base import BaseSchemaWithTimestamps

class RateBase(BaseModel):
    """Esquema base de tarifa"""
    rate_type: RateType
    base_price: Decimal
    daily_storage_rate: Decimal = Decimal('0')
    delivery_rate: Decimal = Decimal('0')
    package_type_multiplier: Decimal = Decimal('1.0')
    is_active: bool = True

class RateCreate(RateBase):
    """Esquema para crear tarifa"""
    pass

class RateUpdate(BaseModel):
    """Esquema para actualizar tarifa"""
    rate_type: Optional[RateType] = None
    base_price: Optional[Decimal] = None
    daily_storage_rate: Optional[Decimal] = None
    delivery_rate: Optional[Decimal] = None
    package_type_multiplier: Optional[Decimal] = None
    is_active: Optional[bool] = None

class RateResponse(BaseSchemaWithTimestamps, RateBase):
    """Esquema de respuesta de tarifa"""
    valid_from: datetime
    valid_to: Optional[datetime] = None

class RateCalculation(BaseModel):
    """Esquema para cálculo de tarifas"""
    package_type: PackageType
    storage_days: int = 1
    delivery_required: bool = True
