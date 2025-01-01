# ========================================
# PAQUETES EL CLUB v3.0 - Esquemas de Paquete
# ========================================

from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime
from ..models.package import PackageStatus, PackageType, PackageCondition
from .base import BaseSchemaWithTimestamps

class PackageBase(BaseModel):
    """Esquema base de paquete"""
    customer_name: str
    customer_phone: str
    package_type: PackageType = PackageType.NORMAL
    package_condition: PackageCondition = PackageCondition.BUENO
    observations: Optional[str] = None

class PackageCreate(PackageBase):
    """Esquema para crear paquete"""
    pass

class PackageUpdate(BaseModel):
    """Esquema para actualizar paquete"""
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    status: Optional[PackageStatus] = None
    package_type: Optional[PackageType] = None
    package_condition: Optional[PackageCondition] = None
    storage_cost: Optional[Decimal] = None
    delivery_cost: Optional[Decimal] = None
    total_cost: Optional[Decimal] = None
    observations: Optional[str] = None

class PackageResponse(BaseSchemaWithTimestamps, PackageBase):
    """Esquema de respuesta de paquete"""
    tracking_number: str
    status: PackageStatus
    storage_cost: Decimal
    delivery_cost: Decimal
    total_cost: Decimal
    announced_at: Optional[datetime] = None
    received_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None

class PackageAnnounce(BaseModel):
    """Esquema para anunciar paquete"""
    customer_name: str
    customer_phone: str
    package_type: PackageType = PackageType.NORMAL
    package_condition: PackageCondition = PackageCondition.BUENO
    observations: Optional[str] = None

class PackageTracking(BaseModel):
    """Esquema para consulta de tracking"""
    tracking_number: str
