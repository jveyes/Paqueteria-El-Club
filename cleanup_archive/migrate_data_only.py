#!/usr/bin/env python3
"""
Script para migrar solo los datos INSERT del backup a la base de datos AWS RDS
"""

import os
import sys
import re
from sqlalchemy import create_engine, text

def main():
    try:
        print("🚀 ========================================")
        print("🚀 MIGRACIÓN DE DATOS A AWS RDS")
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
        
        # Extraer solo los comandos INSERT
        print("🔧 Extrayendo comandos INSERT...")
        
        # Buscar todos los comandos INSERT en el backup
        insert_pattern = r'INSERT INTO [^;]+;'
        insert_commands = re.findall(insert_pattern, backup_content, re.IGNORECASE | re.DOTALL)
        
        print(f"📋 Se encontraron {len(insert_commands)} comandos INSERT")
        
        if not insert_commands:
            print("❌ No se encontraron comandos INSERT en el backup")
            return False
        
        # Ejecutar los comandos INSERT
        print("🔄 Ejecutando migración de datos...")
        successful_commands = 0
        failed_commands = 0
        
        with engine.connect() as conn:
            for i, command in enumerate(insert_commands):
                try:
                    if command.strip():
                        # Limpiar el comando
                        clean_command = command.strip()
                        if clean_command.endswith(';'):
                            clean_command = clean_command[:-1]  # Remover el punto y coma final
                        
                        conn.execute(text(clean_command))
                        successful_commands += 1
                        
                        # Mostrar progreso cada 5 comandos
                        if (i + 1) % 5 == 0:
                            print(f"   Progreso: {i + 1}/{len(insert_commands)} comandos INSERT ejecutados")
                            
                except Exception as e:
                    failed_commands += 1
                    error_msg = str(e)
                    
                    # Ignorar errores esperados
                    if any(ignored in error_msg.lower() for ignored in [
                        'already exists', 'duplicate key', 'constraint'
                    ]):
                        print(f"   ⚠️  Registro duplicado en comando {i + 1} (ignorado)")
                        continue
                    else:
                        print(f"   ❌ Error en comando {i + 1}: {error_msg[:100]}...")
            
            # Commit de todos los cambios
            conn.commit()
        
        print(f"✅ Migración de datos completada:")
        print(f"   - Comandos INSERT exitosos: {successful_commands}")
        print(f"   - Comandos INSERT fallidos: {failed_commands}")
        
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
            
            # Verificar paquetes
            result = conn.execute(text("SELECT COUNT(*) FROM packages"))
            pack_count = result.fetchone()[0]
            print(f"📦 Paquetes: {pack_count}")
            
            # Verificar clientes
            result = conn.execute(text("SELECT COUNT(*) FROM customers"))
            cust_count = result.fetchone()[0]
            print(f"👤 Clientes: {cust_count}")
            
            # Verificar notificaciones
            result = conn.execute(text("SELECT COUNT(*) FROM notifications"))
            notif_count = result.fetchone()[0]
            print(f"🔔 Notificaciones: {notif_count}")
            
            # Verificar tarifas
            result = conn.execute(text("SELECT COUNT(*) FROM rates"))
            rate_count = result.fetchone()[0]
            print(f"💰 Tarifas: {rate_count}")
            
            # Verificar archivos
            result = conn.execute(text("SELECT COUNT(*) FROM files"))
            file_count = result.fetchone()[0]
            print(f"📁 Archivos: {file_count}")
            
            # Verificar mensajes
            result = conn.execute(text("SELECT COUNT(*) FROM messages"))
            msg_count = result.fetchone()[0]
            print(f"💬 Mensajes: {msg_count}")
            
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
        total_records = user_count + ann_count + pack_count + cust_count + notif_count + rate_count + file_count + msg_count + token_count
        
        print(f"\n📊 RESUMEN DE MIGRACIÓN:")
        print("=" * 40)
        print(f"📈 Total de registros migrados: {total_records}")
        print(f"✅ Comandos INSERT exitosos: {successful_commands}")
        print(f"⚠️  Comandos INSERT fallidos: {failed_commands}")
        if (successful_commands + failed_commands) > 0:
            print(f"🎯 Tasa de éxito: {(successful_commands/(successful_commands+failed_commands)*100):.1f}%")
        
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
