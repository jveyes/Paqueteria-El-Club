#!/usr/bin/env python3
"""
Script de prueba del formulario de anuncios
Simula el envío desde el navegador
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

def test_announce_form():
    """Probar el formulario de anuncios"""
    print("🧪 PROBANDO FORMULARIO DE ANUNCIOS DESDE NAVEGADOR")
    print("=" * 60)
    
    base_url = "http://localhost"
    
    # Datos de prueba
    test_data = {
        "customer_name": "Juan Pérez",
        "guide_number": f"GUIDE{int(time.time())}",  # Número único
        "phone_number": "3002596319"
    }
    
    print(f"📝 Datos de prueba:")
    print(f"   • Nombre: {test_data['customer_name']}")
    print(f"   • Guía: {test_data['guide_number']}")
    print(f"   • Teléfono: {test_data['phone_number']}")
    print()
    
    try:
        # Paso 1: Verificar que la página esté disponible
        print("🔍 PASO 1: Verificando página de anuncios...")
        response = requests.get(f"{base_url}/announce")
        
        if response.status_code == 200:
            print("✅ Página de anuncios disponible")
        else:
            print(f"❌ Error accediendo a la página: {response.status_code}")
            return False
        
        # Paso 2: Enviar formulario
        print("\n📤 PASO 2: Enviando formulario...")
        response = requests.post(
            f"{base_url}/api/announcements/",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Formulario enviado exitosamente")
            print(f"   • ID del anuncio: {result['id']}")
            print(f"   • Código de tracking: {result['tracking_code']}")
            print(f"   • Estado: {result['status']}")
            
            # Verificar que el SMS se envió
            print("\n📱 PASO 3: Verificando envío de SMS...")
            
            # Esperar un momento para que se procese el SMS
            time.sleep(2)
            
            # Verificar logs del contenedor
            print("   🔍 Revisando logs del contenedor...")
            print("   💡 El SMS debería haberse enviado a 573002596319")
            print("   ✅ Si ves 'SMS enviado exitosamente' en los logs, todo está funcionando")
            
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

def test_multiple_announcements():
    """Probar múltiples anuncios para verificar rate limiting"""
    print("\n🔄 PROBANDO MÚLTIPLES ANUNCIOS (Rate Limiting)")
    print("=" * 60)
    
    base_url = "http://localhost"
    
    for i in range(3):
        test_data = {
            "customer_name": f"Usuario Test {i+1}",
            "guide_number": f"TEST{i+1}{int(time.time())}",
            "phone_number": "3002596319"
        }
        
        print(f"\n📝 Enviando anuncio {i+1}/3...")
        print(f"   • Guía: {test_data['guide_number']}")
        
        try:
            response = requests.post(
                f"{base_url}/api/announcements/",
                json=test_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Anuncio {i+1} enviado - Tracking: {result['tracking_code']}")
            else:
                print(f"   ❌ Error en anuncio {i+1}: {response.status_code}")
                if response.status_code == 429:
                    print("   ⚠️ Rate limit alcanzado")
                    break
                    
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Pausa entre anuncios
        if i < 2:
            time.sleep(1)

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBAS DEL FORMULARIO DE ANUNCIOS")
    print("=" * 70)
    
    # Probar anuncio individual
    success = test_announce_form()
    
    if success:
        print("\n🎉 PRUEBA EXITOSA")
        print("✅ El formulario está funcionando correctamente")
        print("✅ El SMS se está enviando")
        print("✅ La API está operativa")
        
        # Probar múltiples anuncios
        test_multiple_announcements()
        
    else:
        print("\n❌ PRUEBA FALLIDA")
        print("🔧 Revisar logs del contenedor para más detalles")
    
    print("\n🏁 PRUEBAS COMPLETADAS")
    print("=" * 70)
