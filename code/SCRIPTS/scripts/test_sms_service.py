#!/usr/bin/env python3
# ========================================
# PAQUETES EL CLUB v3.1 - Prueba del Servicio de SMS
# ========================================

import sys
import os
import asyncio

# Agregar el directorio src al path para importar módulos
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from services.sms_service import SMSService

async def test_sms_service():
    """Probar el servicio de SMS"""
    print("🔍 PRUEBA DEL SERVICIO DE SMS - PAQUETES EL CLUB v3.1")
    print("=" * 60)
    
    # Crear instancia del servicio
    sms_service = SMSService()
    
    # Datos de prueba
    test_phone = "3001234567"  # Número de 10 dígitos
    test_customer_name = "Juan Pérez"
    test_tracking_code = "TRK123"
    test_guide_number = "GUIDE456"
    
    print(f"📱 Número de prueba: {test_phone}")
    print(f"👤 Cliente: {test_customer_name}")
    print(f"🔍 Código de tracking: {test_tracking_code}")
    print(f"📦 Número de guía: {test_guide_number}")
    print("-" * 60)
    
    try:
        # Prueba 1: Formateo de número de teléfono
        print("🔧 PRUEBA 1: Formateo de número de teléfono")
        formatted_phone = sms_service._format_phone_number(test_phone)
        print(f"✅ Número formateado: {formatted_phone}")
        print(f"   Formato esperado: 57{test_phone}")
        print(f"   Formato correcto: {'✅' if formatted_phone == f'57{test_phone}' else '❌'}")
        
        # Prueba 2: Autenticación con LIWA.co
        print("\n🔐 PRUEBA 2: Autenticación con LIWA.co")
        auth_result = await sms_service._authenticate()
        if auth_result:
            print("✅ Autenticación exitosa")
            print(f"   Token: {sms_service._auth_token[:50]}..." if sms_service._auth_token else "   No hay token")
        else:
            print("❌ Falló la autenticación")
            return
        
        # Prueba 3: Envío de SMS de tracking
        print("\n📤 PRUEBA 3: Envío de SMS de tracking")
        sms_result = await sms_service.send_tracking_sms(
            phone=test_phone,
            customer_name=test_customer_name,
            tracking_code=test_tracking_code,
            guide_number=test_guide_number
        )
        
        if sms_result["success"]:
            print("✅ SMS enviado exitosamente!")
            print(f"   📱 Teléfono: {sms_result['phone']}")
            print(f"   💬 Mensaje: {sms_result['message']}")
            print(f"   🔍 Tracking: {sms_result['tracking_code']}")
        else:
            print("❌ Falló el envío del SMS")
            print(f"   Error: {sms_result.get('error', 'Error desconocido')}")
        
        # Prueba 4: Envío de SMS de notificación
        print("\n📤 PRUEBA 4: Envío de SMS de notificación")
        notification_result = await sms_service.send_notification_sms(
            phone=test_phone,
            message="Prueba de notificación - PAQUETES EL CLUB"
        )
        
        if notification_result["success"]:
            print("✅ SMS de notificación enviado exitosamente!")
            print(f"   📱 Teléfono: {notification_result['phone']}")
        else:
            print("❌ Falló el envío del SMS de notificación")
            print(f"   Error: {notification_result.get('error', 'Error desconocido')}")
        
    except Exception as e:
        print(f"❌ Error durante las pruebas: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Función principal"""
    print("🚀 Iniciando pruebas del servicio de SMS...")
    
    # Ejecutar pruebas asíncronas
    asyncio.run(test_sms_service())
    
    print("\n" + "=" * 60)
    print("🏁 PRUEBAS COMPLETADAS")

if __name__ == "__main__":
    main()
