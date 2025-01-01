# ========================================
# PAQUETES EL CLUB v3.1 - Servicio de SMS
# ========================================

import httpx
import logging
from typing import Optional, Dict, Any
import os

# Configuración directa para evitar problemas de importación
LIWA_CONFIG = {
    "account": "00486396309",
    "password": "6fEuRnd*$$#NfFAS",
    "api_key": "c52d8399ac63a24563ee8a967bafffc6cb8d8dfa",
    "auth_url": "https://api.liwa.co/v2/auth/login",
}

logger = logging.getLogger(__name__)

class SMSService:
    """Servicio para envío de SMS usando LIWA.co"""
    
    def __init__(self):
        self.account = LIWA_CONFIG["account"]
        self.password = LIWA_CONFIG["password"]
        self.api_key = LIWA_CONFIG["api_key"]
        self.auth_url = LIWA_CONFIG["auth_url"]
        self.sms_url = "https://api.liwa.co/v2/sms/single"
        self._auth_token = None
        self._token_expiry = None
    
    async def _authenticate(self) -> bool:
        """Autenticarse con LIWA.co y obtener token"""
        try:
            auth_data = {
                "account": self.account,
                "password": self.password
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.auth_url,
                    json=auth_data,
                    headers={"Content-Type": "application/json"},
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    self._auth_token = result.get("token")
                    logger.info("Autenticación LIWA.co exitosa")
                    return True
                else:
                    logger.error(f"Error en autenticación LIWA.co: {response.status_code} - {response.text}")
                    return False
                    
        except Exception as e:
            logger.error(f"Error en autenticación LIWA.co: {e}")
            return False
    
    def _format_phone_number(self, phone: str) -> str:
        """
        Formatear número de teléfono para LIWA.co
        
        Args:
            phone (str): Número de 10 dígitos (ej: 3001234567)
            
        Returns:
            str: Número con código de país (ej: 573001234567)
        """
        # Limpiar el número (solo dígitos)
        clean_phone = ''.join(filter(str.isdigit, phone))
        
        # Verificar que tenga 10 dígitos
        if len(clean_phone) != 10:
            raise ValueError(f"El número de teléfono debe tener 10 dígitos, recibido: {len(clean_phone)}")
        
        # Verificar que sea un número colombiano válido
        if not clean_phone.startswith(('3', '6')):
            raise ValueError("El número debe ser un celular o fijo colombiano válido")
        
        # Agregar código de país Colombia (57)
        return f"57{clean_phone}"
    
    async def send_tracking_sms(self, phone: str, customer_name: str, tracking_code: str, guide_number: str) -> Dict[str, Any]:
        """
        Enviar SMS con código de tracking
        
        Args:
            phone (str): Número de teléfono del cliente (10 dígitos)
            customer_name (str): Nombre del cliente
            tracking_code (str): Código de tracking generado
            guide_number (str): Número de guía ingresado
            
        Returns:
            Dict con resultado del envío
        """
        try:
            # Formatear número de teléfono
            formatted_phone = self._format_phone_number(phone)
            
            # Autenticarse si no hay token
            if not self._auth_token:
                if not await self._authenticate():
                    return {
                        "success": False,
                        "error": "No se pudo autenticar con LIWA.co"
                    }
            
            # Preparar mensaje
            message = (
                f"Hola {customer_name}, tu paquete con guía {guide_number} "
                f"ha sido registrado. Código de consulta: {tracking_code}. "
                f"PAQUETES EL CLUB"
            )
            
            # Datos para el SMS
            sms_data = {
                "number": formatted_phone,
                "message": message,
                "type": 1  # SMS estándar
            }
            
            headers = {
                "Authorization": f"Bearer {self._auth_token}",
                "API-KEY": self.api_key,
                "Content-Type": "application/json"
            }
            
            # Enviar SMS
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.sms_url,
                    json=sms_data,
                    headers=headers,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    logger.info(f"SMS enviado exitosamente a {formatted_phone}")
                    return {
                        "success": True,
                        "phone": formatted_phone,
                        "message": message,
                        "tracking_code": tracking_code,
                        "liwa_response": result
                    }
                else:
                    logger.error(f"Error al enviar SMS: {response.status_code} - {response.text}")
                    return {
                        "success": False,
                        "error": f"Error en envío: {response.status_code}",
                        "phone": formatted_phone
                    }
                    
        except ValueError as e:
            logger.error(f"Error de validación en número de teléfono: {e}")
            return {
                "success": False,
                "error": str(e)
            }
        except Exception as e:
            logger.error(f"Error inesperado al enviar SMS: {e}")
            return {
                "success": False,
                "error": f"Error inesperado: {str(e)}"
            }
    
    async def send_notification_sms(self, phone: str, message: str) -> Dict[str, Any]:
        """
        Enviar SMS de notificación genérica
        
        Args:
            phone (str): Número de teléfono (10 dígitos)
            message (str): Mensaje a enviar
            
        Returns:
            Dict con resultado del envío
        """
        try:
            formatted_phone = self._format_phone_number(phone)
            
            if not self._auth_token:
                if not await self._authenticate():
                    return {
                        "success": False,
                        "error": "No se pudo autenticar con LIWA.co"
                    }
            
            sms_data = {
                "number": formatted_phone,
                "message": message,
                "type": 1
            }
            
            headers = {
                "Authorization": f"Bearer {self._auth_token}",
                "API-KEY": self.api_key,
                "Content-Type": "application/json"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.sms_url,
                    json=sms_data,
                    headers=headers,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    logger.info(f"SMS de notificación enviado a {formatted_phone}")
                    return {
                        "success": True,
                        "phone": formatted_phone,
                        "message": message,
                        "liwa_response": result
                    }
                else:
                    logger.error(f"Error al enviar SMS de notificación: {response.status_code}")
                    return {
                        "success": False,
                        "error": f"Error en envío: {response.status_code}",
                        "phone": formatted_phone
                    }
                    
        except Exception as e:
            logger.error(f"Error al enviar SMS de notificación: {e}")
            return {
                "success": False,
                "error": str(e)
            }
