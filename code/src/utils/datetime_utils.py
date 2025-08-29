# ========================================
# PAQUETES EL CLUB v3.1 - Utilidades de Fecha y Hora
# ========================================
# Módulo para manejar fechas y horas con zona horaria de Colombia

from datetime import datetime, timezone
import pytz
from typing import Optional

# Zona horaria de Colombia
COLOMBIA_TZ = pytz.timezone('America/Bogota')

def get_colombia_now() -> datetime:
    """
    Obtener la fecha y hora actual en zona horaria de Colombia
    
    Returns:
        datetime: Fecha y hora actual en Colombia
    """
    return datetime.now(COLOMBIA_TZ)

def get_colombia_datetime(dt: Optional[datetime] = None) -> datetime:
    """
    Convertir datetime a zona horaria de Colombia
    
    Args:
        dt (datetime, optional): Fecha y hora a convertir. Si es None, usa la hora actual
    
    Returns:
        datetime: Fecha y hora en zona horaria de Colombia
    """
    if dt is None:
        dt = datetime.now()
    
    # Si ya tiene zona horaria, convertir a Colombia
    if dt.tzinfo is not None:
        return dt.astimezone(COLOMBIA_TZ)
    
    # Si no tiene zona horaria, asumir que es UTC y convertir
    utc_dt = dt.replace(tzinfo=timezone.utc)
    return utc_dt.astimezone(COLOMBIA_TZ)

def format_colombia_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Formatear datetime en zona horaria de Colombia
    
    Args:
        dt (datetime): Fecha y hora a formatear
        format_str (str): Formato de salida
    
    Returns:
        str: Fecha y hora formateada en Colombia
    """
    colombia_dt = get_colombia_datetime(dt)
    return colombia_dt.strftime(format_str)

def get_colombia_date() -> str:
    """
    Obtener la fecha actual en Colombia en formato YYYY-MM-DD
    
    Returns:
        str: Fecha actual en Colombia
    """
    return get_colombia_now().strftime("%Y-%m-%d")

def get_colombia_time() -> str:
    """
    Obtener la hora actual en Colombia en formato HH:MM:SS
    
    Returns:
        str: Hora actual en Colombia
    """
    return get_colombia_now().strftime("%H:%M:%S")

def is_same_day(dt1: datetime, dt2: datetime) -> bool:
    """
    Verificar si dos fechas son del mismo día en Colombia
    
    Args:
        dt1 (datetime): Primera fecha
        dt2 (datetime): Segunda fecha
    
    Returns:
        bool: True si son del mismo día
    """
    col_dt1 = get_colombia_datetime(dt1).date()
    col_dt2 = get_colombia_datetime(dt2).date()
    return col_dt1 == col_dt2

def get_colombia_timestamp() -> float:
    """
    Obtener timestamp actual en zona horaria de Colombia
    
    Returns:
        float: Timestamp actual
    """
    return get_colombia_now().timestamp()
