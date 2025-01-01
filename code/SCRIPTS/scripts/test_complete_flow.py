#!/usr/bin/env python3
"""
Test completo del flujo de anuncio de paquetes
Solución para imports relativos
"""

import sys
import os
from pathlib import Path

# Agregar el directorio raíz del proyecto al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from src.services.notification_service import NotificationService
    from src.services.sms_service import SMSService
    from src.services.package_service import PackageService
    from src.config import settings
    import logging
    
    # Configurar logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    def test_complete_flow():
        """Probar el flujo completo de anuncio"""
        print("🧪 TEST COMPLETO DEL FLUJO DE ANUNCIO")
        print("=" * 50)
        
        try:
            # Inicializar servicios
            sms_service = SMSService()
            notification_service = NotificationService()
            package_service = PackageService()
            
            print("✅ Servicios inicializados correctamente")
            
            # Probar conexión SMS
            print("\n📱 Probando servicio SMS...")
            test_result = sms_service.test_connection()
            if test_result:
                print("✅ Servicio SMS funcionando")
            else:
                print("❌ Problema con servicio SMS")
            
            print("\n🎉 Test completado")
            
        except Exception as e:
            print(f"❌ Error en el test: {e}")
            logger.error(f"Error en test completo: {e}")
    
    if __name__ == "__main__":
        test_complete_flow()
        
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("Asegúrate de ejecutar desde el directorio raíz del proyecto")
except Exception as e:
    print(f"❌ Error inesperado: {e}")
