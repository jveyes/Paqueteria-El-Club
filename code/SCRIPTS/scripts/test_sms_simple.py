#!/usr/bin/env python3
# ========================================
# PAQUETES EL CLUB v3.1 - Prueba Simple del Servicio de SMS
# ========================================

import asyncio
import httpx
import sys
import os

# Configuración directa (sin dependencias del proyecto)
LIWA_CONFIG = {
    "account": "00486396309",
    "password": "6fEuRnd*$$#NfFAS",
    "api_key": "c52d8399ac63a24563ee8a967bafffc6cb8d8dfa",
    "auth_url": "https://api.liwa.co/v2/auth/login",
    "sms_url": "https://api.liwa.co/v2/sms/single"
}

class SimpleSMSTest:
    """Prueba simple del servicio de SMS"""
    
    def __init__(self):
        self.account = LIWA_CONFIG["account"]
        self.password = LIWA_CONFIG["password"]
        self.api_key = LIWA_CONFIG["api_key"]
        self.auth_url = LIWA_CONFIG["auth_url"]
        self.sms_url = LIWA_CONFIG["sms_url"]
        self._auth_token = None
    
    def format_phone_number(self, phone: str) -> str:
        """Formatear número de teléfono para LIWA.co"""
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
    
    async def authenticate(self) -> bool:
        """Autenticarse con LIWA.co"""
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
                    print(f"✅ Autenticación exitosa")
                    print(f"   Token: {self._auth_token[:50]}..." if self._auth_token else "   No hay token")
                    return True
                else:
                    print(f"❌ Error en autenticación: {response.status_code}")
                    print(f"   Respuesta: {response.text}")
                    return False
                    
        except Exception as e:
            print(f"❌ Error en autenticación: {e}")
            return False
    
    async def send_tracking_sms(self, phone: str, customer_name: str, tracking_code: str, guide_number: str) -> dict:
        """Enviar SMS con código de tracking"""
        try:
            # Formatear número de teléfono
            formatted_phone = self.format_phone_number(phone)
            print(f"📱 Número formateado: {phone} → {formatted_phone}")
            
            # Autenticarse si no hay token
            if not self._auth_token:
                if not await self.authenticate():
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
            
            print(f"📤 Enviando SMS...")
            print(f"   URL: {self.sms_url}")
            print(f"   Teléfono: {formatted_phone}")
            print(f"   Mensaje: {message[:50]}...")
            
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
                    print(f"✅ SMS enviado exitosamente!")
                    print(f"   Respuesta LIWA: {result}")
                    return {
                        "success": True,
                        "phone": formatted_phone,
                        "message": message,
                        "tracking_code": tracking_code,
                        "liwa_response": result
                    }
                else:
                    print(f"❌ Error al enviar SMS: {response.status_code}")
                    print(f"   Respuesta: {response.text}")
                    return {
                        "success": False,
                        "error": f"Error en envío: {response.status_code}",
                        "phone": formatted_phone
                    }
                    
        except ValueError as e:
            print(f"❌ Error de validación: {e}")
            return {
                "success": False,
                "error": str(e)
            }
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            return {
                "success": False,
                "error": f"Error inesperado: {str(e)}"
            }

async def main():
    """Función principal de prueba"""
    print("🔍 PRUEBA SIMPLE DEL SERVICIO DE SMS")
    print("=" * 50)
    
    # Crear instancia del servicio
    sms_test = SimpleSMSTest()
    
    # Datos de prueba
    test_phone = "3001234567"  # Número de 10 dígitos
    test_customer_name = "Juan Pérez"
    test_tracking_code = "TRK123"
    test_guide_number = "GUIDE456"
    
    print(f"📱 Número de prueba: {test_phone}")
    print(f"👤 Cliente: {test_customer_name}")
    print(f"🔍 Código de tracking: {test_tracking_code}")
    print(f"📦 Número de guía: {test_guide_number}")
    print("-" * 50)
    
    try:
        # Prueba 1: Formateo de número de teléfono
        print("🔧 PRUEBA 1: Formateo de número de teléfono")
        formatted_phone = sms_test.format_phone_number(test_phone)
        expected = f"57{test_phone}"
        print(f"   Formato esperado: {expected}")
        print(f"   Formato correcto: {'✅' if formatted_phone == expected else '❌'}")
        
        # Prueba 2: Autenticación con LIWA.co
        print("\n🔐 PRUEBA 2: Autenticación con LIWA.co")
        auth_result = await sms_test.authenticate()
        if not auth_result:
            print("❌ Falló la autenticación, abortando pruebas")
            return
        
        # Prueba 3: Envío de SMS de tracking
        print("\n📤 PRUEBA 3: Envío de SMS de tracking")
        sms_result = await sms_test.send_tracking_sms(
            phone=test_phone,
            customer_name=test_customer_name,
            tracking_code=test_tracking_code,
            guide_number=test_guide_number
        )
        
        if sms_result["success"]:
            print("🎉 ¡PRUEBA EXITOSA!")
            print(f"   📱 Teléfono: {sms_result['phone']}")
            print(f"   🔍 Tracking: {sms_result['tracking_code']}")
        else:
            print("❌ Falló el envío del SMS")
            print(f"   Error: {sms_result.get('error', 'Error desconocido')}")
        
    except Exception as e:
        print(f"❌ Error durante las pruebas: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 Iniciando pruebas del servicio de SMS...")
    asyncio.run(main())
    print("\n" + "=" * 50)
    print("🏁 PRUEBAS COMPLETADAS")
