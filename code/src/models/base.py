# ========================================
# PAQUETES EL CLUB v3.0 - Modelo Base
# ========================================

from sqlalchemy import Column, DateTime, func, String
from sqlalchemy.dialects.postgresql import UUID
import uuid
from ..utils.datetime_utils import get_colombia_now
from ..config import settings

class BaseModel:
    """Modelo base con campos comunes"""
    # Usar UUID para PostgreSQL, String para SQLite
    if settings.database_url.startswith("sqlite"):
        id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    else:
        id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Campos de timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=True)

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
