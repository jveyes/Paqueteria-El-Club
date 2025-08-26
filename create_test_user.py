#!/usr/bin/env python3
"""
Script para crear un usuario de prueba con contraseña conocida
"""

import requests
import json
from datetime import datetime

def create_test_user():
    """Crear usuario de prueba"""
    url = "http://localhost/api/auth/register"
    headers = {"Content-Type": "application/json"}
    
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "test123",
        "first_name": "Test",
        "last_name": "User",
        "role": "USER"
    }
    
    try:
        response = requests.post(url, headers=headers, json=user_data)
        print(f"🔍 Creando usuario: {user_data['username']}")
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ ÉXITO - Usuario creado")
            print(f"👤 Username: {result.get('username', 'N/A')}")
            print(f"📧 Email: {result.get('email', 'N/A')}")
            print(f"🎭 Rol: {result.get('role', 'N/A')}")
        else:
            print(f"❌ ERROR - {response.text}")
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"❌ ERROR DE CONEXIÓN: {e}")
        return False

def test_login_with_new_user():
    """Probar login con el nuevo usuario"""
    print("\n" + "=" * 50)
    print("🧪 PROBANDO LOGIN CON NUEVO USUARIO")
    print("=" * 50)
    
    # Probar con username
    print("\n🔍 Probando login con username 'testuser':")
    url = "http://localhost/api/auth/login"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "password",
        "username": "testuser",
        "password": "test123"
    }
    
    try:
        response = requests.post(url, headers=headers, data=data)
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ ÉXITO - Login por username funciona")
            print(f"👤 Usuario: {result.get('user', {}).get('username', 'N/A')}")
        else:
            print(f"❌ ERROR - {response.text}")
        
    except Exception as e:
        print(f"❌ ERROR DE CONEXIÓN: {e}")
    
    # Probar con email
    print("\n🔍 Probando login con email 'test@example.com':")
    data = {
        "grant_type": "password",
        "username": "test@example.com",
        "password": "test123"
    }
    
    try:
        response = requests.post(url, headers=headers, data=data)
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ ÉXITO - Login por email funciona")
            print(f"📧 Email: {result.get('user', {}).get('email', 'N/A')}")
        else:
            print(f"❌ ERROR - {response.text}")
        
    except Exception as e:
        print(f"❌ ERROR DE CONEXIÓN: {e}")

def main():
    """Función principal"""
    print("=" * 60)
    print("🧪 CREACIÓN Y PRUEBA DE USUARIO DE TEST")
    print("=" * 60)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Crear usuario de prueba
    if create_test_user():
        # Probar login
        test_login_with_new_user()
    else:
        print("❌ No se pudo crear el usuario de prueba")

if __name__ == "__main__":
    main()
