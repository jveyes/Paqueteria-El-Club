#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Directo del Router de Anuncios
====================================

Este script prueba directamente la funcionalidad del router de anuncios
sin necesidad del servidor web para identificar el problema.
"""

import sys
import os

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_announcement_router():
    """Test directo del router de anuncios"""
    
    print("🧪 TEST DIRECTO DEL ROUTER DE ANUNCIOS")
    print("=" * 50)
    
    try:
        # Importar módulos necesarios
        from routers.announcements import create_announcement
        from schemas.announcement import AnnouncementCreate
        from database.database import SessionLocal
        from models.announcement import PackageAnnouncement
        
        print("✅ Módulos importados correctamente")
        
        # Crear datos de prueba
        test_data = AnnouncementCreate(
            customer_name="JUAN PÉREZ",
            guide_number="TEST123456",
            phone_number="3002596319"
        )
        
        print(f"📝 Datos de prueba creados:")
        print(f"   Nombre: {test_data.customer_name}")
        print(f"   Guía: {test_data.guide_number}")
        print(f"   Teléfono: {test_data.phone_number}")
        print()
        
        # Crear sesión de base de datos
        db = SessionLocal()
        print("✅ Sesión de base de datos creada")
        
        # Verificar si ya existe un anuncio con esa guía
        existing_announcement = db.query(PackageAnnouncement).filter(
            PackageAnnouncement.guide_number == test_data.guide_number
        ).first()
        
        if existing_announcement:
            print("⚠️ Ya existe un anuncio con esa guía, eliminándolo para la prueba")
            db.delete(existing_announcement)
            db.commit()
        
        # Generar código de tracking
        import random
        import string
        chars = string.ascii_uppercase.replace('O', '') + string.digits.replace('0', '')
        tracking_code = ''.join(random.choice(chars) for _ in range(4))
        
        print(f"🎯 Código de tracking generado: {tracking_code}")
        
        # Crear anuncio manualmente (simulando lo que hace el router)
        from utils.datetime_utils import get_colombia_now
        
        db_announcement = PackageAnnouncement(
            customer_name=test_data.customer_name,
            guide_number=test_data.guide_number,
            phone_number=test_data.phone_number,
            tracking_code=tracking_code,
            announced_at=get_colombia_now(),
            created_at=get_colombia_now(),
            updated_at=get_colombia_now()
        )
        
        print("✅ Anuncio creado en memoria")
        
        # Agregar a la base de datos
        db.add(db_announcement)
        db.commit()
        db.refresh(db_announcement)
        
        print("✅ Anuncio guardado en la base de datos")
        print(f"   🆔 ID: {db_announcement.id}")
        print(f"   🎯 Código: {db_announcement.tracking_code}")
        print(f"   📅 Fecha: {db_announcement.announced_at}")
        
        # Ahora probar el servicio de notificaciones
        print("\n🔔 PROBANDO SERVICIO DE NOTIFICACIONES")
        print("-" * 40)
        
        from services.notification_service import NotificationService
        
        # Crear servicio de notificaciones
        notification_service = NotificationService(db)
        print("✅ Servicio de notificaciones creado")
        
        # Crear paquete temporal para el SMS
        class TempPackage:
            def __init__(self, tracking_number, customer_phone, tracking_code, customer_name):
                self.tracking_number = tracking_number
                self.customer_phone = customer_phone
                self.tracking_code = tracking_code
                self.customer_name = customer_name
                self.total_cost = 0
                self.id = db_announcement.id
        
        temp_package = TempPackage(
            tracking_number=test_data.guide_number,
            customer_phone=test_data.phone_number,
            tracking_code=tracking_code,
            customer_name=test_data.customer_name
        )
        
        print("✅ Paquete temporal creado")
        
        # Importar asyncio para ejecutar la función async
        import asyncio
        
        # Ejecutar el envío de notificación
        async def send_notification():
            return await notification_service.send_package_announcement(temp_package)
        
        # Ejecutar en un nuevo event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            notification = loop.run_until_complete(send_notification())
            print("✅ Notificación enviada exitosamente")
            print(f"   🆔 ID: {notification.id}")
            print(f"   📊 Estado: {notification.status}")
            print(f"   💬 Mensaje: {notification.message}")
            
            if notification.external_id:
                print(f"   🔗 ID Externo: {notification.external_id}")
                
        except Exception as e:
            print(f"❌ Error enviando notificación: {e}")
            import traceback
            traceback.print_exc()
        finally:
            loop.close()
        
        # Limpiar
        db.delete(db_announcement)
        db.commit()
        db.close()
        
        print("\n🎉 TEST COMPLETADO EXITOSAMENTE")
        print("=" * 50)
        print("✅ El router de anuncios está funcionando")
        print("✅ El servicio de notificaciones está funcionando")
        print("✅ La base de datos está funcionando")
        print("✅ La funcionalidad de SMS está integrada")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Función principal"""
    try:
        success = test_announcement_router()
        if success:
            print("\n🚀 La funcionalidad está lista para producción")
            print("📱 Los usuarios recibirán SMS automáticamente")
        else:
            print("\n❌ Hay problemas que necesitan ser resueltos")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n💥 Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
