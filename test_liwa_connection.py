#!/usr/bin/env python3
# ========================================
# PRUEBA DE CONEXIÓN LIWA.CO
# Datos exactos proporcionados por el usuario
# ========================================

import asyncio
import httpx
from datetime import datetime

class LIWATestConnection:
    def __init__(self):
        # Datos EXACTOS proporcionados por el usuario
        self.account = "00486396309"
        self.password = "6fEuRnd*$$#NfFAS"
        self.api_key = "c52d8399ac63a24563ee8a967bafffc6cb8d8dfa"
        self.auth_url = "https://api.liwa.co/v2/auth/login"
        self.sms_url = "https://api.liwa.co/v2/sms/single"
        self._auth_token = None
    
    async def test_connection(self):
        """Prueba la conexión completa con LIWA.co"""
        print("�� PRUEBA DE CONEXIÓN LIWA.CO")
        print("=" * 50)
        
        # PASO 1: Verificar conectividad
        print("🔍 PASO 1: Verificando conectividad...")
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("https://api.liwa.co/")
                print(f"✅ Conectividad OK - Status: {response.status_code}")
        except Exception as e:
            print(f"❌ Error de conectividad: {e}")
            return False
        
        # PASO 2: Autenticación
        print("\n🔐 PASO 2: Autenticación...")
        print(f"URL: {self.auth_url}")
        print(f"Account: {self.account}")
        
        auth_data = {
            "account": self.account,
            "password": self.password
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.auth_url,
                    json=auth_data,
                    headers={"Content-Type": "application/json"}
                )
                
                print(f"Status: {response.status_code}")
                print(f"Respuesta: {response.text}")
                
                if response.status_code == 200:
                    result = response.json()
                    self._auth_token = result.get("token")
                    print(f"✅ Autenticación exitosa!")
                    print(f"Token: {self._auth_token[:50]}...")
                    return True
                else:
                    print(f"❌ Error en autenticación: {response.status_code}")
                    return False
                    
        except Exception as e:
            print(f"❌ Error en autenticación: {e}")
            return False
    
    async def test_sms_send(self):
        """Prueba el envío de SMS"""
        if not self._auth_token:
            print("❌ No hay token de autenticación")
            return False
        
        print("\n📱 PASO 3: Prueba de envío SMS...")
        print(f"URL: {self.sms_url}")
        
        sms_data = {
            "number": "573002596319",
            "message": "Prueba de conexión LIWA.co - PAQUETES EL CLUB",
            "type": 1
        }
        
        headers = {
            "Authorization": f"Bearer {self._auth_token}",
            "API-KEY": self.api_key,
            "Content-Type": "application/json"
        }
        
        print(f"Body: {sms_data}")
        print(f"Headers: {headers}")
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.sms_url,
                    json=sms_data,
                    headers=headers
                )
                
                print(f"Status: {response.status_code}")
                print(f"Respuesta: {response.text}")
                
                if response.status_code == 200:
                    print("✅ SMS enviado exitosamente!")
                    return True
                else:
                    print(f"❌ Error al enviar SMS: {response.status_code}")
                    return False
                    
        except Exception as e:
            print(f"❌ Error al enviar SMS: {e}")
            return False

async def main():
    """Función principal de prueba"""
    print("🔍 INICIANDO PRUEBA DE CONEXIÓN LIWA.CO")
    print("=" * 60)
    
    liwa_test = LIWATestConnection()
    
    # Prueba de conexión y autenticación
    if await liwa_test.test_connection():
        print("\n✅ ¡CONEXIÓN Y AUTENTICACIÓN EXITOSAS!")
        
        # Prueba de envío SMS
        if await liwa_test.test_sms_send():
            print("\n🎉 ¡SMS ENVIADO EXITOSAMENTE!")
            print("📱 Deberías recibir el mensaje en tu teléfono")
        else:
            print("\n❌ Falló el envío del SMS")
    else:
        print("\n❌ Falló la conexión o autenticación")

if __name__ == "__main__":
    asyncio.run(main())
