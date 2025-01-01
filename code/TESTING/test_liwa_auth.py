#!/usr/bin/env python3
"""
Script para probar diferentes métodos de autenticación con LIWA
"""

import asyncio
import httpx

async def test_liwa_auth_methods():
    """Probar diferentes métodos de autenticación"""
    
    # Configuración
    account = "00486396309"
    password = "6fEuRnd*$$#NfFAS"
    api_key = "c52d8399ac63a24563ee8a967bafffc6cb8d8dfa"
    auth_url = "https://api.liwa.co/v2/auth/login"
    
    print("🔐 Probando diferentes métodos de autenticación con LIWA")
    print("=" * 60)
    
    # Método 1: Solo account y password
    print("\n📋 MÉTODO 1: Solo account y password")
    print("-" * 40)
    try:
        auth_data = {
            "account": account,
            "password": password
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(auth_url, json=auth_data)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code == 200:
                result = response.json()
                token = result.get('token')
                print(f"✅ Token obtenido: {token[:20] if token else 'N/A'}...")
            else:
                print("❌ Autenticación falló")
                
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Método 2: Con API key en el body
    print("\n📋 MÉTODO 2: Con API key en el body")
    print("-" * 40)
    try:
        auth_data = {
            "account": account,
            "password": password,
            "api_key": api_key
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(auth_url, json=auth_data)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code == 200:
                result = response.json()
                token = result.get('token')
                print(f"✅ Token obtenido: {token[:20] if token else 'N/A'}...")
            else:
                print("❌ Autenticación falló")
                
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Método 3: Con API key en headers
    print("\n📋 MÉTODO 3: Con API key en headers")
    print("-" * 40)
    try:
        auth_data = {
            "account": account,
            "password": password
        }
        
        headers = {
            "API-KEY": api_key,
            "Content-Type": "application/json"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(auth_url, json=auth_data, headers=headers)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code == 200:
                result = response.json()
                token = result.get('token')
                print(f"✅ Token obtenido: {token[:20] if token else 'N/A'}...")
            else:
                print("❌ Autenticación falló")
                
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Iniciando pruebas de autenticación LIWA...")
    asyncio.run(test_liwa_auth_methods())
    print("\n✅ Pruebas completadas")

