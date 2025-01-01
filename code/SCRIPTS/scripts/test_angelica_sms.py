#!/usr/bin/env python3
"""
Script para probar específicamente el SMS del anuncio de ANGELICA ARRAZOLA
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

def test_angelica_sms():
    """Probar el SMS del anuncio de ANGELICA ARRAZOLA"""
    print("👩 PROBANDO SMS DEL ANUNCIO DE ANGELICA ARRAZOLA")
    print("=" * 70)
    
    base_url = "http://localhost"
    
    # Datos exactos del anuncio de ANGELICA
    angelica_data = {
        "customer_name": "ANGELICA ARRAZOLA",
        "guide_number": f"ANGELICA{int(time.time())}",
        "phone_number": "3002596319"
    }
    
    print(f"📝 Datos del anuncio:")
    print(f"   • Nombre: {angelica_data['customer_name']}")
    print(f"   • Guía: {angelica_data['guide_number']}")
    print(f"   • Teléfono: {angelica_data['phone_number']}")
    print()
    
    try:
        # Paso 1: Enviar formulario
        print("📤 PASO 1: Enviando formulario...")
        response = requests.post(
            f"{base_url}/api/announcements/",
            json=angelica_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"   📤 Respuesta: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Formulario enviado exitosamente")
            print(f"   • ID del anuncio: {result['id']}")
            print(f"   • Código de tracking: {result['tracking_code']}")
            print(f"   • Estado: {result['status']}")
            
            # Paso 2: Verificar que el anuncio se creó
            print("\n🔍 PASO 2: Verificando creación del anuncio...")
            time.sleep(1)
            
            verify_response = requests.get(f"{base_url}/api/announcements/guide/{angelica_data['guide_number']}")
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
            print("   💡 Buscar: 'Error enviando SMS' en los logs")
            
            # Esperar un momento para que se procese
            time.sleep(3)
            
            return True
            
        else:
            print(f"❌ Error enviando formulario: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def check_sms_logs():
    """Verificar logs de SMS"""
    print("\n📋 VERIFICACIÓN DE LOGS DE SMS")
    print("=" * 50)
    
    print("🔍 Para verificar si el SMS se envió, ejecuta:")
    print("   docker logs paqueteria_v31_app --tail 50 | grep -E '(SMS|Error|ERROR|Exception|EXCEPTION)'")
    print()
    
    print("📱 Buscar estos patrones en los logs:")
    print("   ✅ ÉXITO: 'SMS enviado exitosamente a 573002596319'")
    print("   ❌ ERROR: 'Error enviando SMS:'")
    print("   ❌ EXCEPCIÓN: 'Exception' o 'Error'")
    print()
    
    print("🎯 Si NO ves el log de SMS, el problema está en:")
    print("   1. Servicio de notificaciones fallando silenciosamente")
    print("   2. Error en la importación del servicio")
    print("   3. Error en la creación del objeto temporal")
    print("   4. Error en la llamada al método de envío")

def main():
    """Función principal"""
    print("🚀 PRUEBA ESPECÍFICA DEL SMS DE ANGELICA ARRAZOLA")
    print("=" * 80)
    
    # Probar SMS de ANGELICA
    success = test_angelica_sms()
    
    if success:
        print("\n🎉 PRUEBA COMPLETADA")
        print("✅ El formulario se envió correctamente")
        print("✅ El anuncio se creó en la base de datos")
        print("✅ Ahora verificar si el SMS se envió")
        
        # Instrucciones para verificar logs
        check_sms_logs()
        
        print("\n💡 PRÓXIMOS PASOS:")
        print("   1. Revisar logs del contenedor para SMS")
        print("   2. Si NO hay log de SMS, hay un error silencioso")
        print("   3. Si SÍ hay log de SMS, el problema está resuelto")
        
    else:
        print("\n❌ PRUEBA FALLIDA")
        print("🔧 Revisar logs del contenedor para más detalles")
    
    print("\n🏁 PRUEBA COMPLETADA")
    print("=" * 80)

if __name__ == "__main__":
    main()
