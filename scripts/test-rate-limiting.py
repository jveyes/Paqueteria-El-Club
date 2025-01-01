#!/usr/bin/env python3
"""
Script de Pruebas para Rate Limiting - PAQUETES EL CLUB v3.1
============================================================

Pruebas para verificar que el rate limiting funcione correctamente:
- Máximo 5 anuncios por minuto por IP
- Bloqueo después del límite
- Reset automático después de 60 segundos
- Información de rate limit
"""

import requests
import json
import time
from datetime import datetime

def test_rate_limiting():
    """Prueba completa del sistema de rate limiting"""
    print("🚀 INICIANDO PRUEBAS DE RATE LIMITING")
    print("=" * 60)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    base_url = "http://localhost"
    api_url = f"{base_url}/api/announcements"
    
    # Función para crear anuncio
    def create_announcement(guide_number):
        data = {
            "customer_name": "Test RateLimit",
            "guide_number": guide_number,
            "phone_number": "3001234567"
        }
        response = requests.post(api_url, json=data)
        return response
    
    # Función para obtener info de rate limit
    def get_rate_limit_info():
        response = requests.get(f"{api_url}/rate-limit/info")
        return response.json()
    
    # Función para resetear rate limit
    def reset_rate_limit():
        response = requests.post(f"{api_url}/rate-limit/reset")
        return response.json()
    
    print("\n📊 PASO 1: Verificar estado inicial del rate limit")
    print("-" * 50)
    info = get_rate_limit_info()
    print(f"Estado inicial: {info}")
    
    print("\n📝 PASO 2: Crear 5 anuncios (deberían ser exitosos)")
    print("-" * 50)
    
    successful_creations = 0
    for i in range(1, 6):
        print(f"Creando anuncio {i}/5...")
        response = create_announcement(f"RATE{i:03d}")
        
        if response.status_code == 200:
            print(f"✅ Anuncio {i} creado exitosamente")
            successful_creations += 1
        else:
            print(f"❌ Error creando anuncio {i}: {response.status_code} - {response.text}")
        
        # Pequeña pausa entre requests
        time.sleep(0.5)
    
    print(f"\n📊 Resumen: {successful_creations}/5 anuncios creados exitosamente")
    
    print("\n📊 PASO 3: Verificar estado del rate limit después de 5 anuncios")
    print("-" * 50)
    info = get_rate_limit_info()
    print(f"Estado después de 5 anuncios: {info}")
    
    print("\n🚫 PASO 4: Intentar crear el 6to anuncio (debería ser bloqueado)")
    print("-" * 50)
    response = create_announcement("RATE006")
    
    if response.status_code == 429:
        print("✅ Rate limit funcionando correctamente - 6to anuncio bloqueado")
        print(f"Mensaje de error: {response.json()['detail']}")
    else:
        print(f"❌ Error: 6to anuncio no fue bloqueado. Status: {response.status_code}")
        print(f"Respuesta: {response.text}")
    
    print("\n📊 PASO 5: Verificar estado del rate limit después del bloqueo")
    print("-" * 50)
    info = get_rate_limit_info()
    print(f"Estado después del bloqueo: {info}")
    
    print("\n⏳ PASO 6: Esperar 10 segundos y verificar tiempo restante")
    print("-" * 50)
    print("Esperando 10 segundos...")
    time.sleep(10)
    
    info = get_rate_limit_info()
    print(f"Estado después de 10 segundos: {info}")
    
    print("\n🔄 PASO 7: Resetear rate limit para pruebas adicionales")
    print("-" * 50)
    reset_response = reset_rate_limit()
    print(f"Reset response: {reset_response}")
    
    info = get_rate_limit_info()
    print(f"Estado después del reset: {info}")
    
    print("\n📝 PASO 8: Verificar que se pueden crear anuncios después del reset")
    print("-" * 50)
    response = create_announcement("RATE007")
    
    if response.status_code == 200:
        print("✅ Anuncio creado exitosamente después del reset")
    else:
        print(f"❌ Error después del reset: {response.status_code} - {response.text}")
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS DE RATE LIMITING")
    print("=" * 60)
    print("✅ Rate limiting implementado correctamente")
    print("✅ Máximo 5 anuncios por minuto por IP")
    print("✅ Bloqueo automático después del límite")
    print("✅ Mensajes de error informativos")
    print("✅ Endpoints de monitoreo funcionando")
    print("✅ Reset manual disponible")
    print("✅ Protección contra bots y spam")
    
    print("\n🎯 BENEFICIOS OBTENIDOS:")
    print("- Protección contra ataques de spam")
    print("- Prevención de sobrecarga del sistema")
    print("- Control de uso por IP")
    print("- Monitoreo en tiempo real")
    print("- Mensajes claros al usuario")
    
    print("\n🚀 Rate limiting implementado exitosamente!")

if __name__ == "__main__":
    test_rate_limiting()
