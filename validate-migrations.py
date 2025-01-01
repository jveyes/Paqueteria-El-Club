#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PAQUETES EL CLUB v3.1 - Validación de Migraciones Alembic
==========================================================

Este script valida el estado de las migraciones de Alembic y verifica que estén
correctamente aplicadas en la base de datos.
"""

import sys
import os
import subprocess
from typing import List, Dict, Tuple
from dataclasses import dataclass
from datetime import datetime

# Agregar el directorio src al path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, 'code', 'src')
sys.path.insert(0, src_path)

try:
    from sqlalchemy import create_engine, text
    from config import settings
except ImportError as e:
    print(f"❌ Error importando módulos: {e}")
    print("Asegúrate de ejecutar este script desde el directorio raíz del proyecto")
    sys.exit(1)

@dataclass
class MigrationInfo:
    """Información de una migración"""
    revision: str
    description: str
    applied: bool
    applied_date: str = None
    error: str = None

class MigrationValidator:
    """Validador de migraciones de Alembic"""
    
    def __init__(self):
        self.engine = None
        self.migrations_dir = os.path.join('code', 'alembic', 'versions')
        self.results: List[MigrationInfo] = []
        
    def connect(self):
        """Conectar a la base de datos"""
        try:
            self.engine = create_engine(settings.database_url)
            print("✅ Conectado a la base de datos correctamente")
            return True
        except Exception as e:
            print(f"❌ Error conectando a la base de datos: {e}")
            return False
    
    def get_migration_files(self) -> List[str]:
        """Obtener lista de archivos de migración"""
        migrations = []
        try:
            if os.path.exists(self.migrations_dir):
                for file in os.listdir(self.migrations_dir):
                    if file.endswith('.py') and not file.startswith('__'):
                        migrations.append(file)
                migrations.sort()
            else:
                print(f"⚠️  Directorio de migraciones no encontrado: {self.migrations_dir}")
        except Exception as e:
            print(f"❌ Error leyendo directorio de migraciones: {e}")
        
        return migrations
    
    def get_current_version_from_db(self) -> str:
        """Obtener versión actual desde la base de datos"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT version_num FROM alembic_version"))
                row = result.fetchone()
                if row:
                    return row[0]
                else:
                    return "No hay versión registrada"
        except Exception as e:
            print(f"❌ Error obteniendo versión actual: {e}")
            return "Error"
    
    def get_applied_migrations_from_db(self) -> List[str]:
        """Obtener migraciones aplicadas desde la base de datos"""
        applied = []
        try:
            with self.engine.connect() as conn:
                # Verificar si existe la tabla alembic_version
                result = conn.execute(text("""
                    SELECT table_name FROM information_schema.tables 
                    WHERE table_name = 'alembic_version'
                """))
                if not result.fetchone():
                    print("⚠️  Tabla alembic_version no existe")
                    return applied
                
                # Obtener versión actual
                result = conn.execute(text("SELECT version_num FROM alembic_version"))
                row = result.fetchone()
                if row:
                    applied.append(row[0])
                    
        except Exception as e:
            print(f"❌ Error obteniendo migraciones aplicadas: {e}")
        
        return applied
    
    def parse_migration_file(self, filename: str) -> Tuple[str, str]:
        """Parsear archivo de migración para obtener revisión y descripción"""
        revision = filename.split('_')[0]
        description = filename.replace('.py', '').replace(f'{revision}_', '')
        return revision, description
    
    def validate_migration(self, filename: str, applied_migrations: List[str]) -> MigrationInfo:
        """Validar una migración específica"""
        revision, description = self.parse_migration_file(filename)
        
        migration = MigrationInfo(
            revision=revision,
            description=description,
            applied=revision in applied_migrations
        )
        
        if migration.applied:
            print(f"   ✅ {revision}: {description}")
        else:
            print(f"   ❌ {revision}: {description} (NO APLICADA)")
        
        return migration
    
    def validate_all_migrations(self):
        """Validar todas las migraciones"""
        print("\n🔍 Iniciando validación de migraciones...")
        print("=" * 60)
        
        if not self.connect():
            return False
        
        # Obtener migraciones del sistema de archivos
        migration_files = self.get_migration_files()
        if not migration_files:
            print("❌ No se encontraron archivos de migración")
            return False
        
        print(f"📁 Archivos de migración encontrados: {len(migration_files)}")
        
        # Obtener migraciones aplicadas desde BD
        applied_migrations = self.get_applied_migrations_from_db()
        current_version = self.get_current_version_from_db()
        
        print(f"🗄️  Versión actual en BD: {current_version}")
        print(f"📊 Migraciones aplicadas: {len(applied_migrations)}")
        
        # Validar cada migración
        for filename in migration_files:
            migration = self.validate_migration(filename, applied_migrations)
            self.results.append(migration)
        
        return True
    
    def check_migration_consistency(self):
        """Verificar consistencia de las migraciones"""
        print("\n🔍 Verificando consistencia de migraciones...")
        
        if not self.results:
            print("❌ No hay resultados de validación")
            return False
        
        # Verificar secuencia de migraciones
        revisions = [m.revision for m in self.results]
        applied_revisions = [m.revision for m in self.results if m.applied]
        
        print(f"📋 Secuencia de migraciones: {' -> '.join(revisions)}")
        print(f"✅ Migraciones aplicadas: {' -> '.join(applied_revisions)}")
        
        # Verificar si hay gaps en las migraciones aplicadas
        if len(applied_revisions) > 1:
            for i in range(len(applied_revisions) - 1):
                current_idx = revisions.index(applied_revisions[i])
                next_idx = revisions.index(applied_revisions[i + 1])
                if next_idx - current_idx > 1:
                    print(f"⚠️  Gap detectado entre {applied_revisions[i]} y {applied_revisions[i + 1]}")
        
        return True
    
    def generate_report(self):
        """Generar reporte de validación"""
        print("\n" + "=" * 60)
        print("📊 REPORTE DE VALIDACIÓN DE MIGRACIONES")
        print("=" * 60)
        
        total_migrations = len(self.results)
        applied_migrations = sum(1 for m in self.results if m.applied)
        pending_migrations = total_migrations - applied_migrations
        
        print(f"📈 Resumen General:")
        print(f"   - Total de migraciones: {total_migrations}")
        print(f"   - Migraciones aplicadas: {applied_migrations}")
        print(f"   - Migraciones pendientes: {pending_migrations}")
        
        if pending_migrations > 0:
            print(f"\n⚠️  MIGRACIONES PENDIENTES:")
            for migration in self.results:
                if not migration.applied:
                    print(f"   🔴 {migration.revision}: {migration.description}")
            
            print(f"\n💡 RECOMENDACIONES:")
            print(f"   1. Ejecutar migraciones pendientes: alembic upgrade head")
            print(f"   2. Verificar que no haya conflictos en las migraciones")
            print(f"   3. Probar la aplicación después de aplicar las migraciones")
        else:
            print(f"\n🎉 ¡TODAS LAS MIGRACIONES ESTÁN APLICADAS!")
        
        print(f"\n📋 Estado por migración:")
        for migration in self.results:
            status = "✅" if migration.applied else "❌"
            print(f"   {status} {migration.revision}: {migration.description}")
        
        return pending_migrations == 0
    
    def suggest_fixes(self):
        """Sugerir correcciones para problemas encontrados"""
        print(f"\n🔧 SUGERENCIAS DE CORRECCIÓN:")
        
        pending_count = sum(1 for m in self.results if not m.applied)
        
        if pending_count > 0:
            print(f"   1. Aplicar migraciones pendientes:")
            print(f"      cd code")
            print(f"      alembic upgrade head")
            print(f"")
            print(f"   2. Si hay problemas con migraciones específicas:")
            print(f"      alembic current  # Ver estado actual")
            print(f"      alembic history  # Ver historial")
            print(f"      alembic downgrade -1  # Revertir última migración")
            print(f"")
            print(f"   3. Verificar integridad de la base de datos:")
            print(f"      python validate-model-sync.py")
        
        print(f"   4. Reiniciar la aplicación después de aplicar migraciones:")
        print(f"      docker restart paqueteria_v31_app")

def main():
    """Función principal"""
    print("🛡️  VALIDADOR DE MIGRACIONES ALEMBIC")
    print("=" * 60)
    print(f"⏰ Iniciado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    validator = MigrationValidator()
    
    if validator.validate_all_migrations():
        validator.check_migration_consistency()
        success = validator.generate_report()
        validator.suggest_fixes()
        
        if success:
            print("\n🎉 ¡Validación de migraciones completada exitosamente!")
            sys.exit(0)
        else:
            print("\n⚠️  Se encontraron migraciones pendientes que requieren atención")
            sys.exit(1)
    else:
        print("\n❌ Error durante la validación de migraciones")
        sys.exit(1)

if __name__ == "__main__":
    main()
