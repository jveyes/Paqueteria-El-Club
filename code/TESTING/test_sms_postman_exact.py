#!/usr/bin/env python3
# ========================================
# PAQUETES EL CLUB v3.1 - Prueba SMS EXACTA como Postman
# ========================================

import sys
import os
import asyncio
import httpx
from datetime import datetime

# Configuración exacta como Postman
LIWA_CONFIG = {
    "api_key": "c52d8399ac63a24563ee8a967bafffc6cb8d8dfa",
    "account": "00486396309",
    "password": "6fEuRnd*$$#NfFAS",
    "auth_url": "https://api.liwa.co/v2/auth/login",
    "sms_url": "https://api.liwa.co/v2/sms/send",  # Endpoint exacto
    "from_name": "PAQUETES EL CLUB"
}

class PostmanExactLIWASMSService:
    """Servicio SMS que replica exactamente la configuración de Postman"""
    
    def __init__(self):
        self.api_key = LIWA_CONFIG["api_key"]
        self.account = LIWA_CONFIG["account"]
        self.password = LIWA_CONFIG["password"]
        self.auth_url = LIWA_CONFIG["auth_url"]
        self.sms_url = LIWA_CONFIG["sms_url"]
        self.from_name = LIWA_CONFIG["from_name"]
        self._auth_token = None
    
    async def _get_auth_token(self):
        """Obtener token de autenticación - igual que Postman"""
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
        """Enviar SMS - EXACTAMENTE como Postman"""
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
            
            # Body EXACTO como Postman (documentación)
            sms_data = {
                "to": formatted_phone,
                "message": message,
                "from": self.from_name
            }
            
            print(f"📤 Enviando SMS a {formatted_phone}...")
            print(f"📝 Mensaje: {message[:50]}...")
            print(f"🔗 Endpoint: {self.sms_url}")
            
            # Headers EXACTOS como Postman
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            print(f"🔐 Headers: {headers}")
            print(f"📦 Body: {sms_data}")
            
            # Enviar SMS - EXACTAMENTE como Postman
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.sms_url,
                    json=sms_data,
                    headers=headers,
                    timeout=30.0
                )
                
                print(f"📡 Respuesta de LIWA.co: {response.status_code}")
                print(f"📋 Headers de respuesta: {dict(response.headers)}")
                print(f"📄 Body de respuesta: {response.text}")
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"✅ SMS enviado exitosamente!")
                    return {
                        "success": True,
                        "message_id": result.get("id"),
                        "provider": "LIWA.co",
                        "phone": formatted_phone,
                        "timestamp": datetime.now().isoformat(),
                        "endpoint": self.sms_url
                    }
                else:
                    print(f"❌ Error enviando SMS: {response.status_code}")
                    return {
                        "success": False,
                        "error": f"Error {response.status_code}: {response.text}",
                        "provider": "LIWA.co",
                        "phone": formatted_phone,
                        "response_headers": dict(response.headers),
                        "response_body": response.text
                    }
                    
        except Exception as e:
            print(f"💥 Excepción: {e}")
            return {
                "success": False,
                "error": str(e),
                "provider": "LIWA.co",
                "phone": phone_number
            }

async def test_sms_postman_exact():
    """Probar envío de SMS EXACTAMENTE como Postman"""
    print("🚀 PAQUETES EL CLUB v3.1 - Prueba SMS EXACTA como Postman")
    print("=" * 60)
    print(f"📱 Número de prueba: 3002596319")
    print(f"🕐 Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Crear servicio SMS
    sms_service = PostmanExactLIWASMSService()
    
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
        print("⏳ Usando configuración EXACTA de Postman...")
        
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
            
            # Mostrar detalles de la respuesta para debugging
            if 'response_headers' in result:
                print(f"📋 Headers de respuesta: {result['response_headers']}")
            if 'response_body' in result:
                print(f"📄 Body de respuesta: {result['response_body']}")
            
    except Exception as e:
        print(f"\n💥 EXCEPCIÓN DURANTE EL ENVÍO:")
        print(f"🚨 Error: {e}")
        print(f"📋 Tipo: {type(e).__name__}")
    
    print("\n" + "=" * 60)
    print("🏁 Prueba completada")
    print("📱 Verifica tu teléfono 3002596319 para el SMS")

if __name__ == "__main__":
    asyncio.run(test_sms_postman_exact())
