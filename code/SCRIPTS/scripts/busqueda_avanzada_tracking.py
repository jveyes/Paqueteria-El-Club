#!/usr/bin/env python3
# ========================================
# PAQUETES EL CLUB v3.1 - Búsqueda Avanzada de Tracking
# ========================================

import sys
import os
from sqlalchemy import create_engine, text
from datetime import datetime

# Agregar el directorio src al path para importar módulos
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from config import settings

def buscar_por_tracking(tracking_code):
    """Buscar por código de tracking específico"""
    try:
        engine = create_engine(settings.database_url)
        
        with engine.connect() as conn:
            query = text("""
                SELECT 
                    p.tracking_number,
                    p.customer_name,
                    p.customer_phone,
                    p.status,
                    p.created_at,
                    p.announced_at,
                    c.name as customer_name_alt,
                    c.phone as customer_phone_alt
                FROM packages p
                FULL OUTER JOIN customers c ON p.tracking_number = c.tracking_number
                WHERE p.tracking_number = :tracking_code 
                   OR c.tracking_number = :tracking_code
            """)
            
            result = conn.execute(query, {"tracking_code": tracking_code})
            return result.fetchall()
            
    except Exception as e:
        print(f"Error en búsqueda por tracking: {e}")
        return []

def buscar_por_telefono(phone):
    """Buscar por número de teléfono"""
    try:
        engine = create_engine(settings.database_url)
        
        with engine.connect() as conn:
            query = text("""
                SELECT 
                    p.tracking_number,
                    p.customer_name,
                    p.customer_phone,
                    p.status,
                    p.created_at,
                    p.announced_at
                FROM packages p
                WHERE p.customer_phone = :phone
                UNION
                SELECT 
                    c.tracking_number,
                    c.name as customer_name,
                    c.phone as customer_phone,
                    'N/A' as status,
                    c.created_at,
                    c.created_at as announced_at
                FROM customers c
                WHERE c.phone = :phone
                ORDER BY created_at DESC
            """)
            
            result = conn.execute(query, {"phone": phone})
            return result.fetchall()
            
    except Exception as e:
        print(f"Error en búsqueda por teléfono: {e}")
        return []

def buscar_por_nombre(nombre):
    """Buscar por nombre del cliente"""
    try:
        engine = create_engine(settings.database_url)
        
        with engine.connect() as conn:
            query = text("""
                SELECT 
                    p.tracking_number,
                    p.customer_name,
                    p.customer_phone,
                    p.status,
                    p.created_at,
                    p.announced_at
                FROM packages p
                WHERE LOWER(p.customer_name) LIKE LOWER(:nombre)
                UNION
                SELECT 
                    c.tracking_number,
                    c.name as customer_name,
                    c.phone as customer_phone,
                    'N/A' as status,
                    c.created_at,
                    c.created_at as announced_at
                FROM customers c
                WHERE LOWER(c.name) LIKE LOWER(:nombre)
                ORDER BY created_at DESC
            """)
            
            result = conn.execute(query, {"nombre": f"%{nombre}%"})
            return result.fetchall()
            
    except Exception as e:
        print(f"Error en búsqueda por nombre: {e}")
        return []

def mostrar_resultados(resultados, tipo_busqueda):
    """Mostrar resultados de búsqueda"""
    if not resultados:
        print(f"❌ No se encontraron resultados para la búsqueda: {tipo_busqueda}")
        return
    
    print(f"\n✅ Se encontraron {len(resultados)} resultado(s):")
    print("=" * 80)
    
    for i, row in enumerate(resultados, 1):
        print(f"\n📦 Resultado #{i}:")
        print(f"   🔍 Código de Tracking: {row.tracking_number}")
        print(f"   👤 Nombre del Cliente: {row.customer_name or row.customer_name_alt}")
        print(f"   📱 Teléfono: {row.customer_phone or row.customer_phone_alt}")
        print(f"   📊 Estado: {row.status}")
        
        if row.created_at:
            print(f"   📅 Fecha de Creación: {row.created_at}")
        if row.announced_at:
            print(f"   📢 Fecha de Anuncio: {row.announced_at}")
        
        print("-" * 50)

def main():
    """Función principal del script"""
    print("=" * 80)
    print("PAQUETES EL CLUB v3.1 - Búsqueda Avanzada de Tracking")
    print("=" * 80)
    
    if len(sys.argv) < 3:
        print("Uso:")
        print("  python busqueda_avanzada_tracking.py tracking <CODIGO_TRACKING>")
        print("  python busqueda_avanzada_tracking.py telefono <NUMERO_TELEFONO>")
        print("  python busqueda_avanzada_tracking.py nombre <NOMBRE_CLIENTE>")
        print("\nEjemplos:")
        print("  python busqueda_avanzada_tracking.py tracking PAP2025010112345678")
        print("  python busqueda_avanzada_tracking.py telefono 3001234567")
        print("  python busqueda_avanzada_tracking.py nombre Juan Pérez")
        sys.exit(1)
    
    tipo_busqueda = sys.argv[1].lower()
    valor_busqueda = " ".join(sys.argv[2:]).strip()
    
    print(f"🔍 Tipo de búsqueda: {tipo_busqueda}")
    print(f"📝 Valor a buscar: {valor_busqueda}")
    print("-" * 80)
    
    if tipo_busqueda == "tracking":
        resultados = buscar_por_tracking(valor_busqueda)
        mostrar_resultados(resultados, f"código de tracking '{valor_busqueda}'")
        
    elif tipo_busqueda == "telefono":
        # Limpiar teléfono (solo números)
        telefono_limpio = ''.join(filter(str.isdigit, valor_busqueda))
        if not telefono_limpio:
            print("❌ El teléfono debe contener solo números")
            sys.exit(1)
        
        resultados = buscar_por_telefono(telefono_limpio)
        mostrar_resultados(resultados, f"teléfono '{telefono_limpio}'")
        
    elif tipo_busqueda == "nombre":
        if len(valor_busqueda) < 2:
            print("❌ El nombre debe tener al menos 2 caracteres")
            sys.exit(1)
        
        resultados = buscar_por_nombre(valor_busqueda)
        mostrar_resultados(resultados, f"nombre '{valor_busqueda}'")
        
    else:
        print(f"❌ Tipo de búsqueda no válido: {tipo_busqueda}")
        print("Tipos válidos: tracking, telefono, nombre")
        sys.exit(1)

if __name__ == "__main__":
    main()
