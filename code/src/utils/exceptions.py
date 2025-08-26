# ========================================
# PAQUETES EL CLUB v3.0 - Manejo de Excepciones
# ========================================

from fastapi import HTTPException, status
from typing import Any, Dict, Optional

class PaqueteriaException(Exception):
    """Excepción base para la aplicación"""
    def __init__(self, message: str, status_code: int = 500, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

class PackageNotFoundException(PaqueteriaException):
    """Excepción cuando no se encuentra un paquete"""
    def __init__(self, tracking_number: str):
        super().__init__(
            message=f"Paquete con tracking {tracking_number} no encontrado",
            status_code=status.HTTP_404_NOT_FOUND,
            details={"tracking_number": tracking_number}
        )

class CustomerNotFoundException(PaqueteriaException):
    """Excepción cuando no se encuentra un cliente"""
    def __init__(self, tracking_number: str):
        super().__init__(
            message=f"Cliente con tracking {tracking_number} no encontrado",
            status_code=status.HTTP_404_NOT_FOUND,
            details={"tracking_number": tracking_number}
        )

class InvalidPackageStatusException(PaqueteriaException):
    """Excepción cuando el estado del paquete no es válido para la operación"""
    def __init__(self, current_status: str, required_status: str, operation: str):
        super().__init__(
            message=f"No se puede {operation} un paquete en estado {current_status}",
            status_code=status.HTTP_400_BAD_REQUEST,
            details={
                "current_status": current_status,
                "required_status": required_status,
                "operation": operation
            }
        )

class DuplicateTrackingNumberException(PaqueteriaException):
    """Excepción cuando ya existe un tracking number"""
    def __init__(self, tracking_number: str):
        super().__init__(
            message=f"Ya existe un paquete con tracking {tracking_number}",
            status_code=status.HTTP_400_BAD_REQUEST,
            details={"tracking_number": tracking_number}
        )

class RateCalculationException(PaqueteriaException):
    """Excepción en el cálculo de tarifas"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            details=details
        )

class NotificationException(PaqueteriaException):
    """Excepción en el envío de notificaciones"""
    def __init__(self, notification_type: str, message: str):
        super().__init__(
            message=f"Error enviando notificación {notification_type}: {message}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details={"notification_type": notification_type}
        )

def handle_paqueteria_exception(exc: PaqueteriaException) -> HTTPException:
    """Convertir excepción personalizada a HTTPException"""
    return HTTPException(
        status_code=exc.status_code,
        detail={
            "message": exc.message,
            "details": exc.details
        }
    )
