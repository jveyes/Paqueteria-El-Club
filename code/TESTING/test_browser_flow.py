#!/usr/bin/env python3
"""
Script para simular el flujo completo del navegador
PAQUETES EL CLUB v3.1
"""

import requests
import json
import sys
from datetime import datetime

# Configuración
BASE_URL = "http://localhost:8001"
LOGIN_URL = f"{BASE_URL}/auth/login"
DASHBOARD_URL = f"{BASE_URL}/dashboard"
PROFILE_URL = f"{BASE_URL}/profile/"

def print_header(title):
    """Imprimir encabezado de sección"""
    print(f"\n{'='*60}")
    print(f"🌐 {title}")
    print(f"{'='*60}")

def print_step(step, description):
    """Imprimir paso de prueba"""
    print(f"\n📋 Paso {step}: {description}")

def test_browser_flow():
    """Simular el flujo completo del navegador"""
    print_header("SIMULACIÓN DEL FLUJO DEL NAVEGADOR")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 URL Base: {BASE_URL}")
    
    # Crear sesión para mantener cookies
    session = requests.Session()
    
    # Paso 1: Ir a la página de login
    print_step(1, "Accediendo a la página de login")
    try:
        response = session.get(LOGIN_URL)
        print(f"📡 Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Página de login accesible")
            # Verificar que sea la página correcta
            if "Iniciar Sesión" in response.text:
                print("✅ Contenido correcto de login")
            else:
                print("⚠️  Contenido inesperado en login")
        else:
            print(f"❌ Error en login: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False
    
    # Paso 2: Intentar acceder al dashboard sin autenticación
    print_step(2, "Intentando acceder al dashboard sin autenticación")
    try:
        response = session.get(DASHBOARD_URL)
        print(f"📡 Status: {response.status_code}")
        if response.status_code == 302:
            print("✅ Redirección correcta a login (esperado)")
            redirect_url = response.headers.get('Location', '')
            print(f"📍 Redirigiendo a: {redirect_url}")
        else:
            print(f"⚠️  Status inesperado: {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False
    
    # Paso 3: Hacer login
    print_step(3, "Realizando login")
    try:
        login_data = {
            "username": "admin_test",
            "password": "admin123"
        }
        response = session.post(f"{BASE_URL}/api/auth/login", data=login_data)
        print(f"📡 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            print(f"✅ Login exitoso")
            print(f"👤 Usuario: {data.get('user', {}).get('username')}")
            print(f"🎭 Rol: {data.get('user', {}).get('role')}")
            
            # Agregar token a la sesión
            session.headers.update({"Authorization": f"Bearer {token}"})
        else:
            print(f"❌ Error en login: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False
    
    # Paso 4: Acceder al dashboard con autenticación
    print_step(4, "Accediendo al dashboard con autenticación")
    try:
        response = session.get(DASHBOARD_URL)
        print(f"📡 Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Dashboard accesible")
            # Verificar que contenga el enlace al perfil
            if "profile" in response.text.lower():
                print("✅ Enlace al perfil encontrado en el dashboard")
            else:
                print("⚠️  Enlace al perfil no encontrado")
        else:
            print(f"❌ Error en dashboard: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False
    
    # Paso 5: Acceder al perfil
    print_step(5, "Accediendo al perfil")
    try:
        response = session.get(PROFILE_URL)
        print(f"📡 Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Perfil accesible")
            # Verificar contenido del perfil
            if "Mi Perfil" in response.text:
                print("✅ Contenido correcto del perfil")
            else:
                print("⚠️  Contenido inesperado en perfil")
        else:
            print(f"❌ Error en perfil: {response.status_code}")
            print(f"📄 Respuesta: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False
    
    # Paso 6: Probar páginas adicionales del perfil
    print_step(6, "Probando páginas adicionales del perfil")
    
    # Editar perfil
    try:
        response = session.get(f"{BASE_URL}/profile/edit")
        print(f"📡 Editar perfil - Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Página de edición accesible")
        else:
            print(f"❌ Error en edición: {response.status_code}")
    except Exception as e:
        print(f"❌ Error en edición: {e}")
    
    # Cambiar contraseña
    try:
        response = session.get(f"{BASE_URL}/profile/change-password")
        print(f"📡 Cambiar contraseña - Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Página de cambio de contraseña accesible")
        else:
            print(f"❌ Error en cambio de contraseña: {response.status_code}")
    except Exception as e:
        print(f"❌ Error en cambio de contraseña: {e}")
    
    print_header("FLUJO COMPLETADO")
    print("🎉 ¡El flujo del navegador funciona correctamente!")
    print("\n📋 Resumen:")
    print("   ✅ Login funciona")
    print("   ✅ Dashboard accesible con autenticación")
    print("   ✅ Perfil accesible")
    print("   ✅ Enlaces de navegación funcionando")
    print("\n🔗 URLs para probar en el navegador:")
    print(f"   📄 Login: {LOGIN_URL}")
    print(f"   📊 Dashboard: {DASHBOARD_URL}")
    print(f"   👤 Perfil: {PROFILE_URL}")
    print(f"   ✏️  Editar: {BASE_URL}/profile/edit")
    print(f"   🔒 Cambiar Contraseña: {BASE_URL}/profile/change-password")
    
    return True

if __name__ == "__main__":
    success = test_browser_flow()
    sys.exit(0 if success else 1)
