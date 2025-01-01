# ========================================
# PAQUETES EL CLUB v3.1 - Excepciones Personalizadas
# ========================================

from fastapi import HTTPException, status
from typing import Any, Dict, Optional

class PaqueteriaException(Exception):
    """Excepción base para la aplicación"""
    pass

class DuplicateTrackingNumberException(PaqueteriaException):
    """Excepción para números de tracking duplicados"""
    pass

class UserException(PaqueteriaException):
    """Excepción para errores relacionados con usuarios"""
    pass

class NotificationException(PaqueteriaException):
    """Excepción para errores de notificaciones"""
    pass

class PackageException(PaqueteriaException):
    """Excepción para errores relacionados con paquetes"""
    pass

class RateException(PaqueteriaException):
    """Excepción para errores relacionados con tarifas"""
    pass

class FileException(PaqueteriaException):
    """Excepción para errores relacionados con archivos"""
    pass

class DatabaseException(PaqueteriaException):
    """Excepción para errores de base de datos"""
    pass

class ValidationException(PaqueteriaException):
    """Excepción para errores de validación"""
    pass

class AuthenticationException(PaqueteriaException):
    """Excepción para errores de autenticación"""
    pass

class AuthorizationException(PaqueteriaException):
    """Excepción para errores de autorización"""
    pass

class RateCalculationException(PaqueteriaException):
    """Excepción para errores de cálculo de tarifas"""
    pass

class PackageNotFoundException(PaqueteriaException):
    """Excepción para paquetes no encontrados"""
    pass

class CustomerNotFoundException(PaqueteriaException):
    """Excepción para clientes no encontrados"""
    pass

class InvalidPackageStatusException(PaqueteriaException):
    """Excepción para estados de paquete inválidos"""
    pass
