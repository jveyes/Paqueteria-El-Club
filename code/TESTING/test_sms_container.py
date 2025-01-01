#!/usr/bin/env python3
"""
Script de prueba para verificar el servicio SMS dentro del contenedor
"""

import asyncio
import sys
import os

# Agregar el directorio src al path
sys.path.insert(0, '/app/src')

async def test_sms_service():
    """Probar el servicio SMS"""
    try:
        from services.sms_service import SMSService
        
        print("✅ Importando servicio SMS...")
        sms = SMSService()
        
        print(f"✅ Servicio SMS creado:")
        print(f"   Account: {sms.account}")
        print(f"   API Key: {sms.api_key[:10]}...")
        
        print("\n📱 Probando envío de SMS...")
        result = await sms.send_tracking_sms(
            phone='3002596319',
            customer_name='JUAN PÉREZ',
            tracking_code='TEST123',
            guide_number='TEST789012'
        )
        
        print(f"✅ SMS enviado exitosamente:")
        print(f"   Resultado: {result}")
        
    except Exception as e:
        print(f"❌ Error probando SMS: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 Iniciando prueba del servicio SMS...")
    asyncio.run(test_sms_service())
    print("✅ Prueba completada")

