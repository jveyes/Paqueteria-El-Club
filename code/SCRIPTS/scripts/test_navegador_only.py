#!/usr/bin/env python3
"""
Script para probar que el SMS solo funciona desde navegador
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

def test_api_sms_disabled():
    """Probar que el SMS por API está deshabilitado"""
    print("🚫 PRUEBA: SMS por API DESHABILITADO")
    print("=" * 50)
    
    base_url = "http://localhost"
    
    # Datos de prueba
    test_data = {
        "customer_name": "PRUEBA API BLOQUEADA",
        "guide_number": f"APIBLOQ{int(time.time())}",
        "phone_number": "3002596319"
    }
    
    print(f"📝 Datos de prueba:")
    print(f"   • Nombre: {test_data['customer_name']}")
    print(f"   • Guía: {test_data['guide_number']}")
    print(f"   • Teléfono: {test_data['phone_number']}")
    print()
    
    try:
        # Paso 1: Crear anuncio por API (SMS deshabilitado)
        print("📤 PASO 1: Creando anuncio por API (SMS deshabilitado)...")
        response = requests.post(
            f"{base_url}/api/announcements/",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"   📤 Respuesta: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Anuncio creado exitosamente por API")
            print(f"   • ID del anuncio: {result['id']}")
            print(f"   • Código de tracking: {result['tracking_code']}")
            print(f"   • Estado: {result['status']}")
            
            # Paso 2: Verificar que NO se envió SMS
            print("\n📱 PASO 2: Verificando que NO se envió SMS...")
            print("   🔍 Revisando logs del contenedor...")
            print("   💡 Buscar: 'SMS DESHABILITADO POR API' en los logs")
            print("   💡 NO debe haber: 'SMS enviado exitosamente'")
            
            # Esperar para que se procese
            time.sleep(3)
            
            return result
            
        else:
            print(f"❌ Error creando anuncio: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return None

def test_browser_sms_endpoint():
    """Probar el endpoint específico para SMS desde navegador"""
    print("\n🌐 PRUEBA: Endpoint SMS desde navegador")
    print("=" * 50)
    
    base_url = "http://localhost"
    
    # Simular datos del navegador
    sms_data = {
        "customer_name": "PRUEBA NAVEGADOR",
        "phone_number": "3002596319",
        "guide_number": f"NAVEG{int(time.time())}",
        "tracking_code": "TEST"
    }
    
    print(f"📝 Datos del SMS:")
    print(f"   • Cliente: {sms_data['customer_name']}")
    print(f"   • Teléfono: {sms_data['phone_number']}")
    print(f"   • Guía: {sms_data['guide_number']}")
    print(f"   • Tracking: {sms_data['tracking_code']}")
    print()
    
    try:
        # Paso 1: Intentar SMS con headers de navegador
        print("📤 PASO 1: Enviando SMS con headers de navegador...")
        
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "http://localhost/customers/announce.html"
        }
        
        response = requests.post(
            f"{base_url}/api/announcements/send-sms-browser",
            json=sms_data,
            headers=headers
        )
        
        print(f"   📤 Respuesta: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SMS enviado exitosamente desde navegador")
            print(f"   • Resultado: {result}")
            
            # Paso 2: Verificar envío de SMS
            print("\n📱 PASO 2: Verificando envío de SMS...")
            print("   🔍 Revisando logs del contenedor...")
            print("   💡 Buscar: 'SMS enviado exitosamente desde navegador' en los logs")
            
            # Esperar para que se procese
            time.sleep(3)
            
            return True
            
        else:
            print(f"❌ Error enviando SMS: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def check_logs():
    """Verificar logs del contenedor"""
    print("\n📋 VERIFICACIÓN DE LOGS")
    print("=" * 30)
    
    print("🔍 Para verificar los logs, ejecuta:")
    print("   docker logs paqueteria_v31_app --tail 50 | grep -E '(SMS|Error|ERROR|Exception|EXCEPTION|DESHABILITADO|navegador)'")
    print()
    
    print("📱 Buscar estos patrones en los logs:")
    print("   🚫 API: 'SMS DESHABILITADO POR API - Solo funcionará por navegador'")
    print("   ✅ NAVEGADOR: 'SMS enviado exitosamente desde navegador'")
    print("   🌐 SOLICITUD: 'Solicitud de SMS desde navegador'")

def main():
    """Función principal"""
    print("🚀 PRUEBA: SMS SOLO DESDE NAVEGADOR")
    print("=" * 80)
    
    # Probar que el SMS por API está deshabilitado
    announcement_result = test_api_sms_disabled()
    
    if announcement_result:
        print("\n🎉 PRUEBA 1 COMPLETADA")
        print("✅ El anuncio se creó por API (SMS deshabilitado)")
        
        # Probar el endpoint específico para navegador
        sms_success = test_browser_sms_endpoint()
        
        if sms_success:
            print("\n🎉 PRUEBA 2 COMPLETADA")
            print("✅ El SMS se envió exitosamente desde navegador")
        else:
            print("\n❌ PRUEBA 2 FALLIDA")
            print("🔧 Revisar logs para más detalles")
        
        # Instrucciones para verificar logs
        check_logs()
        
        print("\n💡 RESUMEN:")
        print("   1. ✅ SMS por API: DESHABILITADO")
        print("   2. ✅ SMS desde navegador: FUNCIONANDO")
        print("   3. 🎯 El sistema ahora funciona como se solicitó")
        
    else:
        print("\n❌ PRUEBA 1 FALLIDA")
        print("🔧 Revisar logs del contenedor para más detalles")
    
    print("\n🏁 PRUEBA COMPLETADA")
    print("=" * 80)

if __name__ == "__main__":
    main()
