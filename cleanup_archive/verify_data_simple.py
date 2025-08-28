#!/usr/bin/env python3
"""
Script simple para verificar datos en la base de datos
"""

import os
import sys
sys.path.append('/app')

def main():
    try:
        print("🔍 Verificando datos en la base de datos...")
        
        # Importar después de agregar el path
        from sqlalchemy import create_engine, text
        
        # URL de la base de datos
        database_url = "postgresql://jveyes:a?HC!2.*1#?[==:|289qAI=)#V4kDzl$@ls-abe25e9bea57818f0ee32555c0e7b4a10e361535.ctobuhtlkwoj.us-east-1.rds.amazonaws.com:5432/paqueteria"
        
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            # Verificar usuarios
            print("\n👥 USUARIOS EN LA BASE DE DATOS:")
            print("=" * 50)
            
            result = conn.execute(text("SELECT id, username, email, first_name, last_name, role, is_active FROM users"))
            users = result.fetchall()
            
            if users:
                for user in users:
                    id_user, username, email, first_name, last_name, role, is_active = user
                    status = "✅ Activo" if is_active else "❌ Inactivo"
                    print(f"ID: {id_user}")
                    print(f"Usuario: {username}")
                    print(f"Email: {email}")
                    print(f"Nombre: {first_name} {last_name}")
                    print(f"Rol: {role}")
                    print(f"Estado: {status}")
                    print("-" * 30)
            else:
                print("❌ No se encontraron usuarios")
            
            # Verificar anuncios de paquetes
            print("\n📦 ANUNCIOS DE PAQUETES:")
            print("=" * 50)
            
            result = conn.execute(text("SELECT id, customer_name, phone_number, guide_number, tracking_code, announced_at FROM package_announcements ORDER BY announced_at DESC LIMIT 5"))
            announcements = result.fetchall()
            
            if announcements:
                for ann in announcements:
                    id_ann, customer_name, phone, guide, tracking, announced = ann
                    print(f"ID: {id_ann}")
                    print(f"Cliente: {customer_name}")
                    print(f"Teléfono: {phone}")
                    print(f"Guía: {guide}")
                    print(f"Código: {tracking}")
                    print(f"Anunciado: {announced}")
                    print("-" * 30)
            else:
                print("❌ No se encontraron anuncios")
            
            # Contar registros
            print("\n📊 ESTADÍSTICAS:")
            print("=" * 30)
            
            result = conn.execute(text("SELECT COUNT(*) FROM users"))
            user_count = result.fetchone()[0]
            print(f"Usuarios: {user_count}")
            
            result = conn.execute(text("SELECT COUNT(*) FROM package_announcements"))
            ann_count = result.fetchone()[0]
            print(f"Anuncios: {ann_count}")
            
            result = conn.execute(text("SELECT COUNT(*) FROM packages"))
            pack_count = result.fetchone()[0]
            print(f"Paquetes: {pack_count}")
            
            result = conn.execute(text("SELECT COUNT(*) FROM customers"))
            cust_count = result.fetchone()[0]
            print(f"Clientes: {cust_count}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ Verificación completada")
    else:
        print("\n❌ Error en la verificación")
