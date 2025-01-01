#!/usr/bin/env python3
"""
Script de prueba de conexión a la base de datos
Solución para problemas de imports relativos
"""

import sys
import os
from pathlib import Path

# Agregar el directorio raíz del proyecto al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from sqlalchemy import create_engine, text
    from src.config import settings
    import logging
    
    # Configurar logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    def test_database_connection():
        """Probar conexión a la base de datos"""
        print("🔍 PROBANDO CONEXIÓN A BASE DE DATOS")
        print("=" * 50)
        
        try:
            # Crear engine con configuración específica
            engine = create_engine(
                settings.database_url,
                pool_pre_ping=True,
                pool_recycle=300,
                connect_args={
                    "options": "-c timezone=America/Bogota"
                }
            )
            
            # Probar conexión
            with engine.connect() as conn:
                # Verificar versión de PostgreSQL
                result = conn.execute(text('SELECT version()'))
                db_version = result.fetchone()[0]
                print(f"✅ Conectado a PostgreSQL: {db_version[:50]}...")
                
                # Verificar tablas
                result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
                tables = [row[0] for row in result.fetchall()]
                print(f"✅ Tablas encontradas: {len(tables)}")
                
                # Mostrar tablas principales
                main_tables = ['users', 'packages', 'package_announcements', 'notifications', 'messages']
                for table in main_tables:
                    if table in tables:
                        result = conn.execute(text(f'SELECT COUNT(*) FROM {table}'))
                        count = result.fetchone()[0]
                        print(f"  ✅ {table}: {count} registros")
                    else:
                        print(f"  ❌ {table}: tabla no encontrada")
                
                # Verificar zona horaria
                result = conn.execute(text('SHOW timezone'))
                timezone = result.fetchone()[0]
                print(f"✅ Zona horaria DB: {timezone}")
                
                # Verificar configuración de timezone
                result = conn.execute(text("SELECT current_setting('timezone')"))
                current_tz = result.fetchone()[0]
                print(f"✅ Timezone actual: {current_tz}")
                
                print("\n🎉 CONEXIÓN EXITOSA A LA BASE DE DATOS")
                
        except Exception as e:
            print(f"❌ Error de conexión: {e}")
            print(f"Tipo de error: {type(e).__name__}")
            return False
        
        return True
    
    if __name__ == "__main__":
        test_database_connection()
        
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("Asegúrate de ejecutar desde el directorio raíz del proyecto")
except Exception as e:
    print(f"❌ Error inesperado: {e}")
