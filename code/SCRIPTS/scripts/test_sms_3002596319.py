#!/usr/bin/env python3
# ========================================
# PAQUETES EL CLUB v3.1 - Prueba SMS LIWA.co
# Número de Prueba: 3002596319
# ========================================

import asyncio
import sys
import os
from datetime import datetime

# Agregar el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from services.sms_service import LIWASMSService

async def test_sms_3002596319():
    """Probar envío de SMS con LIWA.co al número 3002596319"""
    print("�� PAQUETES EL CLUB v3.1 - Prueba SMS LIWA.co")
    print("=" * 60)
    print(f"�� Número de prueba: 3002596319")
    print(f"🕐 Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Crear servicio SMS
    sms_service = LIWASMSService()
    
    # Número de prueba específico
    test_phone = "3002596319"
    
    # Mensaje de prueba realista
    test_message = f"¡Prueba de SMS exitosa! 🎉\n\n" \
                   f"📦 Número de Guía: TEST123\n" \
                   f"�� Código de Consulta: TEST\n\n" \
                   f"Consulta el estado en: http://localhost/track\n\n" \
                   f"Recibirás confirmación por SMS cuando cambie el estado.\n\n" \
                   f"PAQUETES EL CLUB\n" \
                   f"🕐 {datetime.now().strftime('%H:%M:%S')}"
    
    print(f"📝 Mensaje a enviar:")
    print("-" * 40)
    print(test_message)
    print("-" * 40)
    
    try:
        print(f"\n📤 Enviando SMS a: {test_phone}")
        print("⏳ Esperando respuesta de LIWA.co...")
        
        # Enviar SMS
        result = await sms_service.send_sms(test_phone, test_message)
        
        print("\n�� RESULTADO DEL ENVÍO:")
        print("=" * 40)
        
        if result["success"]:
            print("✅ SMS enviado exitosamente!")
            print(f"🆔 Message ID: {result.get('message_id', 'N/A')}")
            print(f"📱 Teléfono: {result.get('phone', 'N/A')}")
            print(f"�� Timestamp: {result.get('timestamp', 'N/A')}")
            print(f"�� Proveedor: {result.get('provider', 'N/A')}")
            
            # Verificar estado del mensaje
            if result.get('message_id'):
                print(f"\n�� Verificando estado del mensaje...")
                status_result = await sms_service.get_sms_status(result['message_id'])
                if status_result["success"]:
                    print(f"📊 Estado: {status_result.get('status', 'N/A')}")
                else:
                    print(f"❌ Error verificando estado: {status_result.get('error', 'N/A')}")
            
        else:
            print("❌ Error enviando SMS")
            print(f"🚨 Error: {result['error']}")
            print(f"📱 Teléfono: {result.get('phone', 'N/A')}")
            print(f"�� Proveedor: {result.get('provider', 'N/A')}")
            
    except Exception as e:
        print(f"\n💥 EXCEPCIÓN DURANTE EL ENVÍO:")
        print(f"🚨 Error: {e}")
        print(f"📋 Tipo: {type(e).__name__}")
    
    print("\n" + "=" * 60)
    print("🏁 Prueba completada")
    print("📱 Verifica tu teléfono 3002596319 para el SMS")

async def test_multiple_sms():
    """Probar envío de múltiples SMS para verificar rate limiting"""
    print("\n🔄 PRUEBA DE MÚLTIPLES SMS")
    print("=" * 40)
    
    sms_service = LIWASMSService()
    test_phone = "3002596319"
    
    messages = [
        "Prueba 1: SMS de anuncio de paquete ��",
        "Prueba 2: SMS de paquete recibido ��",
        "Prueba 3: SMS de paquete en tránsito ��",
        "Prueba 4: SMS de paquete entregado ✅"
    ]
    
    for i, message in enumerate(messages, 1):
        print(f"\n�� Enviando SMS {i}/4...")
        result = await sms_service.send_sms(test_phone, message)
        
        if result["success"]:
            print(f"✅ SMS {i} enviado exitosamente")
        else:
            print(f"❌ SMS {i} falló: {result['error']}")
        
        # Esperar 2 segundos entre envíos
        if i < len(messages):
            print("⏳ Esperando 2 segundos...")
            await asyncio.sleep(2)
    
    print("\n🏁 Prueba de múltiples SMS completada")

if __name__ == "__main__":
    print("🧪 INICIANDO PRUEBAS SMS LIWA.co")
    print("=" * 60)
    
    # Ejecutar prueba principal
    asyncio.run(test_sms_3002596319())
    
    # Preguntar si ejecutar prueba de múltiples SMS
    print("\n" + "=" * 60)
    response = input("¿Quieres probar envío de múltiples SMS? (s/n): ").lower().strip()
    
    if response in ['s', 'si', 'sí', 'y', 'yes']:
        asyncio.run(test_multiple_sms())
    
    print("\n🎯 Todas las pruebas completadas!")
    print("📱 Verifica tu teléfono 3002596319")
