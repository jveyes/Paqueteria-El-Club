#!/usr/bin/env python3
"""
Script para probar el login tanto por username como por email
"""

import requests
import json
from datetime import datetime

def test_login(username_or_email, password):
    """Probar login con username o email"""
    url = "http://localhost/api/auth/login"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "password",
        "username": username_or_email,
        "password": password
    }
    
    try:
        response = requests.post(url, headers=headers, data=data)
        print(f"🔍 Probando: {username_or_email}")
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ ÉXITO - Token recibido: {result.get('access_token', '')[:20]}...")
            print(f"👤 Usuario: {result.get('user', {}).get('username', 'N/A')}")
            print(f"📧 Email: {result.get('user', {}).get('email', 'N/A')}")
            print(f"🎭 Rol: {result.get('user', {}).get('role', 'N/A')}")
        else:
            print(f"❌ ERROR - {response.text}")
        
        print("-" * 50)
        return response.status_code == 200
        
    except Exception as e:
        print(f"❌ ERROR DE CONEXIÓN: {e}")
        print("-" * 50)
        return False

def main():
    """Función principal"""
    print("=" * 60)
    print("🧪 PRUEBA DE LOGIN POR USERNAME Y EMAIL")
    print("=" * 60)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Credenciales de prueba
    test_cases = [
        ("jveyes", "admin123"),           # Username
        ("jveyes@gmail.com", "admin123"), # Email
        ("admin", "admin123"),            # Username admin
        ("admin@papyrus.com.co", "admin123"), # Email admin
    ]
    
    success_count = 0
    total_count = len(test_cases)
    
    for username_or_email, password in test_cases:
        if test_login(username_or_email, password):
            success_count += 1
    
    print("=" * 60)
    print(f"📊 RESUMEN: {success_count}/{total_count} pruebas exitosas")
    
    if success_count == total_count:
        print("🎉 ¡TODAS LAS PRUEBAS EXITOSAS!")
        print("✅ El sistema acepta login tanto por username como por email")
    else:
        print("⚠️  Algunas pruebas fallaron")
        print("🔧 Revisar configuración del sistema")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
