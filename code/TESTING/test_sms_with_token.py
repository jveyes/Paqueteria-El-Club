#!/usr/bin/env python3
"""
Script para probar el envío de SMS usando un token válido
"""

import asyncio
import httpx

async def test_sms_with_token():
    """Probar envío de SMS con token válido"""
    
    # Configuración
    account = "00486396309"
    password = "6fEuRnd*$$#NfFAS"
    api_key = "c52d8399ac63a24563ee8a967bafffc6cb8d8dfa"
    auth_url = "https://api.liwa.co/v2/auth/login"
    sms_url = "https://api.liwa.co/v2/sms/single"
    
    print("📱 Probando envío de SMS con token válido")
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
            
            # 2. Enviar SMS
            print("\n📤 Enviando SMS...")
            
            # Probar diferentes formatos de datos para SMS
            sms_formats = [
                {
                    "name": "Formato 1: number + message + type",
                    "data": {
                        "number": "573002596319",
                        "message": "Prueba SMS desde script - PAQUETES EL CLUB",
                        "type": 1
                    }
                },
                {
                    "name": "Formato 2: phone + message",
                    "data": {
                        "phone": "573002596319",
                        "message": "Prueba SMS desde script - PAQUETES EL CLUB"
                    }
                },
                {
                    "name": "Formato 3: to + message + from",
                    "data": {
                        "to": "573002596319",
                        "message": "Prueba SMS desde script - PAQUETES EL CLUB",
                        "from": "PAQUETES"
                    }
                }
            ]
            
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            for i, format_test in enumerate(sms_formats, 1):
                print(f"\n📋 {format_test['name']}")
                print("-" * 40)
                
                try:
                    response = await client.post(
                        sms_url,
                        json=format_test['data'],
                        headers=headers,
                        timeout=30.0
                    )
                    
                    print(f"Status: {response.status_code}")
                    print(f"Response: {response.text}")
                    
                    if response.status_code == 200:
                        result = response.json()
                        print("✅ SMS enviado exitosamente!")
                        print(f"Resultado: {result}")
                        break  # Si uno funciona, no probar los demás
                    else:
                        print(f"❌ Error: {response.status_code}")
                        
                except Exception as e:
                    print(f"❌ Error: {e}")
            
    except Exception as e:
        print(f"❌ Error general: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 Iniciando prueba de SMS con token...")
    asyncio.run(test_sms_with_token())
    print("\n✅ Prueba completada")

