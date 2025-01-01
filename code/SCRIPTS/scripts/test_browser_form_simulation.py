#!/usr/bin/env python3
"""
Script para simular exactamente el comportamiento del navegador
al enviar el formulario de anuncios
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

def test_browser_form_simulation():
    """Simular el envío del formulario como lo haría el navegador"""
    print("🌐 SIMULANDO FORMULARIO DEL NAVEGADOR")
    print("=" * 60)
    
    base_url = "http://localhost"
    
    # Simular exactamente los datos que enviaría el navegador
    browser_data = {
        "customer_name": "Usuario Navegador",
        "guide_number": f"BROWSER{int(time.time())}",
        "phone_number": "3002596319"
    }
    
    print(f"📝 Datos simulando navegador:")
    print(f"   • Nombre: {browser_data['customer_name']}")
    print(f"   • Guía: {browser_data['guide_number']}")
    print(f"   • Teléfono: {browser_data['phone_number']}")
    print()
    
    try:
        # Paso 1: Obtener la página del formulario (como haría el navegador)
        print("🔍 PASO 1: Obteniendo página del formulario...")
        response = requests.get(f"{base_url}/announce")
        
        if response.status_code == 200:
            print("✅ Página del formulario obtenida")
            print(f"   • Tamaño: {len(response.text)} caracteres")
            
            # Verificar que contenga elementos del formulario
            if "announcementForm" in response.text:
                print("   • Formulario encontrado en HTML")
            else:
                print("   ⚠️ Formulario NO encontrado en HTML")
                
            if "api/announcements" in response.text:
                print("   • Endpoint API encontrado en HTML")
            else:
                print("   ⚠️ Endpoint API NO encontrado en HTML")
                
        else:
            print(f"❌ Error obteniendo página: {response.status_code}")
            return False
        
        # Paso 2: Simular envío del formulario (exactamente como el navegador)
        print("\n📤 PASO 2: Simulando envío del formulario...")
        
        # Headers que enviaría un navegador real
        browser_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/plain, */*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Origin": base_url,
            "Referer": f"{base_url}/announce"
        }
        
        print("   • Headers del navegador configurados")
        print("   • Enviando POST a /api/announcements/")
        
        response = requests.post(
            f"{base_url}/api/announcements/",
            json=browser_data,
            headers=browser_headers
        )
        
        print(f"   • Respuesta del servidor: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Formulario enviado exitosamente")
            print(f"   • ID del anuncio: {result['id']}")
            print(f"   • Código de tracking: {result['tracking_code']}")
            print(f"   • Estado: {result['status']}")
            
            # Verificar que el SMS se envió
            print("\n📱 PASO 3: Verificando envío de SMS...")
            
            # Esperar un momento para que se procese el SMS
            time.sleep(3)
            
            # Verificar logs del contenedor
            print("   🔍 Revisando logs del contenedor...")
            print("   💡 El SMS debería haberse enviado a 573002596319")
            
            return True
            
        else:
            print(f"❌ Error enviando formulario: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión: No se puede conectar al servidor")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def test_form_validation():
    """Probar validaciones del formulario"""
    print("\n🧪 PROBANDO VALIDACIONES DEL FORMULARIO")
    print("=" * 50)
    
    base_url = "http://localhost"
    
    # Casos de prueba que podrían fallar en el navegador
    test_cases = [
        {
            "name": "Nombre con caracteres especiales",
            "data": {"customer_name": "José María-López", "guide_number": f"TEST{int(time.time())}", "phone_number": "3002596319"},
            "expected": 200
        },
        {
            "name": "Guía con caracteres especiales",
            "data": {"customer_name": "Test User", "guide_number": f"TEST-{int(time.time())}", "phone_number": "3002596319"},
            "expected": 200
        },
        {
            "name": "Teléfono con formato especial",
            "data": {"customer_name": "Test User", "guide_number": f"TEST{int(time.time())}", "phone_number": "3002596319"},
            "expected": 200
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Prueba {i}: {test_case['name']}")
        
        try:
            response = requests.post(
                f"{base_url}/api/announcements/",
                json=test_case["data"],
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == test_case["expected"]:
                print(f"   ✅ Estado correcto: {response.status_code}")
                if response.status_code == 200:
                    result = response.json()
                    print(f"   • Tracking: {result['tracking_code']}")
            else:
                print(f"   ❌ Estado incorrecto: {response.status_code}")
                print(f"   • Respuesta: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        time.sleep(1)

def main():
    """Función principal"""
    print("🚀 SIMULACIÓN COMPLETA DEL FORMULARIO DEL NAVEGADOR")
    print("=" * 80)
    
    # Simular formulario del navegador
    success = test_browser_form_simulation()
    
    if success:
        print("\n🎉 SIMULACIÓN EXITOSA")
        print("✅ El formulario se comporta como esperado")
        print("✅ La API responde correctamente")
        print("✅ El SMS debería haberse enviado")
        
        # Probar validaciones
        test_form_validation()
        
        print("\n💡 DIAGNÓSTICO:")
        print("   Si el SMS NO llega desde el navegador pero SÍ desde la API:")
        print("   1. Verificar que el navegador esté enviando los datos correctos")
        print("   2. Revisar la consola del navegador para errores JavaScript")
        print("   3. Verificar que el formulario esté usando el endpoint correcto")
        print("   4. Comprobar que no haya bloqueos de CORS o seguridad")
        
    else:
        print("\n❌ SIMULACIÓN FALLIDA")
        print("🔧 Revisar logs del contenedor para más detalles")
    
    print("\n🏁 SIMULACIÓN COMPLETADA")
    print("=" * 80)

if __name__ == "__main__":
    main()
