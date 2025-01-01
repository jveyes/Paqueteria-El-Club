#!/usr/bin/env python3
# ========================================
# PAQUETES EL CLUB v3.1 - Consulta Rápida de Tracking
# ========================================

import sys
import os
from sqlalchemy import create_engine, text

# Agregar el directorio src al path para importar módulos
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from config import settings

def consulta_rapida(tracking_code):
    """Consulta rápida del teléfono asociado a un código de tracking"""
    try:
        # Conexión directa a la base de datos
        engine = create_engine(settings.database_url)
        
        with engine.connect() as conn:
            # Consulta optimizada para obtener solo el teléfono
            query = text("""
                SELECT customer_phone, customer_name, tracking_number
                FROM packages 
                WHERE tracking_number = :tracking_code
                UNION
                SELECT phone as customer_phone, name as customer_name, tracking_number
                FROM customers 
                WHERE tracking_number = :tracking_code
                LIMIT 1
            """)
            
            result = conn.execute(query, {"tracking_code": tracking_code})
            row = result.fetchone()
            
            if row:
                return {
                    "phone": row.customer_phone,
                    "name": row.customer_name,
                    "tracking": row.tracking_number
                }
            return None
            
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python consulta_rapida_tracking.py <CODIGO>")
        sys.exit(1)
    
    codigo = sys.argv[1].strip()
    resultado = consulta_rapida(codigo)
    
    if resultado:
        print(f"📱 {resultado['phone']}")
    else:
        print("❌ No encontrado")
