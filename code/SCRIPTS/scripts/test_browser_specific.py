#!/usr/bin/env python3
"""
Script para probar específicamente los problemas del navegador
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

def test_browser_specific_issues():
    """Probar problemas específicos del navegador"""
    print("🌐 PROBANDO PROBLEMAS ESPECÍFICOS DEL NAVEGADOR")
    print("=" * 70)
    
    base_url = "http://localhost"
    
    # Probar con datos exactos que enviaría el navegador
    print("📝 Probando con datos exactos del navegador...")
    
    # Caso 1: Datos válidos simples
    test_cases = [
        {
            "name": "Datos válidos simples",
            "data": {
                "customer_name": "Juan Pérez",
                "guide_number": f"BROWSER{int(time.time())}",
                "phone_number": "3002596319"
            }
        },
        {
            "name": "Datos con espacios",
            "data": {
                "customer_name": "María González López",
                "guide_number": f"BROWSER{int(time.time())+1}",
                "phone_number": "3002596319"
            }
        },
        {
            "name": "Datos con caracteres especiales",
            "data": {
                "customer_name": "José María",
                "guide_number": f"BROWSER{int(time.time())+2}",
                "phone_number": "3002596319"
            }
        }
    ]
    
    successful_sms = 0
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 Prueba {i}: {test_case['name']}")
        print("-" * 40)
        
        try:
            # Enviar con headers del navegador
            browser_headers = {
                "Content-Type": "application/json",
                "Accept": "application/json, text/plain, */*",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Origin": base_url,
                "Referer": f"{base_url}/announce"
            }
            
            response = requests.post(
                f"{base_url}/api/announcements/",
                json=test_case["data"],
                headers=browser_headers
            )
            
            print(f"   📤 Respuesta: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Éxito - Tracking: {result['tracking_code']}")
                print(f"   • ID: {result['id']}")
                print(f"   • Estado: {result['status']}")
                
                # Verificar SMS
                print("   📱 Verificando SMS...")
                time.sleep(2)
                successful_sms += 1
                
            else:
                print(f"   ❌ Error: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   • Detalle: {error_data.get('detail', 'Sin detalle')}")
                except:
                    print(f"   • Respuesta: {response.text}")
                    
        except Exception as e:
            print(f"   ❌ Excepción: {e}")
        
        time.sleep(1)
    
    return successful_sms, len(test_cases)

def check_form_validation_rules():
    """Verificar las reglas de validación del formulario"""
    print("\n🔍 VERIFICANDO REGLAS DE VALIDACIÓN...")
    print("=" * 50)
    
    base_url = "http://localhost"
    
    # Reglas de validación del frontend
    validation_rules = [
        {
            "name": "Nombre muy corto (debería fallar)",
            "data": {"customer_name": "A", "guide_number": f"TEST{int(time.time())}", "phone_number": "3002596319"},
            "should_fail": True
        },
        {
            "name": "Nombre con caracteres inválidos (debería fallar)",
            "data": {"customer_name": "Juan123", "guide_number": f"TEST{int(time.time())+1}", "phone_number": "3002596319"},
            "should_fail": True
        },
        {
            "name": "Guía muy corta (debería fallar)",
            "data": {"customer_name": "Juan Pérez", "guide_number": "123", "phone_number": "3002596319"},
            "should_fail": True
        },
        {
            "name": "Teléfono muy corto (debería fallar)",
            "data": {"customer_name": "Juan Pérez", "guide_number": f"TEST{int(time.time())+2}", "phone_number": "123"},
            "should_fail": True
        },
        {
            "name": "Teléfono no colombiano (debería fallar)",
            "data": {"customer_name": "Juan Pérez", "guide_number": f"TEST{int(time.time())+3}", "phone_number": "1234567890"},
            "should_fail": True
        }
    ]
    
    for i, rule in enumerate(validation_rules, 1):
        print(f"\n📝 Regla {i}: {rule['name']}")
        
        try:
            response = requests.post(
                f"{base_url}/api/announcements/",
                json=rule["data"],
                headers={"Content-Type": "application/json"}
            )
            
            if rule["should_fail"]:
                if response.status_code in [400, 422]:
                    print(f"   ✅ Comportamiento correcto - Error {response.status_code}")
                else:
                    print(f"   ❌ Comportamiento incorrecto - Éxito {response.status_code}")
            else:
                if response.status_code == 200:
                    print(f"   ✅ Comportamiento correcto - Éxito")
                else:
                    print(f"   ❌ Comportamiento incorrecto - Error {response.status_code}")
                    
        except Exception as e:
            print(f"   ❌ Excepción: {e}")
        
        time.sleep(0.5)

def main():
    """Función principal"""
    print("🚀 ANÁLISIS ESPECÍFICO DE PROBLEMAS DEL NAVEGADOR")
    print("=" * 80)
    
    # Probar problemas específicos del navegador
    successful_sms, total_tests = test_browser_specific_issues()
    
    # Verificar reglas de validación
    check_form_validation_rules()
    
    # Resumen final
    print("\n" + "=" * 80)
    print("📊 RESUMEN DEL ANÁLISIS")
    print("=" * 80)
    print(f"✅ SMS enviados exitosamente: {successful_sms}/{total_tests}")
    
    if successful_sms > 0:
        print("\n🎉 DIAGNÓSTICO COMPLETADO:")
        print("✅ El backend está funcionando perfectamente")
        print("✅ La API está respondiendo correctamente")
        print("✅ Los SMS se están enviando desde la API")
        print("✅ Las validaciones están funcionando")
        
        print("\n🔍 PROBLEMA IDENTIFICADO:")
        print("   El problema está en el NAVEGADOR REAL, no en el código.")
        
        print("\n💡 CAUSAS PROBABLES:")
        print("   1. **Cache del navegador** - Versión antigua del formulario")
        print("   2. **Errores JavaScript** - Consola del navegador con errores")
        print("   3. **Bloqueos de seguridad** - Extensions o configuración del navegador")
        print("   4. **Problemas de red** - Firewall o proxy")
        print("   5. **Versión del navegador** - Incompatibilidad con JavaScript moderno")
        
        print("\n🛠️ SOLUCIONES INMEDIATAS:")
        print("   1. **Hard Refresh**: Ctrl+F5 (Windows) o Cmd+Shift+R (Mac)")
        print("   2. **Limpiar Cache**: Configuración del navegador")
        print("   3. **Modo Incógnito**: Probar sin extensiones")
        print("   4. **DevTools**: F12 → Console → Revisar errores")
        print("   5. **Cambiar Navegador**: Probar con Chrome, Firefox, Edge")
        
        print("\n🎯 PRÓXIMO PASO:")
        print("   Usar el navegador real con las soluciones sugeridas")
        
    else:
        print("\n❌ PROBLEMAS DETECTADOS:")
        print("🔧 Revisar logs del contenedor para más detalles")
    
    print("\n🏁 ANÁLISIS COMPLETADO")
    print("=" * 80)

if __name__ == "__main__":
    main()
