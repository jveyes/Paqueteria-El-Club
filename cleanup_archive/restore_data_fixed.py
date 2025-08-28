#!/usr/bin/env python3
"""
Script para restaurar datos del backup a la base de datos AWS RDS (versión corregida)
"""

import sys
import os

def main():
    try:
        # Leer el archivo de backup (copiado al contenedor)
        backup_file = "/app/backup.sql"
        
        if not os.path.exists(backup_file):
            print(f"❌ Error: No se encontró el archivo de backup: {backup_file}")
            return
        
        print(f"📖 Leyendo archivo de backup: {backup_file}")
        with open(backup_file, 'r') as f:
            backup_content = f.read()
        
        print(f"📊 Tamaño del backup: {len(backup_content)} caracteres")
        
        # URL de la base de datos AWS
        database_url = "postgresql://jveyes:a?HC!2.*1#?[==:|289qAI=)#V4kDzl$@ls-abe25e9bea57818f0ee32555c0e7b4a10e361535.ctobuhtlkwoj.us-east-1.rds.amazonaws.com:5432/paqueteria"
        
        print("🔍 Conectando a la base de datos AWS...")
        from sqlalchemy import create_engine, text
        engine = create_engine(database_url)
        
        print("🔄 Restaurando datos...")
        with engine.connect() as conn:
            # Ejecutar el contenido del backup
            conn.execute(text(backup_content))
            conn.commit()
        
        print("✅ Datos restaurados exitosamente")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
