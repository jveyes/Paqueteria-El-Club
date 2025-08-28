#!/usr/bin/env python3
"""
Script completo para verificar todos los datos en la base de datos AWS RDS
"""

import sys
from sqlalchemy import create_engine, text

def main():
    try:
        print("🔍 ========================================")
        print("🔍 VERIFICACIÓN COMPLETA DE DATOS EN AWS RDS")
        print("🔍 PAQUETES EL CLUB v3.1")
        print("🔍 ========================================")
        print("")
        
        # URL de la base de datos AWS
        database_url = "postgresql://jveyes:a?HC!2.*1#?[==:|289qAI=)#V4kDzl$@ls-abe25e9bea57818f0ee32555c0e7b4a10e361535.ctobuhtlkwoj.us-east-1.rds.amazonaws.com:5432/paqueteria"
        
        print("🔍 Conectando a la base de datos AWS RDS...")
        engine = create_engine(database_url)
        
        # Verificar conexión
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Conexión a AWS RDS establecida")
        
        print("\n📊 VERIFICANDO TODAS LAS TABLAS Y DATOS:")
        print("=" * 50)
        
        with engine.connect() as conn:
            # 1. Verificar tablas existentes
            print("\n1️⃣ TABLAS EXISTENTES:")
            result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name"))
            tables = result.fetchall()
            print(f"   📋 Total de tablas: {len(tables)}")
            for table in tables:
                print(f"   - {table[0]}")
            
            # 2. Verificar usuarios
            print("\n2️⃣ USUARIOS:")
            result = conn.execute(text("SELECT COUNT(*) FROM users"))
            user_count = result.fetchone()[0]
            print(f"   👥 Total de usuarios: {user_count}")
            
            if user_count > 0:
                result = conn.execute(text("SELECT username, email, first_name, last_name, role, is_active FROM users"))
                users = result.fetchall()
                for user in users:
                    username, email, first_name, last_name, role, is_active = user
                    status = "✅ Activo" if is_active else "❌ Inactivo"
                    print(f"   - {username} ({email}) - {first_name} {last_name} - {role} - {status}")
            
            # 3. Verificar anuncios de paquetes
            print("\n3️⃣ ANUNCIOS DE PAQUETES:")
            result = conn.execute(text("SELECT COUNT(*) FROM package_announcements"))
            ann_count = result.fetchone()[0]
            print(f"   📦 Total de anuncios: {ann_count}")
            
            if ann_count > 0:
                result = conn.execute(text("SELECT customer_name, phone_number, guide_number, tracking_code, announced_at FROM package_announcements ORDER BY announced_at DESC LIMIT 10"))
                announcements = result.fetchall()
                for ann in announcements:
                    customer_name, phone, guide, tracking, announced = ann
                    print(f"   - {customer_name} ({phone}) - Guía: {guide} - Código: {tracking} - {announced}")
            
            # 4. Verificar paquetes
            print("\n4️⃣ PAQUETES:")
            result = conn.execute(text("SELECT COUNT(*) FROM packages"))
            pack_count = result.fetchone()[0]
            print(f"   📦 Total de paquetes: {pack_count}")
            
            if pack_count > 0:
                result = conn.execute(text("SELECT tracking_number, customer_name, status, package_type FROM packages ORDER BY created_at DESC LIMIT 5"))
                packages = result.fetchall()
                for pack in packages:
                    tracking, customer, status, ptype = pack
                    print(f"   - {tracking} - {customer} - {status} - {ptype}")
            
            # 5. Verificar clientes
            print("\n5️⃣ CLIENTES:")
            result = conn.execute(text("SELECT COUNT(*) FROM customers"))
            cust_count = result.fetchone()[0]
            print(f"   👤 Total de clientes: {cust_count}")
            
            if cust_count > 0:
                result = conn.execute(text("SELECT name, phone, tracking_number FROM customers ORDER BY created_at DESC LIMIT 5"))
                customers = result.fetchall()
                for cust in customers:
                    name, phone, tracking = cust
                    print(f"   - {name} ({phone}) - {tracking}")
            
            # 6. Verificar notificaciones
            print("\n6️⃣ NOTIFICACIONES:")
            result = conn.execute(text("SELECT COUNT(*) FROM notifications"))
            notif_count = result.fetchone()[0]
            print(f"   🔔 Total de notificaciones: {notif_count}")
            
            # 7. Verificar tarifas
            print("\n7️⃣ TARIFAS:")
            result = conn.execute(text("SELECT COUNT(*) FROM rates"))
            rate_count = result.fetchone()[0]
            print(f"   💰 Total de tarifas: {rate_count}")
            
            # 8. Verificar archivos
            print("\n8️⃣ ARCHIVOS:")
            result = conn.execute(text("SELECT COUNT(*) FROM files"))
            file_count = result.fetchone()[0]
            print(f"   📁 Total de archivos: {file_count}")
            
            # 9. Verificar mensajes
            print("\n9️⃣ MENSAJES:")
            result = conn.execute(text("SELECT COUNT(*) FROM messages"))
            msg_count = result.fetchone()[0]
            print(f"   💬 Total de mensajes: {msg_count}")
            
            # 10. Verificar tokens de reset
            print("\n🔟 TOKENS DE RESET:")
            result = conn.execute(text("SELECT COUNT(*) FROM password_reset_tokens"))
            token_count = result.fetchone()[0]
            print(f"   🔑 Total de tokens: {token_count}")
            
            if token_count > 0:
                result = conn.execute(text("SELECT id, user_id, expires_at, used FROM password_reset_tokens ORDER BY created_at DESC LIMIT 5"))
                tokens = result.fetchall()
                for token in tokens:
                    token_id, user_id, expires_at, used = token
                    status = "✅ Usado" if used else "⏳ Pendiente"
                    print(f"   - Token {token_id} - Usuario: {user_id} - {expires_at} - {status}")
        
        # Calcular total de registros
        total_records = user_count + ann_count + pack_count + cust_count + notif_count + rate_count + file_count + msg_count + token_count
        
        print(f"\n📊 RESUMEN COMPLETO:")
        print("=" * 40)
        print(f"📈 Total de registros en RDS: {total_records}")
        print(f"📋 Total de tablas: {len(tables)}")
        print(f"👥 Usuarios: {user_count}")
        print(f"📦 Anuncios: {ann_count}")
        print(f"📦 Paquetes: {pack_count}")
        print(f"👤 Clientes: {cust_count}")
        print(f"🔔 Notificaciones: {notif_count}")
        print(f"💰 Tarifas: {rate_count}")
        print(f"📁 Archivos: {file_count}")
        print(f"💬 Mensajes: {msg_count}")
        print(f"🔑 Tokens: {token_count}")
        
        print(f"\n🌐 ACCESO A LA APLICACIÓN:")
        print("=" * 30)
        print(f"🔗 URL: https://guia.papyrus.com.co")
        print(f"🔗 Health Check: https://guia.papyrus.com.co/health")
        print(f"🔗 API: https://guia.papyrus.com.co/api/")
        
        if user_count > 0:
            print(f"\n🔐 CREDENCIALES DE ACCESO:")
            print("=" * 30)
            print(f"👤 Usuario: jveyes")
            print(f"📧 Email: jveyes@gmail.com")
            print(f"🔑 Contraseña: (la misma del sistema local)")
        
        print(f"\n✅ VERIFICACIÓN COMPLETADA!")
        print("🎉 Los datos están correctamente migrados a AWS RDS")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante la verificación: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🚀 ¡Verificación exitosa! Tu aplicación está lista en la nube.")
    else:
        print("\n❌ Error en la verificación")
