#!/usr/bin/env python3
# ========================================
# PAQUETES EL CLUB v3.1 - Test de Login y Email
# ========================================
# Script para probar el sistema de autenticación y envío de correos

import sys
import os
import requests
import json
from datetime import datetime

# Configuración de la aplicación
APP_URL = "http://localhost:8001"
TEST_EMAIL = "test@example.com"  # Cambiar por un email real para pruebas

def test_login():
    """Probar el sistema de login"""
    print("🔐 Test de Sistema de Login")
    print("=" * 50)
    
    # Test 1: Verificar que la aplicación esté corriendo
    print(f"\n🌐 Verificando aplicación en {APP_URL}...")
    try:
        response = requests.get(f"{APP_URL}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Aplicación funcionando correctamente")
        else:
            print(f"⚠️ Aplicación respondió con código: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error conectando a la aplicación: {e}")
        return False
    
    # Test 2: Probar endpoint de login
    print(f"\n🔑 Probando endpoint de login...")
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    try:
        response = requests.post(
            f"{APP_URL}/api/auth/login",
            data=login_data,  # Usar data en lugar de json para form data
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=10
        )
        
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text[:200]}...")
        
        if response.status_code == 200:
            data = response.json()
            if "access_token" in data:
                print("✅ Login exitoso - Token obtenido")
                return data["access_token"]
            else:
                print("❌ Login falló - No se obtuvo token")
                return None
        else:
            print(f"❌ Login falló - Status code: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error en login: {e}")
        return None

def test_password_reset():
    """Probar el sistema de reset de contraseña"""
    print(f"\n📧 Test de Reset de Contraseña")
    print("=" * 50)
    
    # Test 1: Solicitar reset de contraseña
    print(f"\n📤 Solicitando reset de contraseña para {TEST_EMAIL}...")
    
    reset_data = {
        "email": TEST_EMAIL
    }
    
    try:
        response = requests.post(
            f"{APP_URL}/api/auth/forgot-password",
            json=reset_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Solicitud de reset enviada correctamente")
            return True
        else:
            print(f"❌ Error en solicitud de reset: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error en reset de contraseña: {e}")
        return False

def test_email_system():
    """Probar el sistema de email directamente"""
    print(f"\n📧 Test de Sistema de Email")
    print("=" * 50)
    
    # Test 1: Probar endpoint de test de email
    print(f"\n📤 Probando envío de email de prueba...")
    
    email_data = {
        "to_email": TEST_EMAIL,
        "subject": f"Test Email - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "message": "Este es un email de prueba desde el sistema de paquetería."
    }
    
    try:
        response = requests.post(
            f"{APP_URL}/api/admin/test-email",
            json=email_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Email de prueba enviado correctamente")
            return True
        else:
            print(f"❌ Error enviando email: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error en envío de email: {e}")
        return False

def test_protected_endpoints(token):
    """Probar endpoints protegidos"""
    if not token:
        print(f"\n🚫 No se puede probar endpoints protegidos sin token")
        return
    
    print(f"\n🔒 Test de Endpoints Protegidos")
    print("=" * 50)
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Test 1: Obtener perfil de usuario
    print(f"\n👤 Obteniendo perfil de usuario...")
    try:
        response = requests.get(
            f"{APP_URL}/api/auth/me",
            headers=headers,
            timeout=10
        )
        
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 200:
            user_data = response.json()
            print(f"   Usuario: {user_data.get('username', 'N/A')}")
            print(f"   Email: {user_data.get('email', 'N/A')}")
            print("✅ Perfil obtenido correctamente")
        else:
            print(f"❌ Error obteniendo perfil: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error obteniendo perfil: {e}")
    
    # Test 2: Listar paquetes
    print(f"\n📦 Listando paquetes...")
    try:
        response = requests.get(
            f"{APP_URL}/api/packages/",
            headers=headers,
            timeout=10
        )
        
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 200:
            packages = response.json()
            print(f"   Total de paquetes: {len(packages)}")
            print("✅ Paquetes listados correctamente")
        else:
            print(f"❌ Error listando paquetes: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error listando paquetes: {e}")

def test_public_endpoints():
    """Probar endpoints públicos"""
    print(f"\n🌐 Test de Endpoints Públicos")
    print("=" * 50)
    
    # Test 1: Página principal
    print(f"\n🏠 Probando página principal...")
    try:
        response = requests.get(f"{APP_URL}/", timeout=10)
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 200:
            print("✅ Página principal accesible")
        else:
            print(f"❌ Error en página principal: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error accediendo a página principal: {e}")
    
    # Test 2: Página de login
    print(f"\n🔐 Probando página de login...")
    try:
        response = requests.get(f"{APP_URL}/login", timeout=10)
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 200:
            print("✅ Página de login accesible")
        else:
            print(f"❌ Error en página de login: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error accediendo a página de login: {e}")

def main():
    """Función principal de pruebas"""
    print("🧪 Test Completo de Login y Email")
    print("=" * 60)
    
    # Test de endpoints públicos
    test_public_endpoints()
    
    # Test de login
    token = test_login()
    
    # Test de endpoints protegidos
    test_protected_endpoints(token)
    
    # Test de reset de contraseña
    test_password_reset()
    
    # Test de email
    test_email_system()
    
    print(f"\n🎉 Tests completados")
    print(f"\n📋 Resumen:")
    print(f"   - Login: {'✅ Exitoso' if token else '❌ Falló'}")
    print(f"   - Reset de contraseña: {'✅ Probado'}")
    print(f"   - Email: {'✅ Probado'}")
    print(f"   - Endpoints protegidos: {'✅ Probados' if token else '❌ No probados'}")
    print(f"   - Endpoints públicos: {'✅ Probados'}")

if __name__ == "__main__":
    main()
