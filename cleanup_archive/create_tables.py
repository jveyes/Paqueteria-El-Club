#!/usr/bin/env python3
"""
Script para crear las tablas en la base de datos AWS RDS
"""

import sys
import os
sys.path.append('/app')

from sqlalchemy import create_engine
from src.database.database import Base

def main():
    try:
        # URL de la base de datos AWS
        database_url = "postgresql://jveyes:a?HC!2.*1#?[==:|289qAI=)#V4kDzl$@ls-abe25e9bea57818f0ee32555c0e7b4a10e361535.ctobuhtlkwoj.us-east-1.rds.amazonaws.com:5432/paqueteria"
        
        print("🔍 Conectando a la base de datos AWS...")
        engine = create_engine(database_url)
        
        print("🔧 Creando tablas...")
        Base.metadata.create_all(engine)
        print("✅ Tablas creadas exitosamente")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
