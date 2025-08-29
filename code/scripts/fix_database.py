#!/usr/bin/env python3
"""
Script para arreglar la base de datos agregando las columnas faltantes
"""

import sqlite3
import os
import sys

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

def fix_database():
    """Arreglar la base de datos agregando las columnas faltantes"""
    
    # Ruta de la base de datos SQLite
    db_path = "paqueteria.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de datos no encontrada en {db_path}")
        return False
    
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔧 Arreglando base de datos...")
        
        # Verificar si las columnas ya existen
        cursor.execute("PRAGMA table_info(package_announcements)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Agregar created_by_id a package_announcements si no existe
        if 'created_by_id' not in columns:
            print("➕ Agregando columna created_by_id a package_announcements...")
            cursor.execute("ALTER TABLE package_announcements ADD COLUMN created_by_id TEXT")
        
        # Verificar columnas de packages
        cursor.execute("PRAGMA table_info(packages)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Agregar created_by_id a packages si no existe
        if 'created_by_id' not in columns:
            print("➕ Agregando columna created_by_id a packages...")
            cursor.execute("ALTER TABLE packages ADD COLUMN created_by_id TEXT")
        
        # Commit los cambios
        conn.commit()
        print("✅ Base de datos arreglada correctamente")
        
        # Mostrar estructura actualizada
        print("\n📋 Estructura actualizada:")
        cursor.execute("PRAGMA table_info(package_announcements)")
        print("package_announcements:")
        for column in cursor.fetchall():
            print(f"  - {column[1]} ({column[2]})")
        
        cursor.execute("PRAGMA table_info(packages)")
        print("\npackages:")
        for column in cursor.fetchall():
            print(f"  - {column[1]} ({column[2]})")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error arreglando la base de datos: {e}")
        return False

if __name__ == "__main__":
    success = fix_database()
    sys.exit(0 if success else 1)
