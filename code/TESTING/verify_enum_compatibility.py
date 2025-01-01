#!/usr/bin/env python3
"""
Script para verificar la compatibilidad de tipos enum entre código y base de datos
PAQUETES EL CLUB v3.1
"""

import psycopg2
import re
import os
from datetime import datetime

# Configuración de AWS RDS
AWS_DB_CONFIG = {
    'host': 'ls-abe25e9bea57818f0ee32555c0e7b4a10e361535.ctobuhtlkwoj.us-east-1.rds.amazonaws.com',
    'port': 5432,
    'database': 'paqueteria',
    'user': 'jveyes',
    'password': 'a?HC!2.*1#?[==:|289qAI=)#V4kDzl$'
}

def print_header(title):
    """Imprimir encabezado de sección"""
    print(f"\n{'='*80}")
    print(f"🔍 {title}")
    print(f"{'='*80}")

def print_subheader(title):
    """Imprimir subencabezado"""
    print(f"\n{'='*60}")
    print(f"📋 {title}")
    print(f"{'='*60}")

def get_database_enums():
    """Obtener tipos enum de la base de datos"""
    try:
        conn = psycopg2.connect(**AWS_DB_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT t.typname, e.enumlabel
            FROM pg_type t
            JOIN pg_enum e ON t.oid = e.enumtypid
            WHERE t.typtype = 'e'
            ORDER BY t.typname, e.enumsortorder
        """)
        
        enums = cursor.fetchall()
        
        # Organizar por tipo
        enum_dict = {}
        for enum_name, enum_value in enums:
            if enum_name not in enum_dict:
                enum_dict[enum_name] = []
            enum_dict[enum_name].append(enum_value)
        
        cursor.close()
        conn.close()
        
        return enum_dict
        
    except Exception as e:
        print(f"❌ Error obteniendo enums de la base de datos: {e}")
        return {}

def get_code_enums():
    """Obtener tipos enum del código"""
    enum_dict = {}
    
    # Buscar en archivos de modelos
    models_dir = "src/models"
    if os.path.exists(models_dir):
        for file in os.listdir(models_dir):
            if file.endswith('.py'):
                file_path = os.path.join(models_dir, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Buscar definiciones de enum
                    enum_matches = re.findall(r'class\s+(\w+)\s*\([^)]*enum[^)]*\):.*?class\s+\w+', content, re.DOTALL)
                    
                    for enum_match in enum_matches:
                        # Buscar valores del enum
                        enum_values = re.findall(r'(\w+)\s*=\s*["\']([^"\']+)["\']', enum_match)
                        if enum_values:
                            enum_name = enum_values[0][0] if enum_values else "Unknown"
                            values = [value for _, value in enum_values]
                            enum_dict[enum_name] = values
                    
                except Exception as e:
                    print(f"❌ Error analizando {file_path}: {e}")
    
    return enum_dict

def verify_enum_compatibility():
    """Verificar compatibilidad de enums"""
    print_header("VERIFICACIÓN DE COMPATIBILIDAD DE TIPOS ENUM")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Obtener enums de la base de datos
    print_subheader("TIPOS ENUM EN LA BASE DE DATOS")
    db_enums = get_database_enums()
    
    for enum_name, enum_values in db_enums.items():
        print(f"📋 {enum_name}: {', '.join(enum_values)}")
    
    # Obtener enums del código
    print_subheader("TIPOS ENUM EN EL CÓDIGO")
    code_enums = get_code_enums()
    
    for enum_name, enum_values in code_enums.items():
        print(f"📋 {enum_name}: {', '.join(enum_values)}")
    
    # Comparar compatibilidad
    print_subheader("ANÁLISIS DE COMPATIBILIDAD")
    
    compatibility_issues = []
    
    # Verificar enums críticos
    critical_enums = {
        "userrole": ["ADMIN", "OPERATOR", "USER"],
        "packagestatus": ["ANUNCIADO", "RECIBIDO", "EN_TRANSITO", "ENTREGADO", "CANCELADO"],
        "packagetype": ["NORMAL", "EXTRA_DIMENSIONADO"],
        "packagecondition": ["BUENO", "REGULAR", "MALO"],
        "notificationtype": ["EMAIL", "SMS", "PUSH"],
        "notificationstatus": ["PENDING", "SENT", "FAILED", "DELIVERED"],
        "messagetype": ["INTERNAL", "SUPPORT", "SYSTEM"],
        "ratetype": ["STORAGE", "DELIVERY", "PACKAGE_TYPE"]
    }
    
    for expected_enum, expected_values in critical_enums.items():
        print(f"\n🔍 Verificando {expected_enum}")
        
        if expected_enum in db_enums:
            db_values = db_enums[expected_enum]
            if set(db_values) == set(expected_values):
                print(f"   ✅ Compatible: {', '.join(db_values)}")
            else:
                print(f"   ❌ Incompatible:")
                print(f"      Base de datos: {', '.join(db_values)}")
                print(f"      Esperado: {', '.join(expected_values)}")
                compatibility_issues.append(f"Enum {expected_enum} incompatible")
        else:
            print(f"   ⚠️  No encontrado en la base de datos")
            compatibility_issues.append(f"Enum {expected_enum} no encontrado en BD")
    
    print_subheader("RESUMEN DE COMPATIBILIDAD")
    if compatibility_issues:
        print(f"❌ Se encontraron {len(compatibility_issues)} problemas de compatibilidad:")
        for issue in compatibility_issues:
            print(f"   ⚠️  {issue}")
    else:
        print("✅ Todos los tipos enum son compatibles")
    
    print_header("VERIFICACIÓN COMPLETADA")

if __name__ == "__main__":
    verify_enum_compatibility()
