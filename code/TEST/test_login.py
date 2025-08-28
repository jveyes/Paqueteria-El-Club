#!/usr/bin/env python3
# ========================================
# PAQUETES EL CLUB v3.1 - Script de Prueba de Login
# ========================================

import requests
import json

def test_login():
    """Probar el login del usuario jveyes"""
    
    url = "http://localhost:8001/api/auth/login"
    data = {
        "username": "jveyes",
        "password": "Seaboard12"
    }
    
    try:
        print("🔐 Probando login para usuario jveyes...")
        print(f"   URL: {url}")
        print(f"   Usuario: {data['username']}")
        print(f"   Contraseña: {data['password']}")
        print()
        
        response = requests.post(url, data=data)
        
        print(f"📊 Respuesta del servidor:")
        print(f"   Status Code: {response.status_code}")
        print(f"   Headers: {dict(response.headers)}")
        print()
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Login exitoso!")
            print(f"   Token: {result.get('access_token', 'No disponible')[:50]}...")
            print(f"   Tipo: {result.get('token_type', 'No disponible')}")
            print(f"   Usuario: {result.get('user', {}).get('username', 'No disponible')}")
            return True
        else:
            print("❌ Login falló")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error al conectar: {e}")
        return False

def test_api_health():
    """Probar si la API está funcionando"""
    
    url = "http://localhost:8001/api/health"
    
    try:
        print("🏥 Probando salud de la API...")
        response = requests.get(url)
        
        if response.status_code == 200:
            print("✅ API está funcionando correctamente")
            return True
        else:
            print(f"❌ API no responde correctamente: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ No se puede conectar a la API: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("PAQUETES EL CLUB v3.1 - PRUEBA DE LOGIN")
    print("=" * 60)
    print()
    
    # Probar salud de la API
    if test_api_health():
        print()
        # Probar login
        test_login()
    else:
        print("❌ No se puede probar el login porque la API no está funcionando")
    
    print()
    print("=" * 60)
