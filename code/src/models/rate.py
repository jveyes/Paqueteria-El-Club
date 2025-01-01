# ========================================
# PAQUETES EL CLUB v3.0 - Modelo de Tarifas
# ========================================

from sqlalchemy import Column, String, Numeric, Boolean, DateTime, Enum
import enum
from datetime import datetime

from .base import BaseModel
from ..database.database import Base

class RateType(str, enum.Enum):
    """Tipos de tarifa"""
    STORAGE = "storage"
    DELIVERY = "delivery"
    PACKAGE_TYPE = "package_type"

class Rate(BaseModel, Base):
    """Modelo de tarifas"""
    __tablename__ = "rates"
    
    rate_type = Column(Enum(RateType), nullable=False)
    base_price = Column(Numeric(10, 2), nullable=False)
    daily_storage_rate = Column(Numeric(10, 2), default=0)
    delivery_rate = Column(Numeric(10, 2), default=0)
    package_type_multiplier = Column(Numeric(10, 2), default=1.0)
    is_active = Column(Boolean, default=True)
    valid_from = Column(DateTime, default=datetime.now)
    valid_to = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<Rate {self.rate_type} - {self.base_price}>"
