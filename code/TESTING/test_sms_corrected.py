#!/usr/bin/env python3
# ========================================
# PAQUETES EL CLUB v3.1 - Prueba SMS Corregida
# ========================================

import sys
import os
import asyncio
import httpx
from datetime import datetime

# Configuración directa para evitar problemas de importación
LIWA_CONFIG = {
    "api_key": "c52d8399ac63a24563ee8a967bafffc6cb8d8dfa",
    "account": "00486396309",
    "password": "6fEuRnd*$$#NfFAS",
    "auth_url": "https://api.liwa.co/v2/auth/login",
    "from_name": "PAQUETES EL CLUB"
}

class CorrectedLIWASMSService:
    """Servicio SMS corregido para LIWA.co"""
    
    def __init__(self):
        self.api_key = LIWA_CONFIG["api_key"]
        self.account = LIWA_CONFIG["account"]
        self.password = LIWA_CONFIG["password"]
        self.auth_url = LIWA_CONFIG["auth_url"]
        self.from_name = LIWA_CONFIG["from_name"]
        self._auth_token = None
        self._token_expiry = None
    
    async def _get_auth_token(self):
        """Obtener token de autenticación de LIWA.co"""
        try:
            auth_data = {
                "account": self.account,
                "password": self.password
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.auth_url,
                    json=auth_data,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    auth_response = response.json()
                    self._auth_token = auth_response.get("token")
                    print(f"✅ Token obtenido: {self._auth_token[:20]}...")
                    return self._auth_token
                else:
                    print(f"❌ Error de autenticación: {response.status_code} - {response.text}")
                    return None
                    
        except Exception as e:
            print(f"❌ Error obteniendo token: {e}")
            return None
    
    async def send_sms(self, phone_number: str, message: str):
        """Enviar SMS usando LIWA.co - Endpoint corregido"""
        try:
            print(f"🔐 Obteniendo token de autenticación...")
            token = await self._get_auth_token()
            if not token:
                return {
                    "success": False,
                    "error": "No se pudo obtener token de autenticación",
                    "provider": "LIWA.co"
                }
            
            # Formatear número de teléfono
            if not phone_number.startswith('+'):
                formatted_phone = f"+57{phone_number}"
            else:
                formatted_phone = phone_number
            
            print(f"📱 Formateando número: {phone_number} → {formatted_phone}")
            
            # Preparar datos para envío - Formato corregido para LIWA.co
            sms_data = {
                "to": formatted_phone,
                "message": message,
                "from": self.from_name,
                "api_key": self.api_key  # Incluir API key en el body
            }
            
            print(f"📤 Enviando SMS a {formatted_phone}...")
            print(f"📝 Mensaje: {message[:50]}...")
            
            # Probar diferentes endpoints de LIWA.co
            endpoints = [
                "https://api.liwa.co/v2/sms/send",
                "https://api.liwa.co/v2/send-sms",
                "https://api.liwa.co/sms/send",
                "https://api.liwa.co/send-sms"
            ]
            
            for endpoint in endpoints:
                print(f"🌐 Probando endpoint: {endpoint}")
                
                try:
                    async with httpx.AsyncClient() as client:
                        response = await client.post(
                            endpoint,
                            json=sms_data,
                            headers={
                                "Authorization": f"Bearer {token}",
                                "Content-Type": "application/json",
                                "X-API-Key": self.api_key  # Header alternativo
                            },
                            timeout=30.0
                        )
                        
                        print(f"📡 Respuesta de {endpoint}: {response.status_code}")
                        
                        if response.status_code == 200:
                            result = response.json()
                            print(f"✅ SMS enviado exitosamente desde {endpoint}!")
                            return {
                                "success": True,
                                "message_id": result.get("id"),
                                "provider": "LIWA.co",
                                "phone": formatted_phone,
                                "timestamp": datetime.now().isoformat(),
                                "endpoint": endpoint
                            }
                        elif response.status_code == 401:
                            print(f"🔐 Error de autenticación en {endpoint}")
                            continue
                        elif response.status_code == 404:
                            print(f"🔍 Endpoint no encontrado: {endpoint}")
                            continue
                        else:
                            print(f"❌ Error {response.status_code} en {endpoint}: {response.text}")
                            continue
                            
                except httpx.ConnectError:
                    print(f"🌐 Error de conexión a {endpoint}")
                    continue
                except httpx.TimeoutException:
                    print(f"⏰ Timeout en {endpoint}")
                    continue
                except Exception as e:
                    print(f"💥 Error en {endpoint}: {e}")
                    continue
            
            # Si llegamos aquí, ningún endpoint funcionó
            return {
                "success": False,
                "error": "Ningún endpoint de LIWA.co funcionó",
                "provider": "LIWA.co",
                "phone": formatted_phone
            }
                    
        except Exception as e:
            print(f"💥 Excepción: {e}")
            return {
                "success": False,
                "error": str(e),
                "provider": "LIWA.co",
                "phone": phone_number
            }

async def test_sms_corrected():
    """Probar envío de SMS con endpoint corregido"""
    print("🚀 PAQUETES EL CLUB v3.1 - Prueba SMS LIWA.co CORREGIDA")
    print("=" * 60)
    print(f"📱 Número de prueba: 3002596319")
    print(f"🕐 Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Crear servicio SMS
    sms_service = CorrectedLIWASMSService()
    
    # Número de prueba
    test_phone = "3002596319"
    
    # Mensaje de prueba
    test_message = f"¡Prueba de SMS exitosa! 🎉\n\n" \
                   f"📦 Número de Guía: TEST123\n" \
                   f"🔗 Código de Consulta: TEST\n\n" \
                   f"Consulta el estado en: http://localhost/track\n\n" \
                   f"Recibirás confirmación por SMS cuando cambie el estado.\n\n" \
                   f"PAQUETES EL CLUB\n" \
                   f"🕐 {datetime.now().strftime('%H:%M:%S')}"
    
    print(f"📝 Mensaje a enviar:")
    print("-" * 40)
    print(test_message)
    print("-" * 40)
    
    try:
        print(f"\n📤 Enviando SMS a: {test_phone}")
        print("⏳ Probando diferentes endpoints de LIWA.co...")
        
        # Enviar SMS
        result = await sms_service.send_sms(test_phone, test_message)
        
        print("\n📊 RESULTADO DEL ENVÍO:")
        print("=" * 40)
        
        if result["success"]:
            print("✅ SMS enviado exitosamente!")
            print(f"🆔 Message ID: {result.get('message_id', 'N/A')}")
            print(f"📱 Teléfono: {result.get('phone', 'N/A')}")
            print(f"⏰ Timestamp: {result.get('timestamp', 'N/A')}")
            print(f"🌐 Proveedor: {result.get('provider', 'N/A')}")
            print(f"🔗 Endpoint: {result.get('endpoint', 'N/A')}")
        else:
            print("❌ Error enviando SMS")
            print(f"🚨 Error: {result['error']}")
            print(f"📱 Teléfono: {result.get('phone', 'N/A')}")
            print(f"🌐 Proveedor: {result.get('provider', 'N/A')}")
            
    except Exception as e:
        print(f"\n💥 EXCEPCIÓN DURANTE EL ENVÍO:")
        print(f"🚨 Error: {e}")
        print(f"📋 Tipo: {type(e).__name__}")
    
    print("\n" + "=" * 60)
    print("🏁 Prueba completada")
    print("📱 Verifica tu teléfono 3002596319 para el SMS")

if __name__ == "__main__":
    asyncio.run(test_sms_corrected())
