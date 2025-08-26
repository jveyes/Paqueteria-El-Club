# ========================================
# PAQUETES EL CLUB v3.0 - Validadores
# ========================================

import re
from typing import Optional
from ..utils.exceptions import RateCalculationException

def validate_phone_number(phone: str) -> bool:
    """Validar formato de número de teléfono colombiano"""
    # Patrón para números colombianos: +57 3XX XXX XXXX o 3XX XXX XXXX
    pattern = r'^(\+57\s?)?(3\d{2})\s?(\d{3})\s?(\d{4})$'
    return bool(re.match(pattern, phone))

def validate_tracking_number(tracking: str) -> bool:
    """Validar formato de número de tracking"""
    # Formato: PAP + YYYYMMDD + 8 caracteres alfanuméricos
    pattern = r'^PAP\d{8}[A-Z0-9]{8}$'
    return bool(re.match(pattern, tracking))

def validate_email(email: str) -> bool:
    """Validar formato de email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_package_dimensions(length: float, width: float, height: float) -> bool:
    """Validar dimensiones de paquete"""
    if any(dim <= 0 for dim in [length, width, height]):
        return False
    if any(dim > 200 for dim in [length, width, height]):  # 200cm máximo
        return False
    return True

def validate_package_weight(weight: float) -> bool:
    """Validar peso del paquete"""
    if weight <= 0:
        return False
    if weight > 50:  # 50kg máximo
        return False
    return True

def validate_rate_calculation_params(
    package_type: str,
    storage_days: int,
    delivery_required: bool
) -> None:
    """Validar parámetros para cálculo de tarifas"""
    if storage_days < 1:
        raise RateCalculationException("Los días de almacenamiento deben ser al menos 1")
    
    if storage_days > 365:
        raise RateCalculationException("Los días de almacenamiento no pueden exceder 365")
    
    valid_package_types = ["normal", "extra_dimensionado"]
    if package_type not in valid_package_types:
        raise RateCalculationException(f"Tipo de paquete debe ser uno de: {valid_package_types}")

def sanitize_filename(filename: str) -> str:
    """Sanitizar nombre de archivo"""
    # Remover caracteres peligrosos
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Limitar longitud
    if len(filename) > 255:
        name, ext = filename.rsplit('.', 1)
        filename = name[:250] + '.' + ext
    return filename

def validate_file_extension(filename: str, allowed_extensions: list) -> bool:
    """Validar extensión de archivo"""
    if not filename:
        return False
    ext = filename.lower().split('.')[-1]
    return ext in [ext.lower() for ext in allowed_extensions]

def validate_file_size(file_size: int, max_size: int) -> bool:
    """Validar tamaño de archivo"""
    return file_size <= max_size
