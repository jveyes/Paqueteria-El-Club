#!/usr/bin/env python3
"""
Script completo para probar el formulario con debugging detallado
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

def test_form_complete_debug():
    """Probar el formulario completo con debugging detallado"""
    print("🌐 PRUEBA COMPLETA DEL FORMULARIO CON DEBUGGING")
    print("=" * 70)
    
    base_url = "http://localhost"
    
    # Datos exactos como los enviaría el formulario
    test_data = {
        "customer_name": "PRUEBA DEBUG COMPLETA",
        "guide_number": f"DEBUG{int(time.time())}",
        "phone_number": "3002596319"
    }
    
    print(f"📝 Datos del formulario:")
    print(f"   • Nombre: {test_data['customer_name']}")
    print(f"   • Guía: {test_data['guide_number']}")
    print(f"   • Teléfono: {test_data['phone_number']}")
    print()
    
    try:
        # PASO 1: Crear anuncio (como hace el formulario)
        print("📤 PASO 1: Creando anuncio...")
        print("   📤 Enviando POST a /api/announcements/")
        
        response = requests.post(
            f"{base_url}/api/announcements/",
            json=test_data,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Referer": "http://localhost/customers/announce.html"
            }
        )
        
        print(f"   📤 Respuesta: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Anuncio creado exitosamente")
            print(f"   • ID del anuncio: {result['id']}")
            print(f"   • Código de tracking: {result['tracking_code']}")
            print(f"   • Estado: {result['status']}")
            
            # PASO 2: Enviar SMS (como hace el formulario)
            print("\n📱 PASO 2: Enviando SMS desde navegador...")
            print("   📤 Enviando POST a /api/announcements/send-sms-browser")
            
            sms_data = {
                "customer_name": result['customer_name'],
                "phone_number": result['phone_number'],
                "guide_number": result['guide_number'],
                "tracking_code": result['tracking_code']
            }
            
            print(f"   📱 Datos del SMS:")
            print(f"      • Cliente: {sms_data['customer_name']}")
            print(f"      • Teléfono: {sms_data['phone_number']}")
            print(f"      • Guía: {sms_data['guide_number']}")
            print(f"      • Tracking: {sms_data['tracking_code']}")
            
            sms_response = requests.post(
                f"{base_url}/api/announcements/send-sms-browser",
                json=sms_data,
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "Referer": "http://localhost/customers/announce.html"
                }
            )
            
            print(f"   📱 Respuesta SMS: {sms_response.status_code}")
            
            if sms_response.status_code == 200:
                sms_result = sms_response.json()
                print("✅ SMS enviado exitosamente")
                print(f"   • Resultado: {sms_result}")
                
                # PASO 3: Verificar envío real
                print("\n🔍 PASO 3: Verificando envío real de SMS...")
                print("   🔍 Revisando logs del contenedor...")
                print("   💡 Buscar: 'SMS enviado exitosamente desde navegador'")
                print("   💡 Buscar: 'SMS enviado exitosamente a 573002596319'")
                
                # Esperar para que se procese
                time.sleep(5)
                
                return True
                
            else:
                print(f"❌ Error enviando SMS: {sms_response.status_code}")
                print(f"   Respuesta: {sms_response.text}")
                return False
            
        else:
            print(f"❌ Error creando anuncio: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def verificar_logs_completos():
    """Verificar logs completos del contenedor"""
    print("\n📋 VERIFICACIÓN COMPLETA DE LOGS")
    print("=" * 50)
    
    print("🔍 Para verificar los logs completos, ejecuta:")
    print("   docker logs paqueteria_v31_app --tail 100 | grep -E '(SMS|Error|ERROR|Exception|EXCEPTION|navegador|DEBUG|POST.*announcements)'")
    print()
    
    print("📱 Buscar estos patrones en los logs:")
    print("   ✅ ÉXITO: 'SMS enviado exitosamente desde navegador'")
    print("   ✅ ÉXITO: 'SMS enviado exitosamente a 573002596319'")
    print("   ❌ ERROR: 'Error enviando SMS' o 'Exception'")
    print("   📤 POST: 'POST /api/announcements/ HTTP/1.1' 200 OK")
    print("   📱 SMS: 'POST /api/announcements/send-sms-browser HTTP/1.1' 200 OK")
    print()
    
    print("🎯 Si NO ves el log de SMS, el problema está en:")
    print("   1. El endpoint no se está llamando")
    print("   2. El servicio de SMS está fallando")
    print("   3. Hay un error en el procesamiento")

def main():
    """Función principal"""
    print("🚀 PRUEBA COMPLETA DEL FORMULARIO CON DEBUGGING")
    print("=" * 80)
    
    # Probar formulario completo
    success = test_form_complete_debug()
    
    if success:
        print("\n🎉 PRUEBA COMPLETADA")
        print("✅ El anuncio se creó correctamente")
        print("✅ El SMS se envió exitosamente")
        print("✅ Ahora verificar si el SMS llegó realmente")
        
        # Instrucciones para verificar logs
        verificar_logs_completos()
        
        print("\n💡 PRÓXIMOS PASOS:")
        print("   1. Revisar logs del contenedor para confirmar SMS")
        print("   2. Verificar si el SMS llegó al teléfono")
        print("   3. Si no llegó, el problema está en LIWA.co")
        
    else:
        print("\n❌ PRUEBA FALLIDA")
        print("🔧 Revisar logs del contenedor para más detalles")
    
    print("\n🏁 PRUEBA COMPLETADA")
    print("=" * 80)

if __name__ == "__main__":
    main()
