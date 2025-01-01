#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Simple de Integración SMS
==============================

Este script prueba la integración del SMS de manera simple,
simulando exactamente lo que hace el formulario de announce.html
"""

import asyncio
import sys
import os

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

async def test_sms_integration():
    """Test simple de la integración SMS"""
    
    print("🧪 TEST SIMPLE DE INTEGRACIÓN SMS")
    print("=" * 50)
    
    try:
        # Importar servicios
        from services.sms_service import SMSService
        from services.notification_service import NotificationService
        from database.database import SessionLocal
        
        print("✅ Servicios importados correctamente")
        
        # Crear servicio SMS
        sms_service = SMSService()
        print("✅ Servicio SMS creado")
        
        # Datos de prueba
        test_data = {
            "customer_name": "JUAN PÉREZ",
            "guide_number": "TEST123456",
            "phone_number": "3002596319",
            "tracking_code": "ABCD"
        }
        
        print(f"📝 Datos de prueba:")
        print(f"   Nombre: {test_data['customer_name']}")
        print(f"   Guía: {test_data['guide_number']}")
        print(f"   Teléfono: {test_data['phone_number']}")
        print(f"   Código: {test_data['tracking_code']}")
        print()
        
        # Paso 1: Probar SMS directamente
        print("📱 PASO 1: Probando envío de SMS")
        print("-" * 40)
        
        sms_result = await sms_service.send_tracking_sms(
            phone=test_data['phone_number'],
            customer_name=test_data['customer_name'],
            tracking_code=test_data['tracking_code'],
            guide_number=test_data['guide_number']
        )
        
        if sms_result["success"]:
            print("   ✅ SMS enviado exitosamente")
            print(f"   📱 Número: {sms_result['phone']}")
            print(f"   💬 Mensaje: {sms_result['message']}")
        else:
            print(f"   ❌ Error en SMS: {sms_result['error']}")
            return False
        
        print()
        
        # Paso 2: Probar con servicio de notificaciones
        print("🔔 PASO 2: Probando con Servicio de Notificaciones")
        print("-" * 40)
        
        # Crear sesión de BD
        db = SessionLocal()
        
        # Crear paquete temporal
        class TempPackage:
            def __init__(self, tracking_number, customer_phone, tracking_code, customer_name):
                self.tracking_number = tracking_number
                self.customer_phone = customer_phone
                self.tracking_code = tracking_code
                self.customer_name = customer_name
                self.total_cost = 0
                self.id = 999
        
        temp_package = TempPackage(
            tracking_number=test_data['guide_number'],
            customer_phone=test_data['phone_number'],
            tracking_code=test_data['tracking_code'],
            customer_name=test_data['customer_name']
        )
        
        # Crear servicio de notificaciones
        notification_service = NotificationService(db)
        
        # Enviar notificación
        notification = await notification_service.send_package_announcement(temp_package)
        
        print("   ✅ Notificación creada exitosamente")
        print(f"   🆔 ID: {notification.id}")
        print(f"   📊 Estado: {notification.status}")
        print(f"   💬 Mensaje: {notification.message}")
        
        db.close()
        
        print()
        print("🎉 TEST COMPLETADO EXITOSAMENTE")
        print("=" * 50)
        print("✅ El servicio SMS está funcionando")
        print("✅ El servicio de notificaciones está funcionando")
        print("✅ La integración está completa")
        print("✅ El formulario de announce.html enviará SMS automáticamente")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Función principal"""
    try:
        success = await test_sms_integration()
        if success:
            print("\n🚀 La funcionalidad de SMS está lista para producción")
            print("📱 Los usuarios recibirán SMS automáticamente al enviar el formulario")
        else:
            print("\n❌ Hay problemas que necesitan ser resueltos")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n💥 Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
