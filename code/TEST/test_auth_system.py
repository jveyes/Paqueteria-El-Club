#!/usr/bin/env python3
# ========================================
# PAQUETES EL CLUB v3.1 - Test del Sistema de Autenticación
# ========================================

import requests
import json
import sys

# Configuración
BASE_URL = "http://localhost:8000"
TEST_EMAIL = "admin@papyrus.com.co"
TEST_PASSWORD = "Admin2025!"

def test_health_check():
    """Probar health check"""
    print("🔍 Probando health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check OK")
            return True
        else:
            print(f"❌ Health check falló: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error en health check: {e}")
        return False

def test_auth_check():
    """Probar verificación de autenticación"""
    print("🔍 Probando verificación de autenticación...")
    try:
        response = requests.get(f"{BASE_URL}/api/auth/check")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Auth check OK - Autenticado: {data.get('is_authenticated', False)}")
            return True
        else:
            print(f"❌ Auth check falló: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error en auth check: {e}")
        return False

def test_login():
    """Probar login"""
    print("🔍 Probando login...")
    try:
        # Usar form data como espera el endpoint
        data = {
            'grant_type': 'password',
            'username': TEST_EMAIL,
            'password': TEST_PASSWORD
        }
        
        response = requests.post(f"{BASE_URL}/api/auth/login", data=data)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Login exitoso")
            print(f"   Token: {data.get('access_token', 'N/A')[:20]}...")
            print(f"   Usuario: {data.get('user', {}).get('first_name', 'N/A')}")
            return data.get('access_token')
        else:
            print(f"❌ Login falló: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error en login: {e}")
        return None

def test_forgot_password():
    """Probar recuperación de contraseña"""
    print("🔍 Probando recuperación de contraseña...")
    try:
        data = {
            'email': TEST_EMAIL
        }
        
        response = requests.post(f"{BASE_URL}/api/auth/forgot-password", json=data)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Recuperación de contraseña exitosa")
            print(f"   Mensaje: {data.get('message', 'N/A')}")
            return True
        else:
            print(f"❌ Recuperación de contraseña falló: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error en recuperación de contraseña: {e}")
        return False

def test_register():
    """Probar registro de usuario"""
    print("🔍 Probando registro de usuario...")
    try:
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'TestPassword123!',
            'first_name': 'Test',
            'last_name': 'User',
            'phone': '1234567890',
            'role': 'USER'
        }
        
        response = requests.post(f"{BASE_URL}/api/auth/register", json=data)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Registro exitoso")
            print(f"   Usuario: {data.get('username', 'N/A')}")
            return True
        else:
            print(f"❌ Registro falló: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error en registro: {e}")
        return False

def main():
    """Ejecutar todas las pruebas"""
    print("🚀 Iniciando pruebas del sistema de autenticación...")
    print("=" * 50)
    
    # Probar health check
    if not test_health_check():
        print("❌ El servidor no está respondiendo. Asegúrate de que esté ejecutándose.")
        sys.exit(1)
    
    print()
    
    # Probar auth check
    test_auth_check()
    
    print()
    
    # Probar login
    token = test_login()
    
    print()
    
    # Probar recuperación de contraseña
    test_forgot_password()
    
    print()
    
    # Probar registro
    test_register()
    
    print()
    print("=" * 50)
    print("✅ Pruebas completadas")
    
    if token:
        print("🎉 El sistema de autenticación está funcionando correctamente")
        print("📝 Puedes usar las siguientes credenciales para probar:")
        print(f"   Email: {TEST_EMAIL}")
        print(f"   Contraseña: {TEST_PASSWORD}")
    else:
        print("⚠️  Algunas pruebas fallaron. Revisa los logs del servidor.")

if __name__ == "__main__":
    main()
