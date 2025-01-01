#!/usr/bin/env python3
"""
Script para probar el servicio SMS real del contenedor
"""

import asyncio
import sys
import os

# Agregar el directorio src al path
sys.path.insert(0, '/app/src')

async def test_real_sms():
    """Probar el servicio SMS real"""
    try:
        print("✅ Importando servicios...")
        
        # Importar el servicio SMS real
        from services.sms_service import SMSService
        
        print("✅ Creando servicio SMS...")
        sms_service = SMSService()
        
        print(f"✅ Servicio creado:")
        print(f"   Account: {sms_service.account}")
        print(f"   API Key: {sms_service.api_key[:10]}...")
        
        print("\n📱 Probando envío de SMS real...")
        
        # Probar envío de SMS
        result = await sms_service.send_tracking_sms(
            phone='3002596319',
            customer_name='JUAN PÉREZ',
            tracking_code='TEST123',
            guide_number='TEST789012'
        )
        
        print(f"✅ Resultado del SMS:")
        print(f"   {result}")
        
        if result.get('success'):
            print("🎉 SMS enviado exitosamente!")
        else:
            print(f"❌ Error enviando SMS: {result.get('error')}")
        
    except Exception as e:
        print(f"❌ Error en prueba: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 Iniciando prueba del servicio SMS real...")
    asyncio.run(test_real_sms())
    print("✅ Prueba completada")

