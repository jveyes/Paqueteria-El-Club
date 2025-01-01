#!/usr/bin/env python3
"""
Script para extraer y migrar datos del backup de manera directa (versión corregida)
"""

import os
import sys
import re
from sqlalchemy import create_engine, text

def main():
    try:
        print("🚀 ========================================")
        print("🚀 EXTRACCIÓN Y MIGRACIÓN DE DATOS")
        print("🚀 PAQUETES EL CLUB v3.1")
        print("🚀 ========================================")
        print("")
        
        # URL de la base de datos AWS
        database_url = "postgresql://jveyes:a?HC!2.*1#?[==:|289qAI=)#V4kDzl$@ls-abe25e9bea57818f0ee32555c0e7b4a10e361535.ctobuhtlkwoj.us-east-1.rds.amazonaws.com:5432/paqueteria"
        
        print("🔍 Conectando a la base de datos AWS...")
        engine = create_engine(database_url)
        
        # Verificar conexión
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Conexión a base de datos AWS establecida")
        
        # Leer el archivo de backup
        backup_file = "/app/backup.sql"
        
        if not os.path.exists(backup_file):
            print(f"❌ Error: No se encontró el archivo de backup: {backup_file}")
            return False
        
        print(f"📖 Leyendo archivo de backup: {backup_file}")
        with open(backup_file, 'r', encoding='utf-8') as f:
            backup_content = f.read()
        
        print(f"📊 Tamaño del backup: {len(backup_content)} caracteres")
        
        # Buscar secciones de datos específicas
        print("🔧 Analizando contenido del backup...")
        
        # Buscar sección de usuarios
        users_section = re.search(r'-- TOC entry.*users.*Type: TABLE DATA.*?COPY public\.users.*?FROM stdin;(.*?)\\\.', backup_content, re.DOTALL | re.IGNORECASE)
        
        # Buscar sección de anuncios de paquetes
        announcements_section = re.search(r'-- TOC entry.*package_announcements.*Type: TABLE DATA.*?COPY public\.package_announcements.*?FROM stdin;(.*?)\\\.', backup_content, re.DOTALL | re.IGNORECASE)
        
        # Buscar sección de tokens de reset
        tokens_section = re.search(r'-- TOC entry.*password_reset_tokens.*Type: TABLE DATA.*?COPY public\.password_reset_tokens.*?FROM stdin;(.*?)\\\.', backup_content, re.DOTALL | re.IGNORECASE)
        
        print(f"📋 Secciones encontradas:")
        print(f"   - Usuarios: {'✅' if users_section else '❌'}")
        print(f"   - Anuncios: {'✅' if announcements_section else '❌'}")
        print(f"   - Tokens: {'✅' if tokens_section else '❌'}")
        
        # Migrar datos de usuarios
        if users_section:
            print("\n👥 Migrando usuarios...")
            users_data = users_section.group(1).strip()
            if users_data:
                # Parsear datos de usuarios
                user_lines = users_data.split('\n')
                for line in user_lines:
                    if line.strip():
                        # Parsear línea de usuario (formato: id, created_at, updated_at, username, email, password_hash, first_name, last_name, phone, is_active, role, permissions, last_login)
                        parts = line.split('\t')
                        if len(parts) >= 11:
                            user_id, created_at, updated_at, username, email, password_hash, first_name, last_name, phone, is_active, role = parts[:11]
                            
                            # Insertar usuario
                            insert_sql = f"""
                            INSERT INTO users (id, created_at, updated_at, username, email, password_hash, first_name, last_name, phone, is_active, role)
                            VALUES ('{user_id}', '{created_at}', '{updated_at}', '{username}', '{email}', '{password_hash}', '{first_name}', '{last_name}', '{phone}', {is_active.lower() == 't'}, '{role}')
                            ON CONFLICT (id) DO NOTHING;
                            """
                            
                            try:
                                with engine.connect() as conn:
                                    conn.execute(text(insert_sql))
                                    conn.commit()
                                print(f"   ✅ Usuario migrado: {username}")
                            except Exception as e:
                                print(f"   ⚠️  Error migrando usuario {username}: {e}")
        
        # Migrar datos de anuncios de paquetes
        if announcements_section:
            print("\n📦 Migrando anuncios de paquetes...")
            announcements_data = announcements_section.group(1).strip()
            if announcements_data:
                # Parsear datos de anuncios
                ann_lines = announcements_data.split('\n')
                for line in ann_lines:
                    if line.strip():
                        # Parsear línea de anuncio
                        parts = line.split('\t')
                        if len(parts) >= 13:
                            ann_id, customer_name, phone_number, guide_number, is_active, is_processed, announced_at, processed_at, customer_id, package_id, created_at, updated_at, tracking_code = parts[:13]
                            
                            # Preparar valores para SQL
                            processed_at_val = f"'{processed_at}'" if processed_at != '\\N' else 'NULL'
                            customer_id_val = f"'{customer_id}'" if customer_id != '\\N' else 'NULL'
                            package_id_val = f"'{package_id}'" if package_id != '\\N' else 'NULL'
                            
                            # Insertar anuncio
                            insert_sql = f"""
                            INSERT INTO package_announcements (id, customer_name, phone_number, guide_number, is_active, is_processed, announced_at, processed_at, customer_id, package_id, created_at, updated_at, tracking_code)
                            VALUES ('{ann_id}', '{customer_name}', '{phone_number}', '{guide_number}', {is_active.lower() == 't'}, {is_processed.lower() == 't'}, '{announced_at}', {processed_at_val}, {customer_id_val}, {package_id_val}, '{created_at}', '{updated_at}', '{tracking_code}')
                            ON CONFLICT (id) DO NOTHING;
                            """
                            
                            try:
                                with engine.connect() as conn:
                                    conn.execute(text(insert_sql))
                                    conn.commit()
                                print(f"   ✅ Anuncio migrado: {customer_name} - {guide_number}")
                            except Exception as e:
                                print(f"   ⚠️  Error migrando anuncio {customer_name}: {e}")
        
        # Migrar datos de tokens de reset
        if tokens_section:
            print("\n🔑 Migrando tokens de reset...")
            tokens_data = tokens_section.group(1).strip()
            if tokens_data:
                # Parsear datos de tokens
                token_lines = tokens_data.split('\n')
                for line in token_lines:
                    if line.strip():
                        # Parsear línea de token
                        parts = line.split('\t')
                        if len(parts) >= 6:
                            token_id, token, user_id, expires_at, used, created_at = parts[:6]
                            
                            # Insertar token
                            insert_sql = f"""
                            INSERT INTO password_reset_tokens (id, token, user_id, expires_at, used, created_at)
                            VALUES ({token_id}, '{token}', '{user_id}', '{expires_at}', {used.lower() == 't'}, '{created_at}')
                            ON CONFLICT (id) DO NOTHING;
                            """
                            
                            try:
                                with engine.connect() as conn:
                                    conn.execute(text(insert_sql))
                                    conn.commit()
                                print(f"   ✅ Token migrado: {token_id}")
                            except Exception as e:
                                print(f"   ⚠️  Error migrando token {token_id}: {e}")
        
        # Verificar datos migrados
        print("\n🔍 Verificando datos migrados...")
        with engine.connect() as conn:
            # Verificar usuarios
            result = conn.execute(text("SELECT COUNT(*) FROM users"))
            user_count = result.fetchone()[0]
            print(f"👥 Usuarios: {user_count}")
            
            # Verificar anuncios de paquetes
            result = conn.execute(text("SELECT COUNT(*) FROM package_announcements"))
            ann_count = result.fetchone()[0]
            print(f"📦 Anuncios de paquetes: {ann_count}")
            
            # Verificar tokens de reset
            result = conn.execute(text("SELECT COUNT(*) FROM password_reset_tokens"))
            token_count = result.fetchone()[0]
            print(f"🔑 Tokens de reset: {token_count}")
            
            # Mostrar usuarios específicos
            if user_count > 0:
                print("\n👤 Usuarios disponibles:")
                result = conn.execute(text("SELECT username, email, first_name, last_name, role, is_active FROM users"))
                users = result.fetchall()
                for user in users:
                    username, email, first_name, last_name, role, is_active = user
                    status = "✅ Activo" if is_active else "❌ Inactivo"
                    print(f"   - {username} ({email}) - {first_name} {last_name} - {role} - {status}")
            
            # Mostrar algunos anuncios de paquetes
            if ann_count > 0:
                print(f"\n📦 Últimos {min(5, ann_count)} anuncios de paquetes:")
                result = conn.execute(text("SELECT customer_name, phone_number, guide_number, tracking_code, announced_at FROM package_announcements ORDER BY announced_at DESC LIMIT 5"))
                announcements = result.fetchall()
                for ann in announcements:
                    customer_name, phone, guide, tracking, announced = ann
                    print(f"   - {customer_name} ({phone}) - Guía: {guide} - Código: {tracking} - {announced}")
        
        # Calcular total de registros
        total_records = user_count + ann_count + token_count
        
        print(f"\n📊 RESUMEN DE MIGRACIÓN:")
        print("=" * 40)
        print(f"📈 Total de registros migrados: {total_records}")
        print(f"👥 Usuarios: {user_count}")
        print(f"📦 Anuncios: {ann_count}")
        print(f"🔑 Tokens: {token_count}")
        
        print(f"\n🌐 URLs de acceso:")
        print("=" * 30)
        print(f"🔗 Aplicación: https://guia.papyrus.com.co")
        print(f"🔗 Health Check: https://guia.papyrus.com.co/health")
        print(f"🔗 API: https://guia.papyrus.com.co/api/")
        
        print(f"\n✅ MIGRACIÓN DE DATOS COMPLETADA!")
        print("🎉 Los datos han sido migrados a AWS RDS")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🚀 ¡Migración completada! Puedes acceder a tu aplicación en la nube.")
    else:
        print("\n❌ Error en la migración")
