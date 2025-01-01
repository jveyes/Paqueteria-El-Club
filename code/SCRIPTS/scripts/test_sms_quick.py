#!/usr/bin/env python3
# ========================================
# PAQUETES EL CLUB v3.1 - Prueba SMS Rápida
# ========================================

import asyncio
import sys
import os

# Agregar el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from services.sms_service import LIWASMSService

async def quick_test():
    """Prueba rápida de SMS"""
    print("🚀 Prueba rápida SMS")
    print(" Número: 3002596319")
    
    sms_service = LIWASMSService()
    phone = "3002596319"  # Formato local
    message = "¡Prueba rápida SMS exitosa!  PAQUETES EL CLUB"
    
    try:
        print(f"📤 Enviando SMS a {phone}...")
        print(f" El sistema formateará: {phone} → +57{phone}")
        
        result = await sms_service.send_sms(phone, message)
        
        if result["success"]:
            print("✅ SMS enviado exitosamente!")
            print(f"🆔 Message ID: {result.get('message_id', 'N/A')}")
            print(f"📱 Teléfono formateado: {result.get('phone', 'N/A')}")
        else:
            print(f"❌ Error: {result['error']}")
    except Exception as e:
        print(f" Excepción: {e}")

if __name__ == "__main__":
    asyncio.run(quick_test())
