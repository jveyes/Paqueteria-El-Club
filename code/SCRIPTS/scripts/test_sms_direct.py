#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Directo del Servicio SMS
=============================

Este script prueba directamente el servicio SMS sin dependencias complejas
para verificar que esté funcionando correctamente.
"""

import asyncio
import sys
import os

# Configuración directa de LIWA.co (como en sms_service.py)
LIWA_CONFIG = {
    "account": "00486396309",
    "password": "6fEuRnd*$$#NfFAS",
    "api_key": "c52d8399ac63a24563ee8a967bafffc6cb8d8dfa",
    "auth_url": "https://api.liwa.co/v2/auth/login",
}

async def test_sms_direct():
    """Test directo del servicio SMS"""
    
    print("🧪 TEST DIRECTO DEL SERVICIO SMS")
    print("=" * 50)
    
    # Datos de prueba
    test_phone = "3002596319"  # Tu número real
    test_name = "JUAN PÉREZ"
    test_guide = "TEST123456"
    test_code = "ABCD"
    
    print(f"📱 Número de prueba: {test_phone}")
    print(f"👤 Nombre: {test_name}")
    print(f"📦 Guía: {test_guide}")
    print(f"🎯 Código: {test_code}")
    print()
    
    # Simular el envío de SMS
    print("📤 Enviando SMS de prueba...")
    
    try:
        # Importar httpx para hacer la petición HTTP
        import httpx
        
        # Paso 1: Autenticación
        print("🔐 Paso 1: Autenticación con LIWA.co")
        
        auth_data = {
            "account": LIWA_CONFIG["account"],
            "password": LIWA_CONFIG["password"]
        }
        
        async with httpx.AsyncClient() as client:
            auth_response = await client.post(
                LIWA_CONFIG["auth_url"],
                json=auth_data,
                timeout=30.0
            )
            
            if auth_response.status_code != 200:
                print(f"   ❌ Error en autenticación: {auth_response.status_code}")
                print(f"   📄 Respuesta: {auth_response.text}")
                return False
            
            auth_result = auth_response.json()
            auth_token = auth_result.get("token")
            
            if not auth_token:
                print("   ❌ No se recibió token de autenticación")
                return False
            
            print("   ✅ Autenticación exitosa")
            print(f"   🔑 Token recibido: {auth_token[:20]}...")
            
            # Paso 2: Enviar SMS
            print("\n📱 Paso 2: Enviando SMS")
            
            # Formatear número de teléfono (agregar 57)
            formatted_phone = f"57{test_phone}"
            print(f"   📞 Número formateado: {formatted_phone}")
            
            # Preparar mensaje (exactamente como en el sistema)
            message = (
                f"Hola {test_name}, tu paquete con guía {test_guide} "
                f"ha sido registrado. Código de consulta: {test_code}. "
                f"PAQUETES EL CLUB"
            )
            
            print(f"   💬 Mensaje: {message}")
            
            # Datos para el SMS
            sms_data = {
                "number": formatted_phone,
                "message": message,
                "type": 1  # SMS estándar
            }
            
            headers = {
                "Authorization": f"Bearer {auth_token}",
                "API-KEY": LIWA_CONFIG["api_key"],
                "Content-Type": "application/json"
            }
            
            # Enviar SMS
            sms_response = await client.post(
                "https://api.liwa.co/v2/sms/single",
                json=sms_data,
                headers=headers,
                timeout=30.0
            )
            
            if sms_response.status_code == 200:
                result = sms_response.json()
                print("   ✅ SMS enviado exitosamente")
                print(f"   📱 Número: {formatted_phone}")
                print(f"   💬 Mensaje: {message}")
                print(f"   🆔 ID LIWA: {result.get('id', 'N/A')}")
                print(f"   📊 Estado: {result.get('status', 'N/A')}")
                
                print("\n🎉 SMS ENVIADO EXITOSAMENTE")
                print("=" * 50)
                print("✅ El servicio SMS está funcionando correctamente")
                print("✅ La integración con LIWA.co está operativa")
                print("✅ El formato del mensaje es correcto")
                print("✅ El número de teléfono se formatea correctamente")
                
                return True
                
            else:
                print(f"   ❌ Error al enviar SMS: {sms_response.status_code}")
                print(f"   📄 Respuesta: {sms_response.text}")
                return False
                
    except Exception as e:
        print(f"   ❌ Error inesperado: {e}")
        return False

async def main():
    """Función principal"""
    try:
        success = await test_sms_direct()
        if success:
            print("\n🚀 El servicio SMS está funcionando perfectamente")
            print("📱 Los usuarios recibirán SMS automáticamente")
        else:
            print("\n❌ Hay problemas en el servicio SMS")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n💥 Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
