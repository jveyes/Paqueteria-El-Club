# ========================================
# PAQUETES EL CLUB v3.0 - Modelo Base
# ========================================

from sqlalchemy import Column, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
import uuid

class BaseModel:
    """Modelo base con campos comunes"""
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
