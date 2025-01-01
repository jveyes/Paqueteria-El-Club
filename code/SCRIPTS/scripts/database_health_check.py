#!/usr/bin/env python3
"""
Script de verificación de salud de la base de datos
Solución completa para problemas de conexión
"""

import sys
import os
from pathlib import Path
import time

# Agregar el directorio raíz del proyecto al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    import psycopg2
    from sqlalchemy import create_engine, text
    from src.config import settings
    import logging
    
    # Configurar logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    class DatabaseHealthChecker:
        """Clase para verificar la salud de la base de datos"""
        
        def __init__(self):
            self.connection_string = settings.database_url
            self.engine = None
            self.connection = None
            
        def test_direct_psycopg2_connection(self):
            """Probar conexión directa con psycopg2"""
            print("🔌 PROBANDO CONEXIÓN DIRECTA (psycopg2)")
            print("=" * 50)
            
            try:
                # Parsear la URL de conexión
                from urllib.parse import urlparse
                parsed = urlparse(self.connection_string)
                
                connection_params = {
                    'host': parsed.hostname,
                    'port': parsed.port or 5432,
                    'database': parsed.path[1:],  # Remover el slash inicial
                    'user': parsed.username,
                    'password': parsed.password
                }
                
                print(f"📡 Conectando a: {connection_params['host']}:{connection_params['port']}")
                print(f"🗄️ Base de datos: {connection_params['database']}")
                print(f"👤 Usuario: {connection_params['user']}")
                
                # Probar conexión
                start_time = time.time()
                conn = psycopg2.connect(**connection_params)
                connection_time = time.time() - start_time
                
                print(f"✅ Conexión exitosa en {connection_time:.2f}s")
                
                # Probar operaciones básicas
                with conn.cursor() as cur:
                    # Verificar versión
                    cur.execute("SELECT version()")
                    version = cur.fetchone()[0]
                    print(f"📊 PostgreSQL: {version[:50]}...")
                    
                    # Verificar timezone
                    cur.execute("SHOW timezone")
                    timezone = cur.fetchone()[0]
                    print(f"🕐 Timezone: {timezone}")
                    
                    # Verificar tablas
                    cur.execute("""
                        SELECT table_name, table_type 
                        FROM information_schema.tables 
                        WHERE table_schema = 'public'
                        ORDER BY table_name
                    """)
                    tables = cur.fetchall()
                    print(f"📋 Tablas encontradas: {len(tables)}")
                    
                    # Mostrar tablas principales
                    main_tables = ['users', 'packages', 'package_announcements', 'notifications', 'messages']
                    for table_name, table_type in tables:
                        if table_name in main_tables:
                            cur.execute(f"SELECT COUNT(*) FROM {table_name}")
                            count = cur.fetchone()[0]
                            print(f"  ✅ {table_name}: {count} registros")
                        elif table_type == 'BASE TABLE':
                            print(f"  📋 {table_name}: tabla del sistema")
                
                conn.close()
                return True
                
            except Exception as e:
                print(f"❌ Error de conexión directa: {e}")
                print(f"Tipo de error: {type(e).__name__}")
                return False
        
        def test_sqlalchemy_connection(self):
            """Probar conexión con SQLAlchemy"""
            print("\n🔧 PROBANDO CONEXIÓN SQLALCHEMY")
            print("=" * 50)
            
            try:
                # Crear engine con configuración específica
                self.engine = create_engine(
                    self.connection_string,
                    pool_pre_ping=True,
                    pool_recycle=300,
                    connect_args={
                        "options": "-c timezone=America/Bogota"
                    }
                )
                
                print("⚙️ Engine SQLAlchemy creado")
                
                # Probar conexión
                start_time = time.time()
                with self.engine.connect() as conn:
                    connection_time = time.time() - start_time
                    print(f"✅ Conexión SQLAlchemy en {connection_time:.2f}s")
                    
                    # Verificar configuración
                    result = conn.execute(text("SELECT current_setting('timezone')"))
                    current_tz = result.fetchone()[0]
                    print(f"🕐 Timezone configurado: {current_tz}")
                    
                    # Verificar permisos
                    result = conn.execute(text("SELECT current_user, current_database()"))
                    user, db = result.fetchone()
                    print(f"👤 Usuario actual: {user}")
                    print(f"🗄️ Base de datos actual: {db}")
                    
                    # Verificar conexiones activas
                    result = conn.execute(text("SELECT count(*) FROM pg_stat_activity"))
                    active_connections = result.fetchone()[0]
                    print(f"🔗 Conexiones activas: {active_connections}")
                
                return True
                
            except Exception as e:
                print(f"❌ Error de conexión SQLAlchemy: {e}")
                print(f"Tipo de error: {type(e).__name__}")
                return False
        
        def test_database_operations(self):
            """Probar operaciones básicas de la base de datos"""
            print("\n📝 PROBANDO OPERACIONES DE BASE DE DATOS")
            print("=" * 50)
            
            if not self.engine:
                print("❌ No hay engine SQLAlchemy disponible")
                return False
            
            try:
                with self.engine.connect() as conn:
                    # Probar SELECT simple
                    result = conn.execute(text("SELECT 1 as test"))
                    test_value = result.fetchone()[0]
                    print(f"✅ SELECT simple: {test_value}")
                    
                    # Probar función de fecha
                    result = conn.execute(text("SELECT NOW() as current_time"))
                    current_time = result.fetchone()[0]
                    print(f"✅ Función NOW(): {current_time}")
                    
                    # Probar información del sistema
                    result = conn.execute(text("SELECT version()"))
                    version = result.fetchone()[0]
                    print(f"✅ Versión PostgreSQL: {version[:50]}...")
                    
                    # Probar configuración de timezone
                    result = conn.execute(text("SELECT current_setting('timezone')"))
                    timezone = result.fetchone()[0]
                    print(f"✅ Timezone actual: {timezone}")
                    
                    # Probar información de la base de datos
                    result = conn.execute(text("SELECT current_database(), current_user"))
                    db, user = result.fetchone()
                    print(f"✅ Base de datos: {db}")
                    print(f"✅ Usuario: {user}")
                
                return True
                
            except Exception as e:
                print(f"❌ Error en operaciones: {e}")
                return False
        
        def run_health_check(self):
            """Ejecutar verificación completa de salud"""
            print("🏥 VERIFICACIÓN COMPLETA DE SALUD DE LA BASE DE DATOS")
            print("=" * 70)
            print()
            
            results = []
            
            # Probar conexión directa
            results.append(self.test_direct_psycopg2_connection())
            
            # Probar conexión SQLAlchemy
            results.append(self.test_sqlalchemy_connection())
            
            # Probar operaciones
            results.append(self.test_database_operations())
            
            # Resumen
            print("\n" + "=" * 70)
            successful = sum(results)
            total = len(results)
            
            print("📊 RESUMEN DE LA VERIFICACIÓN DE SALUD")
            print("=" * 70)
            print(f"✅ Pruebas exitosas: {successful}/{total}")
            
            if successful == total:
                print("🎉 ¡LA BASE DE DATOS ESTÁ COMPLETAMENTE SALUDABLE!")
                print("✅ Conexión directa: Funcionando")
                print("✅ Conexión SQLAlchemy: Funcionando")
                print("✅ Operaciones: Funcionando")
                print("✅ Timezone: Configurado para Colombia")
            else:
                print("⚠️ Algunas pruebas fallaron:")
                tests = ["Conexión directa", "SQLAlchemy", "Operaciones"]
                for i, result in enumerate(results):
                    status = "✅" if result else "❌"
                    print(f"   • {tests[i]}: {status}")
            
            return successful == total
    
    if __name__ == "__main__":
        checker = DatabaseHealthChecker()
        checker.run_health_check()
        
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("Asegúrate de ejecutar desde el directorio raíz del proyecto")
except Exception as e:
    print(f"❌ Error inesperado: {e}")
