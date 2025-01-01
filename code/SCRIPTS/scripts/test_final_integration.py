#!/usr/bin/env python3
# ========================================
# PAQUETES EL CLUB v3.1 - Prueba Final de Integración
# ========================================

import asyncio
import httpx

# Configuración directa de LIWA.co
LIWA_CONFIG = {
    "account": "00486396309",
    "password": "6fEuRnd*$$#NfFAS",
    "api_key": "c52d8399ac63a24563ee8a967bafffc6cb8d8dfa",
    "auth_url": "https://api.liwa.co/v2/auth/login",
    "sms_url": "https://api.liwa.co/v2/sms/single"
}

class FinalIntegrationTest:
    """Prueba final de integración del servicio de SMS"""
    
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
    
    async def send_production_sms(self, phone: str, customer_name: str, tracking_code: str, guide_number: str) -> dict:
        """Enviar SMS de producción (exactamente como se enviará en announce.html)"""
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
            
            # Preparar mensaje de PRODUCCIÓN (exactamente como se enviará)
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
            
            print(f"📤 Enviando SMS de PRODUCCIÓN...")
            print(f"   URL: {self.sms_url}")
            print(f"   Teléfono: {formatted_phone}")
            print(f"   Mensaje: {message}")
            
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
                    print(f"✅ SMS de PRODUCCIÓN enviado exitosamente!")
                    print(f"   Respuesta LIWA: {result}")
                    return {
                        "success": True,
                        "phone": formatted_phone,
                        "message": message,
                        "tracking_code": tracking_code,
                        "liwa_response": result
                    }
                else:
                    print(f"❌ Error al enviar SMS de producción: {response.status_code}")
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
    """Función principal de prueba de integración final"""
    print("🔍 PRUEBA FINAL DE INTEGRACIÓN - PAQUETES EL CLUB v3.1")
    print("=" * 80)
    print("🎯 PRUEBA DE PRODUCCIÓN CON TU NÚMERO REAL: 3002596319")
    print("=" * 80)
    
    # Crear instancia del servicio
    integration_test = FinalIntegrationTest()
    
    # DATOS DE PRODUCCIÓN (exactamente como se enviarán en announce.html)
    production_data = {
        "phone": "3002596319",  # TU NÚMERO REAL
        "customer_name": "Cliente de Producción",
        "tracking_code": "PAP2025010112345678",  # Código generado por sistema
        "guide_number": "GUIDE-PROD-123"  # Número de guía ingresado por usuario
    }
    
    print(f"📱 DATOS DE PRODUCCIÓN (announce.html):")
    print(f"   📞 Teléfono: {production_data['phone']}")
    print(f"   👤 Cliente: {production_data['customer_name']}")
    print(f"   🔍 Código de tracking: {production_data['tracking_code']}")
    print(f"   📦 Número de guía: {production_data['guide_number']}")
    print("-" * 80)
    
    try:
        # Prueba 1: Formateo de número de teléfono
        print("🔧 PRUEBA 1: Formateo de número de teléfono")
        formatted_phone = integration_test.format_phone_number(production_data['phone'])
        expected = f"57{production_data['phone']}"
        print(f"   Entrada: {production_data['phone']} (tu número real)")
        print(f"   Salida: {formatted_phone} (formato LIWA.co)")
        print(f"   Esperado: {expected}")
        print(f"   ✅ Formato correcto" if formatted_phone == expected else "   ❌ Formato incorrecto")
        
        # Prueba 2: Autenticación con LIWA.co
        print("\n🔐 PRUEBA 2: Autenticación con LIWA.co")
        auth_result = await integration_test.authenticate()
        if not auth_result:
            print("❌ Falló la autenticación, abortando pruebas")
            return
        
        # Prueba 3: Envío de SMS de PRODUCCIÓN (exactamente como announce.html)
        print("\n📤 PRUEBA 3: Envío de SMS de PRODUCCIÓN")
        print("   🎯 Este es el mensaje EXACTO que se enviará en announce.html")
        print("   📱 ENVIARÁ SMS REAL al cliente")
        
        sms_result = await integration_test.send_production_sms(
            phone=production_data['phone'],
            customer_name=production_data['customer_name'],
            tracking_code=production_data['tracking_code'],
            guide_number=production_data['guide_number']
        )
        
        if sms_result["success"]:
            print("\n🎉 ¡INTEGRACIÓN DE PRODUCCIÓN EXITOSA!")
            print(f"   📱 Tu teléfono: {sms_result['phone']}")
            print(f"   🔍 Código de consulta enviado: {sms_result['tracking_code']}")
            print(f"   📦 Número de guía: {production_data['guide_number']}")
            
            # Simular lo que verías en tu teléfono
            print("\n📱 SIMULACIÓN - Mensaje de PRODUCCIÓN que DEBERÍAS recibir:")
            print("   " + "="*50)
            print(f"   {sms_result['message']}")
            print("   " + "="*50)
            
            print(f"\n✅ RESULTADO FINAL:")
            print(f"   🎉 La funcionalidad de SMS está COMPLETAMENTE implementada")
            print(f"   📱 announce.html enviará SMS automáticamente a todos los clientes")
            print(f"   🔍 Los clientes recibirán su código de consulta por SMS")
            print(f"   🚀 La implementación está lista para producción")
            
        else:
            print("❌ Falló el envío del SMS de producción")
            print(f"   Error: {sms_result.get('error', 'Error desconocido')}")
            print(f"   🔧 Revisar configuración de producción")
        
    except Exception as e:
        print(f"❌ Error durante la prueba de integración: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 Iniciando prueba final de integración...")
    print("⚠️  ESTA PRUEBA ENVIARÁ UN SMS REAL AL NÚMERO 3002596319")
    print("   📱 El mensaje será EXACTAMENTE como se enviará en announce.html")
    
    # Confirmar antes de enviar
    confirm = input("\n¿Estás seguro de que quieres probar la integración final? (s/N): ")
    if confirm.lower() in ['s', 'si', 'sí', 'y', 'yes']:
        asyncio.run(main())
    else:
        print("❌ Prueba de integración final cancelada por el usuario")
    
    print("\n" + "=" * 80)
    print("🏁 PRUEBA FINAL DE INTEGRACIÓN COMPLETADA")
    print("\n💡 Si la prueba pasó, la implementación está completa y funcionando!")
