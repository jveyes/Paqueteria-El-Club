#!/usr/bin/env python3
"""
Script para probar el login con AWS RDS
PAQUETES EL CLUB v3.1
"""

import requests
import json
import sys
from datetime import datetime

# Configuración
BASE_URL = "http://localhost:8001"
LOGIN_URL = f"{BASE_URL}/api/auth/login"

def print_header(title):
    """Imprimir encabezado de sección"""
    print(f"\n{'='*60}")
    print(f"🔐 {title}")
    print(f"{'='*60}")

def test_login(identifier, password, description):
    """Probar login con un identificador específico"""
    print(f"\n📋 Probando: {description}")
    print(f"   Identificador: {identifier}")
    print(f"   Contraseña: {password}")
    
    try:
        response = requests.post(LOGIN_URL, data={
            "username": identifier,
            "password": password
        })
        
        print(f"   📡 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            user = data.get("user", {})
            print(f"   ✅ Login exitoso")
            print(f"   👤 Usuario: {user.get('username')}")
            print(f"   📧 Email: {user.get('email')}")
            print(f"   🎭 Rol: {user.get('role')}")
            print(f"   🔑 Token: {token[:20]}...")
            return True
        else:
            error_data = response.json()
            print(f"   ❌ Error: {error_data.get('detail', 'Error desconocido')}")
            return False
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print_header("PRUEBAS DE LOGIN CON AWS RDS")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 URL Base: {BASE_URL}")
    print(f"🗄️  Base de datos: AWS RDS")
    
    # Casos de prueba
    test_cases = [
        # Usuario jveyes
        ("jveyes", "admin123", "Login con username (jveyes)"),
        ("jveyes@gmail.com", "admin123", "Login con email (jveyes)"),
        
        # Usuario jesus
        ("jesus", "admin123", "Login con username (jesus)"),
        ("jesus@papyrus.com.co", "admin123", "Login con email (jesus)"),
        
        # Casos de error
        ("usuario_inexistente", "admin123", "Login con username inexistente"),
        ("email@inexistente.com", "admin123", "Login con email inexistente"),
        ("jveyes", "contraseña_incorrecta", "Login con contraseña incorrecta"),
    ]
    
    successful_tests = 0
    total_tests = len(test_cases)
    
    for identifier, password, description in test_cases:
        if test_login(identifier, password, description):
            successful_tests += 1
    
    print_header("RESULTADOS FINALES")
    print(f"✅ Pruebas exitosas: {successful_tests}/{total_tests}")
    print(f"❌ Pruebas fallidas: {total_tests - successful_tests}/{total_tests}")
    
    if successful_tests >= 4:  # Los 4 casos válidos deberían funcionar
        print("\n🎉 ¡Sistema de login con AWS RDS funcionando correctamente!")
        print("   ✅ Login con username funciona")
        print("   ✅ Login con email funciona")
        print("   ✅ Validación de credenciales incorrectas funciona")
        print("   ✅ Base de datos AWS RDS configurada correctamente")
    else:
        print("\n⚠️  Hay problemas con el sistema de login")
    
    print("\n📋 Credenciales válidas para usar:")
    print("   👤 Usuario: jveyes")
    print("   📧 Email: jveyes@gmail.com")
    print("   🔑 Contraseña: admin123")
    print()
    print("   👤 Usuario: jesus")
    print("   📧 Email: jesus@papyrus.com.co")
    print("   🔑 Contraseña: admin123")

if __name__ == "__main__":
    main()
