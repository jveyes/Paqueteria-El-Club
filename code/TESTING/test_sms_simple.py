#!/usr/bin/env python3
"""
Script de prueba simple para verificar el servicio SMS
"""

import asyncio
import httpx

async def test_liwa_api():
    """Probar la API de LIWA directamente"""
    try:
        # Configuración de LIWA
        account = "00486396309"
        password = "6fEuRnd*$$#NfFAS"
        api_key = "c52d8399ac63a24563ee8a967bafffc6cb8d8dfa"
        auth_url = "https://api.liwa.co/v2/auth/login"
        sms_url = "https://api.liwa.co/v2/sms/single"
        
        print("✅ Configuración de LIWA cargada")
        print(f"   Account: {account}")
        print(f"   API Key: {api_key[:10]}...")
        
        # Autenticación
        print("\n🔐 Autenticando con LIWA...")
        auth_data = {
            "account": account,
            "password": password,
            "api_key": api_key
        }
        
        async with httpx.AsyncClient() as client:
            auth_response = await client.post(auth_url, json=auth_data)
            print(f"   Status: {auth_response.status_code}")
            
            if auth_response.status_code == 200:
                auth_result = auth_response.json()
                print(f"   ✅ Autenticación exitosa")
                print(f"   Token: {auth_result.get('token', 'N/A')[:20]}...")
                
                # Probar envío de SMS
                print("\n📱 Probando envío de SMS...")
                sms_data = {
                    "phone": "573002596319",
                    "message": "Prueba desde contenedor - PAQUETES EL CLUB",
                    "sender": "PAQUETES"
                }
                
                headers = {"Authorization": f"Bearer {auth_result['token']}"}
                sms_response = await client.post(sms_url, json=sms_data, headers=headers)
                print(f"   Status: {sms_response.status_code}")
                
                if sms_response.status_code == 200:
                    sms_result = sms_response.json()
                    print(f"   ✅ SMS enviado exitosamente")
                    print(f"   Resultado: {sms_result}")
                else:
                    print(f"   ❌ Error enviando SMS: {sms_response.text}")
            else:
                print(f"   ❌ Error de autenticación: {auth_response.text}")
                
    except Exception as e:
        print(f"❌ Error en prueba: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 Iniciando prueba directa de API LIWA...")
    asyncio.run(test_liwa_api())
    print("✅ Prueba completada")
