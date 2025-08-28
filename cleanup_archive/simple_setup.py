#!/usr/bin/env python3
"""
Script simple para configurar la base de datos paso a paso
"""

import os
import sys
sys.path.append('/app')

def main():
    try:
        print("🔧 Configurando base de datos paso a paso...")
        
        # Importar después de agregar el path
        from sqlalchemy import create_engine, text
        from src.database.database import Base
        
        # URL de la base de datos
        database_url = "postgresql://jveyes:a?HC!2.*1#?[==:|289qAI=)#V4kDzl$@ls-abe25e9bea57818f0ee32555c0e7b4a10e361535.ctobuhtlkwoj.us-east-1.rds.amazonaws.com:5432/paqueteria"
        
        engine = create_engine(database_url)
        
        print("1️⃣ Creando tablas...")
        Base.metadata.create_all(engine)
        print("✅ Tablas creadas")
        
        print("2️⃣ Verificando tablas...")
        with engine.connect() as conn:
            result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name"))
            tables = result.fetchall()
            print(f"✅ Se encontraron {len(tables)} tablas:")
            for table in tables:
                print(f"   - {table[0]}")
        
        print("3️⃣ Creando usuario de prueba...")
        with engine.connect() as conn:
            # Crear un usuario de prueba
            test_user_sql = """
            INSERT INTO users (id, username, email, password_hash, first_name, last_name, is_active, role)
            VALUES (
                '26af2c6f-c2d7-4b73-a8fc-2444cc9a0370',
                'jveyes',
                'jveyes@gmail.com',
                '$2b$12$3rsPzcNY6VgmEsIvs9nx0efwHdyamcL/ABqOALsjaZyhkeu8KVvsq',
                'Jesus',
                'Villalobos',
                true,
                'USER'
            ) ON CONFLICT (id) DO NOTHING;
            """
            
            try:
                conn.execute(text(test_user_sql))
                conn.commit()
                print("✅ Usuario de prueba creado")
            except Exception as e:
                print(f"⚠️  Usuario ya existe o error: {e}")
        
        print("4️⃣ Verificando datos...")
        with engine.connect() as conn:
            # Verificar usuarios
            result = conn.execute(text("SELECT COUNT(*) FROM users"))
            user_count = result.fetchone()[0]
            print(f"👥 Usuarios: {user_count}")
            
            if user_count > 0:
                print("\n👤 Usuarios disponibles:")
                result = conn.execute(text("SELECT username, email, first_name, last_name, role FROM users"))
                users = result.fetchall()
                for user in users:
                    username, email, first_name, last_name, role = user
                    print(f"   - {username} ({email}) - {first_name} {last_name} - {role}")
        
        print("\n✅ Configuración completada")
        print("🌐 Puedes acceder a: https://guia.papyrus.com.co")
        print("🔐 Usuario de prueba: jveyes / jveyes@gmail.com")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 ¡Configuración exitosa!")
    else:
        print("\n❌ Error en la configuración")
