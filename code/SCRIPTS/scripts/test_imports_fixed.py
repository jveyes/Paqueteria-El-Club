#!/usr/bin/env python3
"""
Script de prueba de imports corregidos
Solución para todos los problemas de imports relativos
"""

import sys
import os
from pathlib import Path

# Agregar el directorio raíz del proyecto al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_all_imports():
    """Probar todos los imports principales"""
    print("🧪 PROBANDO TODOS LOS IMPORTS CORREGIDOS")
    print("=" * 50)
    
    imports_to_test = [
        # Configuración
        ("src.config", "settings"),
        
        # Base de datos
        ("src.database.database", "engine"),
        ("src.database.database", "get_db"),
        
        # Modelos
        ("src.models.user", "User"),
        ("src.models.package", "Package"),
        ("src.models.announcement", "PackageAnnouncement"),
        ("src.models.notification", "Notification"),
        
        # Servicios
        ("src.services.sms_service", "SMSService"),
        ("src.services.notification_service", "NotificationService"),
        ("src.services.user_service", "UserService"),
        ("src.services.package_service", "PackageService"),
        
        # Routers
        ("src.routers.auth", "router as auth_router"),
        ("src.routers.packages", "router as packages_router"),
        ("src.routers.announcements", "router as announcements_router"),
        
        # Utilidades
        ("src.utils.exceptions", "PaqueteriaException"),
        ("src.utils.auth", "verify_token"),
    ]
    
    results = []
    
    for module_path, item_name in imports_to_test:
        try:
            module = __import__(module_path, fromlist=[item_name])
            if hasattr(module, item_name):
                print(f"✅ {module_path}.{item_name}: OK")
                results.append(True)
            else:
                print(f"⚠️ {module_path}.{item_name}: Módulo OK, item no encontrado")
                results.append(False)
        except ImportError as e:
            print(f"❌ {module_path}.{item_name}: Error de import - {e}")
            results.append(False)
        except Exception as e:
            print(f"❌ {module_path}.{item_name}: Error inesperado - {e}")
            results.append(False)
    
    # Resumen
    print("\n" + "=" * 50)
    successful = sum(results)
    total = len(results)
    print(f"📊 RESUMEN: {successful}/{total} imports exitosos")
    
    if successful == total:
        print("🎉 ¡TODOS LOS IMPORTS FUNCIONAN CORRECTAMENTE!")
    else:
        print(f"⚠️ {total - successful} imports tienen problemas")
    
    return successful == total

def test_service_initialization():
    """Probar inicialización de servicios"""
    print("\n🔧 PROBANDO INICIALIZACIÓN DE SERVICIOS")
    print("=" * 50)
    
    try:
        from src.services.sms_service import SMSService
        from src.services.notification_service import NotificationService
        
        # Probar SMS Service
        sms_service = SMSService()
        print("✅ SMSService inicializado correctamente")
        
        # Probar Notification Service
        notification_service = NotificationService()
        print("✅ NotificationService inicializado correctamente")
        
        return True
        
    except Exception as e:
        print(f"❌ Error inicializando servicios: {e}")
        return False

def test_configuration():
    """Probar configuración"""
    print("\n⚙️ PROBANDO CONFIGURACIÓN")
    print("=" * 50)
    
    try:
        from src.config import settings
        
        print(f"✅ App Name: {settings.app_name}")
        print(f"✅ Version: {settings.app_version}")
        print(f"✅ Environment: {settings.environment}")
        print(f"✅ Database Host: {settings.postgres_host[:30]}...")
        print(f"✅ LIWA Account: {settings.liwa_account}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en configuración: {e}")
        return False

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBAS DE IMPORTS CORREGIDOS")
    print("=" * 60)
    
    # Ejecutar todas las pruebas
    imports_ok = test_all_imports()
    services_ok = test_service_initialization()
    config_ok = test_configuration()
    
    print("\n" + "=" * 60)
    print("🏁 RESULTADO FINAL DE LAS PRUEBAS")
    print("=" * 60)
    
    if imports_ok and services_ok and config_ok:
        print("🎉 ¡TODAS LAS PRUEBAS PASARON EXITOSAMENTE!")
        print("✅ Los imports relativos están corregidos")
        print("✅ Los servicios se inicializan correctamente")
        print("✅ La configuración se carga sin problemas")
    else:
        print("⚠️ Algunas pruebas fallaron:")
        print(f"   • Imports: {'✅' if imports_ok else '❌'}")
        print(f"   • Servicios: {'✅' if services_ok else '❌'}")
        print(f"   • Configuración: {'✅' if config_ok else '❌'}")
    
    print("\n💡 Si todas las pruebas pasaron, los scripts funcionarán correctamente")
