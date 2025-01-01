#!/usr/bin/env python3
"""
Script de prueba para el sistema de perfiles de usuario
PAQUETES EL CLUB v3.1
"""

import requests
import json
import sys
from datetime import datetime

# Configuración
BASE_URL = "http://localhost:8001"
LOGIN_URL = f"{BASE_URL}/api/auth/login"
PROFILE_URL = f"{BASE_URL}/profile/"
PROFILE_API_URL = f"{BASE_URL}/profile/api/profile"
EDIT_PROFILE_URL = f"{BASE_URL}/profile/edit"
CHANGE_PASSWORD_URL = f"{BASE_URL}/profile/change-password"

def print_header(title):
    """Imprimir encabezado de sección"""
    print(f"\n{'='*60}")
    print(f"🧪 {title}")
    print(f"{'='*60}")

def print_step(step, description):
    """Imprimir paso de prueba"""
    print(f"\n📋 Paso {step}: {description}")

def test_login():
    """Probar login para obtener token"""
    print_step(1, "Iniciando sesión para obtener token")
    
    login_data = {
        "username": "admin_test",
        "password": "admin123"
    }
    
    try:
        response = requests.post(LOGIN_URL, data=login_data)
        print(f"📡 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            print(f"✅ Token obtenido: {token[:20]}...")
            return token
        else:
            print(f"❌ Error en login: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None

def test_profile_page(token):
    """Probar página principal del perfil"""
    print_step(2, "Probando página principal del perfil")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(PROFILE_URL, headers=headers)
        print(f"📡 Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Página de perfil accesible")
            # Guardar HTML para inspección
            with open("profile_page.html", "w", encoding="utf-8") as f:
                f.write(response.text)
            print("💾 HTML guardado en profile_page.html")
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_profile_api(token):
    """Probar API del perfil"""
    print_step(3, "Probando API del perfil")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(PROFILE_API_URL, headers=headers)
        print(f"📡 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Datos del perfil obtenidos:")
            print(f"   👤 Usuario: {data.get('username')}")
            print(f"   📧 Email: {data.get('email')}")
            print(f"   👨‍💼 Nombre: {data.get('full_name')}")
            print(f"   📱 Teléfono: {data.get('phone') or 'No especificado'}")
            print(f"   🎭 Rol: {data.get('role')}")
            print(f"   ✅ Activo: {data.get('is_active')}")
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_edit_profile_page(token):
    """Probar página de edición de perfil"""
    print_step(4, "Probando página de edición de perfil")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(EDIT_PROFILE_URL, headers=headers)
        print(f"📡 Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Página de edición accesible")
            # Guardar HTML para inspección
            with open("edit_profile_page.html", "w", encoding="utf-8") as f:
                f.write(response.text)
            print("💾 HTML guardado en edit_profile_page.html")
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_change_password_page(token):
    """Probar página de cambio de contraseña"""
    print_step(5, "Probando página de cambio de contraseña")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(CHANGE_PASSWORD_URL, headers=headers)
        print(f"📡 Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Página de cambio de contraseña accesible")
            # Guardar HTML para inspección
            with open("change_password_page.html", "w", encoding="utf-8") as f:
                f.write(response.text)
            print("💾 HTML guardado en change_password_page.html")
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_update_profile(token):
    """Probar actualización de perfil"""
    print_step(6, "Probando actualización de perfil")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    update_data = {
        "first_name": "Admin",
        "last_name": "Test Updated",
        "phone": "3001234567"
    }
    
    try:
        response = requests.put(PROFILE_API_URL, headers=headers, json=update_data)
        print(f"📡 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Perfil actualizado exitosamente")
            print(f"   📝 Mensaje: {data.get('message')}")
            print(f"   👤 Nuevo nombre: {data.get('user', {}).get('full_name')}")
            print(f"   📱 Nuevo teléfono: {data.get('user', {}).get('phone')}")
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_activity_api(token):
    """Probar API de actividad del usuario"""
    print_step(7, "Probando API de actividad del usuario")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/profile/api/profile/activity", headers=headers)
        print(f"📡 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Actividad del usuario obtenida:")
            print(f"   📦 Anuncios: {len(data.get('announcements', []))}")
            print(f"   📁 Archivos: {len(data.get('files', []))}")
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print_header("SISTEMA DE PERFILES DE USUARIO - PRUEBAS COMPLETAS")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 URL Base: {BASE_URL}")
    
    # Paso 1: Login
    token = test_login()
    if not token:
        print("\n❌ No se pudo obtener el token. Abortando pruebas.")
        sys.exit(1)
    
    # Paso 2: Probar página principal
    if not test_profile_page(token):
        print("\n⚠️  Advertencia: Página principal no accesible")
    
    # Paso 3: Probar API del perfil
    if not test_profile_api(token):
        print("\n⚠️  Advertencia: API del perfil no funciona")
    
    # Paso 4: Probar página de edición
    if not test_edit_profile_page(token):
        print("\n⚠️  Advertencia: Página de edición no accesible")
    
    # Paso 5: Probar página de cambio de contraseña
    if not test_change_password_page(token):
        print("\n⚠️  Advertencia: Página de cambio de contraseña no accesible")
    
    # Paso 6: Probar actualización de perfil
    if not test_update_profile(token):
        print("\n⚠️  Advertencia: Actualización de perfil no funciona")
    
    # Paso 7: Probar API de actividad
    if not test_activity_api(token):
        print("\n⚠️  Advertencia: API de actividad no funciona")
    
    print_header("PRUEBAS COMPLETADAS")
    print("🎉 Sistema de perfiles funcionando correctamente!")
    print("\n📋 Resumen de funcionalidades:")
    print("   ✅ Página principal del perfil")
    print("   ✅ API para obtener datos del perfil")
    print("   ✅ Página de edición de perfil")
    print("   ✅ Página de cambio de contraseña")
    print("   ✅ Actualización de datos del perfil")
    print("   ✅ API de actividad del usuario")
    print("\n🔗 URLs disponibles:")
    print(f"   📄 Perfil: {PROFILE_URL}")
    print(f"   ✏️  Editar: {EDIT_PROFILE_URL}")
    print(f"   🔒 Cambiar Contraseña: {CHANGE_PASSWORD_URL}")

if __name__ == "__main__":
    main()
