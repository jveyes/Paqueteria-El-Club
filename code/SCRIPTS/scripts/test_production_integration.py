#!/usr/bin/env python3
# ========================================
# PAQUETES EL CLUB v3.1 - Prueba de Integración de Producción
# ========================================

import sys
import os
import asyncio

# Agregar el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from services.notification_service import NotificationService
from services.sms_service import SMSService

class MockPackage:
    """Paquete simulado para pruebas de producción"""
    def __init__(self, tracking_number, customer_name, customer_phone, tracking_code):
        self.id = "prod-test-456"
        self.tracking_number = tracking_number
        self.customer_name = customer_name
        self.customer_phone = customer_phone
        self.tracking_code = tracking_code

class MockDatabase:
    """Base de datos simulada para pruebas de producción"""
    def __init__(self):
        self.notifications = []
    
    def add(self, notification):
        self.notifications.append(notification)
        print(f"📝 Notificación agregada a BD: {notification.notification_type}")
    
    def commit(self):
        print("💾 Cambios guardados en BD")
    
    def refresh(self, notification):
        print(f"🔄 Notificación refrescada: {notification.id}")

async def test_production_integration():
    """Probar la integración completa de producción"""
    print("🔍 PRUEBA DE INTEGRACIÓN DE PRODUCCIÓN - PAQUETES EL CLUB v3.1")
    print("=" * 80)
    print("🎯 Esta prueba simula EXACTAMENTE el flujo de announce.html en producción")
    print("=" * 80)
    
    # Crear base de datos simulada
    mock_db = MockDatabase()
    
    # Crear servicio de notificaciones
    notification_service = NotificationService(mock_db)
    
    # DATOS REALES DE PRUEBA (simulando formulario de announce.html)
    test_data = {
        "tracking_number": "GUIDE-PROD-789",  # Número de guía ingresado por usuario
        "customer_name": "María González",
        "customer_phone": "3002596319",  # NÚMERO REAL DEL USUARIO
        "tracking_code": "PAP2025010112345678"  # Código generado por sistema
    }
    
    print(f"📱 DATOS DEL FORMULARIO (announce.html en producción):")
    print(f"   📦 Número de guía: {test_data['tracking_number']}")
    print(f"   👤 Nombre del cliente: {test_data['customer_name']}")
    print(f"   📞 Teléfono: {test_data['customer_phone']}")
    print(f"   🔍 Código de tracking: {test_data['tracking_code']}")
    print("-" * 80)
    
    try:
        # Crear paquete simulado
        mock_package = MockPackage(
            tracking_number=test_data['tracking_number'],
            customer_name=test_data['customer_name'],
            customer_phone=test_data['customer_phone'],
            tracking_code=test_data['tracking_code']
        )
        
        print("🔧 PASO 1: Creando paquete simulado...")
        print(f"   ✅ Paquete creado con ID: {mock_package.id}")
        
        # Prueba del flujo completo: anuncio de paquete (PRODUCCIÓN)
        print("\n📤 PASO 2: Ejecutando send_package_announcement()...")
        print("   🎯 Este es el método que se ejecuta automáticamente en announce.html")
        print("   📱 ENVIARÁ SMS REAL al cliente")
        
        notification = await notification_service.send_package_announcement(mock_package)
        
        print(f"\n📊 RESULTADO DE LA NOTIFICACIÓN:")
        print(f"   ID: {notification.id}")
        print(f"   Tipo: {notification.notification_type}")
        print(f"   Estado: {notification.status}")
        print(f"   Mensaje: {notification.message}")
        
        if notification.status.value == "SENT":
            print("   ✅ SMS enviado exitosamente!")
            print(f"   📱 El cliente recibió su código de consulta")
            print(f"   🎉 ¡FUNCIONALIDAD DE PRODUCCIÓN FUNCIONANDO!")
        elif notification.status.value == "FAILED":
            print("   ❌ Falló el envío del SMS")
            print(f"   Error: {notification.error_message}")
            print(f"   🔧 Revisar configuración de producción")
        else:
            print(f"   ⚠️ Estado inesperado: {notification.status.value}")
        
        # Mostrar notificaciones en BD
        print(f"\n📝 NOTIFICACIONES EN BASE DE DATOS:")
        for i, notif in enumerate(mock_db.notifications, 1):
            print(f"   {i}. ID: {notif.id}, Estado: {notif.status}, Tipo: {notif.notification_type}")
        
        # Verificar que el SMS se envió realmente
        print(f"\n🔍 VERIFICACIÓN FINAL DE PRODUCCIÓN:")
        if notification.status.value == "SENT":
            print("   🎉 ¡INTEGRACIÓN DE PRODUCCIÓN EXITOSA!")
            print("   📱 El cliente recibió el SMS con su código de consulta")
            print("   🔍 El código de tracking está disponible para consultas")
            print("   💡 announce.html enviará SMS automáticamente a todos los clientes")
            print("   🚀 La funcionalidad está lista para producción")
        else:
            print("   ❌ La integración de producción no se completó correctamente")
            print("   🔧 Revisar logs y configuración")
        
    except Exception as e:
        print(f"❌ Error durante la prueba de producción: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Función principal"""
    print("🚀 Iniciando prueba de integración de producción...")
    print("⚠️  ESTA PRUEBA ENVIARÁ UN SMS REAL AL NÚMERO 3002596319")
    
    # Confirmar antes de enviar
    confirm = input("\n¿Estás seguro de que quieres probar la integración de producción? (s/N): ")
    if confirm.lower() in ['s', 'si', 'sí', 'y', 'yes']:
        asyncio.run(test_production_integration())
    else:
        print("❌ Prueba de producción cancelada por el usuario")
    
    print("\n" + "=" * 80)
    print("🏁 PRUEBA DE INTEGRACIÓN DE PRODUCCIÓN FINALIZADA")
    print("\n💡 Si la prueba pasó, announce.html enviará SMS automáticamente en producción!")

if __name__ == "__main__":
    main()
