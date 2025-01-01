#!/usr/bin/env python3
# ========================================
# PAQUETES EL CLUB v3.1 - Consulta de Teléfono por Tracking
# ========================================

import sys
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Agregar el directorio src al path para importar módulos
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from config import settings

def consultar_telefono_por_tracking(tracking_code):
    """
    Consulta en la base de datos a qué número de teléfono se envió un código de tracking
    
    Args:
        tracking_code (str): El código de tracking a consultar
    
    Returns:
        dict: Información del cliente y paquete, o None si no se encuentra
    """
    try:
        # Crear conexión a la base de datos
        engine = create_engine(settings.database_url)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Consulta SQL para obtener información del cliente y paquete
        query = text("""
            SELECT 
                c.name as customer_name,
                c.phone as customer_phone,
                c.tracking_number,
                p.status as package_status,
                p.created_at,
                p.announced_at
            FROM customers c
            LEFT JOIN packages p ON c.tracking_number = p.tracking_number
            WHERE c.tracking_number = :tracking_code
        """)
        
        result = db.execute(query, {"tracking_code": tracking_code})
        row = result.fetchone()
        
        if row:
            return {
                "customer_name": row.customer_name,
                "customer_phone": row.customer_phone,
                "tracking_number": row.tracking_number,
                "package_status": row.package_status,
                "created_at": row.created_at,
                "announced_at": row.announced_at
            }
        else:
            # Si no se encuentra en customers, buscar en packages
            query_package = text("""
                SELECT 
                    customer_name,
                    customer_phone,
                    tracking_number,
                    status as package_status,
                    created_at,
                    announced_at
                FROM packages
                WHERE tracking_number = :tracking_code
            """)
            
            result_package = db.execute(query_package, {"tracking_code": tracking_code})
            row_package = result_package.fetchone()
            
            if row_package:
                return {
                    "customer_name": row_package.customer_name,
                    "customer_phone": row_package.customer_phone,
                    "tracking_number": row_package.tracking_number,
                    "package_status": row_package.package_status,
                    "created_at": row_package.created_at,
                    "announced_at": row_package.announced_at
                }
            else:
                return None
                
    except Exception as e:
        print(f"Error al consultar la base de datos: {e}")
        return None
    finally:
        if 'db' in locals():
            db.close()

def main():
    """Función principal del script"""
    print("=" * 60)
    print("PAQUETES EL CLUB v3.1 - Consulta de Teléfono por Tracking")
    print("=" * 60)
    
    if len(sys.argv) != 2:
        print("Uso: python consultar_telefono_tracking.py <CODIGO_TRACKING>")
        print("Ejemplo: python consultar_telefono_tracking.py PAP2025010112345678")
        sys.exit(1)
    
    tracking_code = sys.argv[1].strip()
    
    print(f"Consultando código de tracking: {tracking_code}")
    print("-" * 60)
    
    # Realizar la consulta
    resultado = consultar_telefono_por_tracking(tracking_code)
    
    if resultado:
        print("✅ INFORMACIÓN ENCONTRADA:")
        print(f"📦 Código de Tracking: {resultado['tracking_number']}")
        print(f"👤 Nombre del Cliente: {resultado['customer_name']}")
        print(f"📱 Teléfono: {resultado['customer_phone']}")
        print(f"📊 Estado del Paquete: {resultado['package_status']}")
        
        if resultado['created_at']:
            print(f"📅 Fecha de Creación: {resultado['created_at']}")
        if resultado['announced_at']:
            print(f"📢 Fecha de Anuncio: {resultado['announced_at']}")
            
        print("-" * 60)
        print(f"📞 El código {tracking_code} fue enviado al teléfono: {resultado['customer_phone']}")
        
    else:
        print("❌ NO SE ENCONTRÓ INFORMACIÓN")
        print(f"El código de tracking '{tracking_code}' no existe en la base de datos.")
        print("\nVerifica que:")
        print("- El código esté escrito correctamente")
        print("- El código exista en el sistema")
        print("- No haya espacios o caracteres extra")

if __name__ == "__main__":
    main()
