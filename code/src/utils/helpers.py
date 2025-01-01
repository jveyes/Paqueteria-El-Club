# ========================================
# PAQUETES EL CLUB v3.0 - Funciones Helper
# ========================================

import uuid
import hashlib
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from passlib.context import CryptContext
from ..config import settings
from .datetime_utils import get_colombia_now

# Configuración de hash de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verificar contraseña"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Generar hash de contraseña"""
    return pwd_context.hash(password)

def generate_tracking_number() -> str:
    """Generar número de tracking único"""
    date_str = get_colombia_now().strftime('%Y%m%d')
    unique_id = str(uuid.uuid4())[:8].upper()
    return f"PAP{date_str}{unique_id}"

def generate_unique_filename(original_filename: str) -> str:
    """Generar nombre de archivo único"""
    name, ext = os.path.splitext(original_filename)
    timestamp = get_colombia_now().strftime('%Y%m%d_%H%M%S')
    unique_id = str(uuid.uuid4())[:8]
    return f"{name}_{timestamp}_{unique_id}{ext}"

def calculate_file_hash(file_path: str) -> str:
    """Calcular hash SHA-256 de un archivo"""
    hash_sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

def format_currency(amount: float, currency: str = "COP") -> str:
    """Formatear cantidad como moneda"""
    if currency == "COP":
        return f"${amount:,.0f}"
    return f"{currency} {amount:,.2f}"

def format_phone_number(phone: str) -> str:
    """Formatear número de teléfono colombiano"""
    # Remover espacios y caracteres especiales
    phone = ''.join(filter(str.isdigit, phone))
    
    if len(phone) == 10:
        return f"+57 {phone[:3]} {phone[3:6]} {phone[6:]}"
    elif len(phone) == 12 and phone.startswith('57'):
        return f"+57 {phone[2:5]} {phone[5:8]} {phone[8:]}"
    else:
        return phone

def get_file_size_mb(file_size_bytes: int) -> float:
    """Convertir bytes a MB"""
    return round(file_size_bytes / (1024 * 1024), 2)

def is_valid_date_range(start_date: datetime, end_date: datetime) -> bool:
    """Validar rango de fechas"""
    return start_date < end_date

def calculate_days_between(start_date: datetime, end_date: datetime) -> int:
    """Calcular días entre dos fechas"""
    return (end_date - start_date).days

def get_package_status_color(status: str) -> str:
    """Obtener color CSS para estado de paquete"""
    colors = {
        "anunciado": "bg-blue-100 text-blue-800",
        "recibido": "bg-yellow-100 text-yellow-800",
        "en_transito": "bg-purple-100 text-purple-800",
        "entregado": "bg-green-100 text-green-800",
        "cancelado": "bg-red-100 text-red-800"
    }
    return colors.get(status, "bg-gray-100 text-gray-800")

def get_package_status_icon(status: str) -> str:
    """Obtener icono para estado de paquete"""
    icons = {
        "anunciado": "📦",
        "recibido": "📥",
        "en_transito": "🚚",
        "entregado": "✅",
        "cancelado": "❌"
    }
    return icons.get(status, "❓")

def create_pagination_metadata(
    total_items: int,
    page: int,
    page_size: int,
    base_url: str
) -> Dict[str, Any]:
    """Crear metadatos de paginación"""
    total_pages = (total_items + page_size - 1) // page_size
    
    return {
        "total_items": total_items,
        "total_pages": total_pages,
        "current_page": page,
        "page_size": page_size,
        "has_next": page < total_pages,
        "has_prev": page > 1,
        "next_page": page + 1 if page < total_pages else None,
        "prev_page": page - 1 if page > 1 else None,
        "base_url": base_url
    }

def sanitize_search_term(search_term: str) -> str:
    """Sanitizar término de búsqueda"""
    # Remover caracteres especiales peligrosos para SQL
    dangerous_chars = ['%', '_', ';', '--', '/*', '*/']
    for char in dangerous_chars:
        search_term = search_term.replace(char, '')
    return search_term.strip()

def get_environment_info() -> Dict[str, Any]:
    """Obtener información del entorno"""
    return {
        "environment": settings.environment,
        "version": settings.app_version,
        "debug": settings.debug,
        "timestamp": get_colombia_now().isoformat()
    }
