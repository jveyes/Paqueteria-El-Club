#!/usr/bin/env python3
"""
Script final para probar el formulario web después de las correcciones
"""

import sys
import os
import requests
import json
import time
from pathlib import Path

# Agregar el directorio raíz del proyecto al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_form_web_final():
    """Probar el formulario web después de las correcciones"""
    print("🌐 PRUEBA FINAL DEL FORMULARIO WEB")
    print("=" * 60)
    
    base_url = "http://localhost"
    
    # Datos de prueba
    test_data = {
        "customer_name": "PRUEBA FINAL WEB",
        "guide_number": f"WEBFINAL{int(time.time())}",
        "phone_number": "3002596319"
    }
    
    print(f"📝 Datos de prueba:")
    print(f"   • Nombre: {test_data['customer_name']}")
    print(f"   • Guía: {test_data['guide_number']}")
    print(f"   • Teléfono: {test_data['phone_number']}")
    print()
    
    try:
        # Paso 1: Enviar formulario
        print("📤 PASO 1: Enviando formulario web...")
        response = requests.post(
            f"{base_url}/api/announcements/",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"   📤 Respuesta: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Formulario enviado exitosamente")
            print(f"   • ID del anuncio: {result['id']}")
            print(f"   • Código de tracking: {result['tracking_code']}")
            print(f"   • Estado: {result['status']}")
            
            # Paso 2: Verificar creación del anuncio
            print("\n🔍 PASO 2: Verificando creación del anuncio...")
            time.sleep(2)
            
            verify_response = requests.get(f"{base_url}/api/announcements/guide/{test_data['guide_number']}")
            if verify_response.status_code == 200:
                verify_result = verify_response.json()
                print("✅ Anuncio verificado en la base de datos")
                print(f"   • Tracking: {verify_result['tracking_code']}")
                print(f"   • Estado: {verify_result['status']}")
            else:
                print(f"❌ Error verificando anuncio: {verify_response.status_code}")
            
            # Paso 3: Verificar envío de SMS
            print("\n📱 PASO 3: Verificando envío de SMS...")
            print("   🔍 Revisando logs del contenedor...")
            print("   💡 Buscar: 'SMS enviado exitosamente' en los logs")
            print("   💡 Buscar: 'Error específico en envío de SMS' en los logs")
            
            # Esperar para que se procese
            time.sleep(5)
            
            return True
            
        else:
            print(f"❌ Error enviando formulario: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def check_sms_logs_final():
    """Verificar logs de SMS después de las correcciones"""
    print("\n📋 VERIFICACIÓN FINAL DE LOGS DE SMS")
    print("=" * 50)
    
    print("🔍 Para verificar si el SMS se envió, ejecuta:")
    print("   docker logs paqueteria_v31_app --tail 50 | grep -E '(SMS|Error|ERROR|Exception|EXCEPTION)'")
    print()
    
    print("📱 Buscar estos patrones en los logs:")
    print("   ✅ ÉXITO: 'SMS enviado exitosamente a 573002596319'")
    print("   ❌ ERROR ESPECÍFICO: 'Error específico en envío de SMS:'")
    print("   ❌ ERROR GENERAL: 'Error general en servicio de notificaciones:'")
    print()
    
    print("🎯 Si ahora ves logs detallados de errores, el problema está identificado")
    print("🎯 Si el SMS se envía exitosamente, el problema está resuelto")

def main():
    """Función principal"""
    print("🚀 PRUEBA FINAL DEL FORMULARIO WEB DESPUÉS DE CORRECCIONES")
    print("=" * 80)
    
    # Probar formulario web
    success = test_form_web_final()
    
    if success:
        print("\n🎉 PRUEBA COMPLETADA")
        print("✅ El formulario se envió correctamente")
        print("✅ El anuncio se creó en la base de datos")
        print("✅ Ahora verificar si el SMS se envió")
        
        # Instrucciones para verificar logs
        check_sms_logs_final()
        
        print("\n💡 PRÓXIMOS PASOS:")
        print("   1. Revisar logs del contenedor para SMS")
        print("   2. Si hay errores detallados, el problema está identificado")
        print("   3. Si el SMS se envía, el problema está resuelto")
        
    else:
        print("\n❌ PRUEBA FALLIDA")
        print("🔧 Revisar logs del contenedor para más detalles")
    
    print("\n🏁 PRUEBA FINAL COMPLETADA")
    print("=" * 80)

if __name__ == "__main__":
    main()
