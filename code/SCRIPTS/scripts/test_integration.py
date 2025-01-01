#!/usr/bin/env python3
# ========================================
# PAQUETES EL CLUB v3.1 - Prueba de Integración SMS
# ========================================

import sys
import os
import asyncio

# Agregar el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from services.sms_service import SMSService

async def test_integration():
    """Probar la integración completa del servicio de SMS"""
    print("🔍 PRUEBA DE INTEGRACIÓN SMS - PAQUETES EL CLUB v3.1")
    print("=" * 60)
    
    # Crear instancia del servicio
    sms_service = SMSService()
    
    # Datos de prueba (simulando un anuncio real)
    test_data = {
        "phone": "3001234567",
        "customer_name": "María González",
        "tracking_code": "PAP2025010112345678",
        "guide_number": "GUIDE789"
    }
    
    print(f"📱 Datos de prueba:")
    print(f"   Teléfono: {test_data['phone']}")
    print(f"   Cliente: {test_data['customer_name']}")
    print(f"   Tracking: {test_data['tracking_code']}")
    print(f"   Guía: {test_data['guide_number']}")
    print("-" * 60)
    
    try:
        # Prueba 1: Formateo de número de teléfono
        print("🔧 PRUEBA 1: Formateo de número de teléfono")
        formatted_phone = sms_service._format_phone_number(test_data['phone'])
        expected = f"57{test_data['phone']}"
        print(f"   Entrada: {test_data['phone']}")
        print(f"   Salida: {formatted_phone}")
        print(f"   Esperado: {expected}")
        print(f"   ✅ Correcto" if formatted_phone == expected else "   ❌ Incorrecto")
        
        # Prueba 2: Autenticación con LIWA.co
        print("\n🔐 PRUEBA 2: Autenticación con LIWA.co")
        auth_result = await sms_service._authenticate()
        if auth_result:
            print("   ✅ Autenticación exitosa")
            print(f"   Token: {sms_service._auth_token[:50]}..." if sms_service._auth_token else "   No hay token")
        else:
            print("   ❌ Falló la autenticación")
            return
        
        # Prueba 3: Envío de SMS de tracking (simulando anuncio de paquete)
        print("\n📤 PRUEBA 3: Envío de SMS de tracking (ANUNCIO DE PAQUETE)")
        sms_result = await sms_service.send_tracking_sms(
            phone=test_data['phone'],
            customer_name=test_data['customer_name'],
            tracking_code=test_data['tracking_code'],
            guide_number=test_data['guide_number']
        )
        
        if sms_result["success"]:
            print("   ✅ SMS enviado exitosamente!")
            print(f"   📱 Teléfono: {sms_result['phone']}")
            print(f"   💬 Mensaje: {sms_result['message']}")
            print(f"   🔍 Tracking: {sms_result['tracking_code']}")
            print(f"   📦 Guía: {test_data['guide_number']}")
            
            # Simular lo que vería el cliente
            print("\n📱 SIMULACIÓN - Lo que recibe el cliente:")
            print(f"   {sms_result['message']}")
            
        else:
            print("   ❌ Falló el envío del SMS")
            print(f"   Error: {sms_result.get('error', 'Error desconocido')}")
        
        # Prueba 4: Envío de SMS de notificación (simulando cambio de estado)
        print("\n📤 PRUEBA 4: Envío de SMS de notificación (CAMBIO DE ESTADO)")
        notification_result = await sms_service.send_notification_sms(
            phone=test_data['phone'],
            message=f"Su paquete {test_data['guide_number']} ha sido recibido en nuestras instalaciones."
        )
        
        if notification_result["success"]:
            print("   ✅ SMS de notificación enviado exitosamente!")
            print(f"   📱 Teléfono: {notification_result['phone']}")
            print(f"   💬 Mensaje: {notification_result['message']}")
        else:
            print("   ❌ Falló el envío del SMS de notificación")
            print(f"   Error: {notification_result.get('error', 'Error desconocido')}")
        
    except Exception as e:
        print(f"❌ Error durante las pruebas: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Función principal"""
    print("🚀 Iniciando pruebas de integración...")
    
    # Ejecutar pruebas asíncronas
    asyncio.run(test_integration())
    
    print("\n" + "=" * 60)
    print("🏁 PRUEBAS DE INTEGRACIÓN COMPLETADAS")
    print("\n💡 Si todas las pruebas pasaron, la funcionalidad está lista para producción!")

if __name__ == "__main__":
    main()
