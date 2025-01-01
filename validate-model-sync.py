#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PAQUETES EL CLUB v3.1 - Validación de Sincronización de Modelos
================================================================

Este script valida que los modelos SQLAlchemy estén sincronizados con la estructura real
de la base de datos, detectando inconsistencias como columnas faltantes o tipos incorrectos.
"""

import sys
import os
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
from datetime import datetime

# Agregar el directorio src al path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, 'code', 'src')
sys.path.insert(0, src_path)

try:
    from sqlalchemy import create_engine, text, inspect, MetaData
    from sqlalchemy.ext.declarative import DeclarativeMeta
    from sqlalchemy.orm import DeclarativeBase
    from config import settings
    from models import Base
    from models.user import User
    from models.package import Package
    from models.customer import Customer
    from models.file import File
    from models.message import Message
    from models.notification import Notification
    from models.announcement import PackageAnnouncement
    from models.password_reset import PasswordResetToken
    from models.user_activity_log import UserActivityLog
    from models.rate import Rate
except ImportError as e:
    print(f"❌ Error importando módulos: {e}")
    print("Asegúrate de ejecutar este script desde el directorio raíz del proyecto")
    sys.exit(1)

@dataclass
class ColumnInfo:
    """Información de una columna de base de datos"""
    name: str
    type: str
    nullable: bool
    default: Any
    primary_key: bool
    foreign_key: bool

@dataclass
class TableValidationResult:
    """Resultado de la validación de una tabla"""
    table_name: str
    is_synchronized: bool
    missing_columns: List[str]
    extra_columns: List[str]
    type_mismatches: List[Tuple[str, str, str]]  # (columna, tipo_modelo, tipo_bd)
    missing_foreign_keys: List[str]
    errors: List[str]

class ModelValidator:
    """Validador de sincronización entre modelos SQLAlchemy y base de datos"""
    
    def __init__(self):
        self.engine = None
        self.inspector = None
        self.metadata = None
        self.results: List[TableValidationResult] = []
        
    def connect(self):
        """Conectar a la base de datos"""
        try:
            self.engine = create_engine(settings.database_url)
            self.inspector = inspect(self.engine)
            self.metadata = MetaData()
            self.metadata.reflect(bind=self.engine)
            print("✅ Conectado a la base de datos correctamente")
            return True
        except Exception as e:
            print(f"❌ Error conectando a la base de datos: {e}")
            return False
    
    def get_model_tables(self) -> Dict[str, DeclarativeMeta]:
        """Obtener todos los modelos de la aplicación"""
        models = {
            'users': User,
            'packages': Package,
            'customers': Customer,
            'files': File,
            'messages': Message,
            'notifications': Notification,
            'package_announcements': PackageAnnouncement,
            'password_reset_tokens': PasswordResetToken,
            'user_activity_logs': UserActivityLog,
            'rates': Rate
        }
        return models
    
    def get_table_columns_from_db(self, table_name: str) -> Dict[str, ColumnInfo]:
        """Obtener información de columnas desde la base de datos"""
        columns = {}
        try:
            table_columns = self.inspector.get_columns(table_name)
            for col in table_columns:
                col_info = ColumnInfo(
                    name=col['name'],
                    type=str(col['type']),
                    nullable=col.get('nullable', True),
                    default=col.get('default'),
                    primary_key=col.get('primary_key', False),
                    foreign_key=False  # Se verifica por separado
                )
                columns[col['name']] = col_info
            
            # Verificar claves foráneas
            foreign_keys = self.inspector.get_foreign_keys(table_name)
            for fk in foreign_keys:
                for col_name in fk['constrained_columns']:
                    if col_name in columns:
                        columns[col_name].foreign_key = True
                        
        except Exception as e:
            print(f"⚠️  Error obteniendo columnas de {table_name}: {e}")
            
        return columns
    
    def get_table_columns_from_model(self, model_class) -> Dict[str, ColumnInfo]:
        """Obtener información de columnas desde el modelo SQLAlchemy"""
        columns = {}
        try:
            for column in model_class.__table__.columns:
                col_info = ColumnInfo(
                    name=column.name,
                    type=str(column.type),
                    nullable=column.nullable,
                    default=column.default.arg if column.default else None,
                    primary_key=column.primary_key,
                    foreign_key=bool(column.foreign_keys)
                )
                columns[column.name] = col_info
        except Exception as e:
            print(f"⚠️  Error obteniendo columnas del modelo {model_class.__name__}: {e}")
            
        return columns
    
    def compare_columns(self, db_columns: Dict[str, ColumnInfo], 
                       model_columns: Dict[str, ColumnInfo]) -> Tuple[List[str], List[str], List[Tuple[str, str, str]]]:
        """Comparar columnas entre base de datos y modelo"""
        missing_columns = []
        extra_columns = []
        type_mismatches = []
        
        # Verificar columnas faltantes en BD
        for col_name, model_col in model_columns.items():
            if col_name not in db_columns:
                missing_columns.append(col_name)
            else:
                # Verificar tipos de datos
                db_col = db_columns[col_name]
                if not self._types_compatible(model_col.type, db_col.type):
                    type_mismatches.append((col_name, model_col.type, db_col.type))
        
        # Verificar columnas extra en BD
        for col_name in db_columns:
            if col_name not in model_columns:
                extra_columns.append(col_name)
        
        return missing_columns, extra_columns, type_mismatches
    
    def _types_compatible(self, model_type: str, db_type: str) -> bool:
        """Verificar si los tipos de datos son compatibles"""
        # Normalizar tipos
        model_type = model_type.lower()
        db_type = db_type.lower()
        
        # Mapeo de tipos compatibles
        type_mapping = {
            'string': ['character varying', 'varchar', 'text', 'char'],
            'integer': ['integer', 'int', 'bigint', 'smallint'],
            'boolean': ['boolean', 'bool'],
            'datetime': ['timestamp', 'timestamp with time zone', 'timestamptz'],
            'date': ['date'],
            'uuid': ['uuid'],
            'text': ['text', 'character varying', 'varchar'],
            'float': ['real', 'double precision', 'numeric', 'decimal']
        }
        
        # Verificar compatibilidad
        for compatible_types in type_mapping.values():
            if model_type in compatible_types or db_type in compatible_types:
                return True
        
        # Verificar coincidencia exacta
        return model_type == db_type
    
    def validate_table(self, table_name: str, model_class) -> TableValidationResult:
        """Validar una tabla específica"""
        print(f"🔍 Validando tabla: {table_name}")
        
        result = TableValidationResult(
            table_name=table_name,
            is_synchronized=True,
            missing_columns=[],
            extra_columns=[],
            type_mismatches=[],
            missing_foreign_keys=[],
            errors=[]
        )
        
        try:
            # Obtener columnas desde BD y modelo
            db_columns = self.get_table_columns_from_db(table_name)
            model_columns = self.get_table_columns_from_model(model_class)
            
            if not db_columns:
                result.errors.append(f"No se pudieron obtener columnas de la BD para {table_name}")
                result.is_synchronized = False
                return result
            
            if not model_columns:
                result.errors.append(f"No se pudieron obtener columnas del modelo para {table_name}")
                result.is_synchronized = False
                return result
            
            # Comparar columnas
            missing, extra, type_mismatches = self.compare_columns(db_columns, model_columns)
            
            result.missing_columns = missing
            result.extra_columns = extra
            result.type_mismatches = type_mismatches
            
            # Determinar si está sincronizada
            if missing or type_mismatches:
                result.is_synchronized = False
            
            # Mostrar resultado
            if result.is_synchronized:
                print(f"   ✅ {table_name}: Sincronizada correctamente")
            else:
                print(f"   ❌ {table_name}: Inconsistencias encontradas")
                if missing:
                    print(f"      - Columnas faltantes: {', '.join(missing)}")
                if extra:
                    print(f"      - Columnas extra: {', '.join(extra)}")
                if type_mismatches:
                    print(f"      - Incompatibilidades de tipo: {len(type_mismatches)}")
            
        except Exception as e:
            result.errors.append(str(e))
            result.is_synchronized = False
            print(f"   ❌ {table_name}: Error durante validación - {e}")
        
        return result
    
    def validate_all_tables(self):
        """Validar todas las tablas"""
        print("\n🔍 Iniciando validación de sincronización...")
        print("=" * 60)
        
        if not self.connect():
            return False
        
        models = self.get_model_tables()
        
        for table_name, model_class in models.items():
            try:
                result = self.validate_table(table_name, model_class)
                self.results.append(result)
            except Exception as e:
                print(f"❌ Error validando {table_name}: {e}")
        
        return True
    
    def generate_report(self):
        """Generar reporte de validación"""
        print("\n" + "=" * 60)
        print("📊 REPORTE DE VALIDACIÓN DE SINCRONIZACIÓN")
        print("=" * 60)
        
        total_tables = len(self.results)
        synchronized_tables = sum(1 for r in self.results if r.is_synchronized)
        error_tables = total_tables - synchronized_tables
        
        print(f"📈 Resumen General:")
        print(f"   - Tablas validadas: {total_tables}")
        print(f"   - Tablas sincronizadas: {synchronized_tables}")
        print(f"   - Tablas con problemas: {error_tables}")
        
        if error_tables > 0:
            print(f"\n⚠️  TABLAS CON PROBLEMAS:")
            for result in self.results:
                if not result.is_synchronized:
                    print(f"\n   🔴 {result.table_name.upper()}:")
                    if result.missing_columns:
                        print(f"      ❌ Columnas faltantes: {', '.join(result.missing_columns)}")
                    if result.type_mismatches:
                        print(f"      ⚠️  Incompatibilidades de tipo:")
                        for col, model_type, db_type in result.type_mismatches:
                            print(f"         - {col}: Modelo={model_type}, BD={db_type}")
                    if result.errors:
                        print(f"      💥 Errores: {', '.join(result.errors)}")
        else:
            print(f"\n🎉 ¡TODAS LAS TABLAS ESTÁN SINCRONIZADAS CORRECTAMENTE!")
        
        print(f"\n📋 Detalles por tabla:")
        for result in self.results:
            status = "✅" if result.is_synchronized else "❌"
            print(f"   {status} {result.table_name}")
        
        return error_tables == 0

def main():
    """Función principal"""
    print("🛡️  VALIDADOR DE SINCRONIZACIÓN DE MODELOS")
    print("=" * 60)
    print(f"⏰ Iniciado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    validator = ModelValidator()
    
    if validator.validate_all_tables():
        success = validator.generate_report()
        if success:
            print("\n🎉 ¡Validación completada exitosamente!")
            sys.exit(0)
        else:
            print("\n⚠️  Se encontraron inconsistencias que requieren atención")
            sys.exit(1)
    else:
        print("\n❌ Error durante la validación")
        sys.exit(1)

if __name__ == "__main__":
    main()
