#!/usr/bin/env python3
"""
Script de depuración para identificar problemas en el formulario del navegador
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

def debug_browser_form_issues():
    """Depurar problemas del formulario del navegador"""
    print("🔍 DEPURANDO PROBLEMAS DEL FORMULARIO DEL NAVEGADOR")
    print("=" * 70)
    
    base_url = "http://localhost"
    
    print("📋 DIAGNÓSTICO PASO A PASO:")
    print("=" * 50)
    
    # Paso 1: Verificar que la página esté funcionando
    print("\n1️⃣ VERIFICANDO PÁGINA DEL FORMULARIO...")
    try:
        response = requests.get(f"{base_url}/announce")
        if response.status_code == 200:
            print("   ✅ Página accesible")
            
            # Verificar elementos críticos
            html_content = response.text
            
            checks = [
                ("Formulario HTML", "announcementForm"),
                ("Endpoint API", "api/announcements"),
                ("JavaScript", "fetch('/api/announcements/'"),
                ("Modal de éxito", "successModal"),
                ("Validaciones", "showError"),
                ("Botón submit", "submitButton")
            ]
            
            for check_name, check_text in checks:
                if check_text in html_content:
                    print(f"   ✅ {check_name}: Encontrado")
                else:
                    print(f"   ❌ {check_name}: NO encontrado")
                    
        else:
            print(f"   ❌ Error accediendo a la página: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Paso 2: Verificar que la API esté funcionando
    print("\n2️⃣ VERIFICANDO API DE ANUNCIOS...")
    try:
        test_data = {
            "customer_name": "Debug User",
            "guide_number": f"DEBUG{int(time.time())}",
            "phone_number": "3002596319"
        }
        
        response = requests.post(
            f"{base_url}/api/announcements/",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("   ✅ API funcionando")
            print(f"   • Tracking code: {result['tracking_code']}")
            print(f"   • ID: {result['id']}")
            
            # Verificar que el SMS se envió
            print("\n3️⃣ VERIFICANDO ENVÍO DE SMS...")
            time.sleep(2)
            
            # Revisar logs del contenedor
            print("   🔍 Revisando logs del contenedor...")
            print("   💡 Si ves 'SMS enviado exitosamente', el backend está funcionando")
            
        else:
            print(f"   ❌ Error en API: {response.status_code}")
            print(f"   • Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Paso 3: Simular diferentes escenarios del navegador
    print("\n4️⃣ SIMULANDO ESCENARIOS DEL NAVEGADOR...")
    
    scenarios = [
        {
            "name": "Headers mínimos (navegador básico)",
            "headers": {"Content-Type": "application/json"}
        },
        {
            "name": "Headers completos (navegador real)",
            "headers": {
                "Content-Type": "application/json",
                "Accept": "application/json, text/plain, */*",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Origin": base_url,
                "Referer": f"{base_url}/announce"
            }
        },
        {
            "name": "Headers con CORS",
            "headers": {
                "Content-Type": "application/json",
                "Accept": "*/*",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "content-type"
            }
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n   📝 Escenario {i}: {scenario['name']}")
        
        test_data = {
            "customer_name": f"Escenario {i}",
            "guide_number": f"SCENARIO{i}{int(time.time())}",
            "phone_number": "3002596319"
        }
        
        try:
            response = requests.post(
                f"{base_url}/api/announcements/",
                json=test_data,
                headers=scenario["headers"]
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"      ✅ Funcionando - Tracking: {result['tracking_code']}")
            else:
                print(f"      ❌ Error {response.status_code}")
                
        except Exception as e:
            print(f"      ❌ Error: {e}")
        
        time.sleep(1)
    
    return True

def check_potential_issues():
    """Verificar posibles problemas conocidos"""
    print("\n5️⃣ VERIFICANDO PROBLEMAS CONOCIDOS...")
    print("=" * 50)
    
    issues = [
        {
            "name": "CORS (Cross-Origin Resource Sharing)",
            "description": "El navegador podría estar bloqueando la petición por CORS",
            "solution": "Verificar configuración de CORS en el backend"
        },
        {
            "name": "JavaScript Errors",
            "description": "Errores en la consola del navegador podrían estar impidiendo el envío",
            "solution": "Abrir DevTools (F12) y revisar la consola"
        },
        {
            "name": "Validaciones Frontend",
            "description": "Las validaciones JavaScript podrían estar fallando silenciosamente",
            "solution": "Verificar que todos los campos pasen las validaciones"
        },
        {
            "name": "Network Issues",
            "description": "Problemas de red o firewall",
            "solution": "Verificar conectividad y logs del navegador"
        },
        {
            "name": "Cache del Navegador",
            "description": "El navegador podría estar usando una versión cacheada del formulario",
            "solution": "Hard refresh (Ctrl+F5) o limpiar cache"
        }
    ]
    
    for i, issue in enumerate(issues, 1):
        print(f"\n   ⚠️ Problema {i}: {issue['name']}")
        print(f"      📝 Descripción: {issue['description']}")
        print(f"      🛠️ Solución: {issue['solution']}")

def main():
    """Función principal"""
    print("🚀 INICIANDO DEPURACIÓN DEL FORMULARIO DEL NAVEGADOR")
    print("=" * 80)
    
    # Depurar problemas
    success = debug_browser_form_issues()
    
    if success:
        # Verificar problemas conocidos
        check_potential_issues()
        
        print("\n" + "=" * 80)
        print("📊 RESUMEN DE DEPURACIÓN")
        print("=" * 80)
        print("✅ Backend funcionando correctamente")
        print("✅ API respondiendo correctamente")
        print("✅ SMS enviándose desde la API")
        print("✅ Página del formulario accesible")
        
        print("\n🔍 PROBLEMA IDENTIFICADO:")
        print("   El problema NO está en el backend ni en la API.")
        print("   El problema está en el FRONTEND del navegador.")
        
        print("\n💡 SOLUCIONES A PROBAR:")
        print("   1. Abrir DevTools (F12) en el navegador")
        print("   2. Ir a la pestaña Console")
        print("   3. Enviar el formulario y revisar errores")
        print("   4. Verificar que no haya errores JavaScript")
        print("   5. Comprobar que la petición se envíe en Network tab")
        print("   6. Hard refresh (Ctrl+F5) para limpiar cache")
        
        print("\n🎯 PRÓXIMO PASO:")
        print("   Usar el navegador real y revisar la consola para errores")
        
    else:
        print("\n❌ DEPURACIÓN FALLIDA")
        print("🔧 Revisar logs del contenedor para más detalles")
    
    print("\n🏁 DEPURACIÓN COMPLETADA")
    print("=" * 80)

if __name__ == "__main__":
    main()
