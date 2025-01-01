#!/usr/bin/env python3
"""
Script para probar el envío de SMS incluyendo la API key en el header
"""

import asyncio
import httpx

async def test_sms_with_api_key():
    """Probar envío de SMS con API key en header"""
    
    # Configuración
    account = "00486396309"
    password = "6fEuRnd*$$#NfFAS"
    api_key = "c52d8399ac63a24563ee8a967bafffc6cb8d8dfa"
    auth_url = "https://api.liwa.co/v2/auth/login"
    sms_url = "https://api.liwa.co/v2/sms/single"
    
    print("📱 Probando envío de SMS con API key en header")
    print("=" * 60)
    
    try:
        # 1. Autenticarse
        print("🔐 Autenticando...")
        auth_data = {
            "account": account,
            "password": password
        }
        
        async with httpx.AsyncClient() as client:
            auth_response = await client.post(auth_url, json=auth_data)
            
            if auth_response.status_code != 200:
                print(f"❌ Error de autenticación: {auth_response.status_code}")
                return
            
            auth_result = auth_response.json()
            token = auth_result.get('token')
            print(f"✅ Token obtenido: {token[:20]}...")
            
            # 2. Enviar SMS con API key en header
            print("\n📤 Enviando SMS con API key...")
            
            # Probar con API key en header
            sms_data = {
                "number": "573002596319",
                "message": "Prueba SMS con API key - PAQUETES EL CLUB",
                "type": 1
            }
            
            headers = {
                "Authorization": f"Bearer {token}",
                "API-KEY": api_key,
                "Content-Type": "application/json"
            }
            
            print(f"📋 Datos del SMS:")
            print(f"   Número: {sms_data['number']}")
            print(f"   Mensaje: {sms_data['message']}")
            print(f"   Headers: {headers}")
            
            response = await client.post(
                sms_url,
                json=sms_data,
                headers=headers,
                timeout=30.0
            )
            
            print(f"\n📡 Respuesta del servidor:")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text}")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ SMS enviado exitosamente!")
                print(f"Resultado: {result}")
            else:
                print(f"❌ Error enviando SMS: {response.status_code}")
                
    except Exception as e:
        print(f"❌ Error general: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 Iniciando prueba de SMS con API key...")
    asyncio.run(test_sms_with_api_key())
    print("\n✅ Prueba completada")
