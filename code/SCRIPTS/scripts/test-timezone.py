#!/usr/bin/env python3
# ========================================
# PAQUETES EL CLUB v3.1 - Test de Zona Horaria
# ========================================
# Script para verificar que la zona horaria de Colombia esté funcionando correctamente

import sys
import os
from datetime import datetime
import pytz

# Agregar el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_timezone():
    """Probar la configuración de zona horaria"""
    print("🕐 Test de Zona Horaria - Colombia")
    print("=" * 50)
    
    # Test 1: Hora del sistema
    print("\n📅 Hora del sistema:")
    print(f"   datetime.now(): {datetime.now()}")
    print(f"   datetime.now().tzinfo: {datetime.now().tzinfo}")
    
    # Test 2: Hora UTC
    utc_now = datetime.now(pytz.UTC)
    print(f"\n🌍 Hora UTC:")
    print(f"   UTC: {utc_now}")
    
    # Test 3: Hora Colombia
    colombia_tz = pytz.timezone('America/Bogota')
    colombia_now = datetime.now(colombia_tz)
    print(f"\n🇨🇴 Hora Colombia:")
    print(f"   Colombia: {colombia_now}")
    print(f"   Colombia (formateada): {colombia_now.strftime('%A, %d de %B de %Y, %H:%M')}")
    
    # Test 4: Diferencia horaria
    print(f"\n⏰ Diferencia horaria:")
    print(f"   UTC vs Colombia: {utc_now.astimezone(colombia_tz).strftime('%H:%M')}")
    
    # Test 5: Verificar función personalizada
    try:
        from utils.datetime_utils import get_colombia_now, format_colombia_datetime
        print(f"\n🔧 Función personalizada:")
        custom_now = get_colombia_now()
        print(f"   get_colombia_now(): {custom_now}")
        print(f"   format_colombia_datetime(): {format_colombia_datetime(custom_now, '%A, %d de %B de %Y, %H:%M')}")
        
        # Test 6: Generar tracking number
        from utils.helpers import generate_tracking_number
        tracking = generate_tracking_number()
        print(f"\n📦 Tracking number generado:")
        print(f"   {tracking}")
        
    except ImportError as e:
        print(f"\n❌ Error importando módulos: {e}")
    
    # Test 7: Verificar variables de entorno
    print(f"\n🌍 Variables de entorno:")
    tz_env = os.environ.get('TZ', 'No configurada')
    print(f"   TZ: {tz_env}")
    
    print(f"\n✅ Test completado")
    print(f"   Hora actual en Colombia: {colombia_now.strftime('%A, %d de %B de %Y, %H:%M')}")

if __name__ == "__main__":
    test_timezone()
