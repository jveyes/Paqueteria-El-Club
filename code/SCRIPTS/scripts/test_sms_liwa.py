#!/usr/bin/env python3
# ========================================
# PAQUETES EL CLUB v3.1 - Prueba SMS LIWA.co
# ========================================

import asyncio
import sys
import os

# Agregar el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from services.sms_service import LIWASMSService

async def test_sms():
    """Probar envío de SMS con LIWA.co"""
    print("🚀 Probando servicio SMS con LIWA.co...")
    
    # Crear servicio SMS
    sms_service = LIWASMSService()
    
    # Número de prueba (reemplaza con tu número)
    test_phone = "3001234567"  # Cambia por tu número real
    
    # Mensaje de prueba
    test_message = "¡Prueba de SMS exitosa! 🎉\n\n" \
                   "Este es un mensaje de prueba del sistema PAQUETES EL CLUB.\n\n" \
                   "SMS enviado via LIWA.co API"
    
    print(f"📱 Enviando SMS a: {test_phone}")
    print(f"📝 Mensaje: {test_message}")
    print("-" * 50)
    
    try:
        # Enviar SMS
        result = await sms_service.send_sms(test_phone, test_message)
        
        if result["success"]:
            print("✅ SMS enviado exitosamente!")
            print(f"🎉 Resultado: {result}")
        else:
            print("❌ Error enviando SMS")
            print(f"🚨 Error: {result['error']}")
            
    except Exception as e:
        print(f"💥 Excepción: {e}")
    
    print("-" * 50)
    print("🏁 Prueba completada")

if __name__ == "__main__":
    asyncio.run(test_sms())
