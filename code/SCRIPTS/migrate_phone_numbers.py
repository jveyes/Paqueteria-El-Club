#!/usr/bin/env python3
"""
Script para migrar números de teléfono existentes al nuevo formato
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database.database import SessionLocal
from src.models.customer import Customer
from src.utils.validators import validate_international_phone_number

def migrate_existing_phone_numbers():
    """Migra números de teléfono existentes al nuevo formato"""
    db = SessionLocal()
    
    try:
        # Obtener todos los clientes
        customers = db.query(Customer).all()
        
        print(f"Migrando {len(customers)} números de teléfono...")
        
        for customer in customers:
            if customer.phone:
                # Validar y formatear el número
                result = validate_international_phone_number(customer.phone)
                
                if result['is_valid']:
                    # Actualizar campos
                    customer.phone_formatted = result['formatted_number']
                    customer.country_code = result['country_code']
                    customer.phone_country = result['country']
                    
                    print(f"✅ {customer.name}: {customer.phone} → {result['formatted_number']} ({result['country']})")
                else:
                    print(f"❌ {customer.name}: {customer.phone} - {result['error_message']}")
        
        # Guardar cambios
        db.commit()
        print("✅ Migración completada exitosamente")
        
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    migrate_existing_phone_numbers()
