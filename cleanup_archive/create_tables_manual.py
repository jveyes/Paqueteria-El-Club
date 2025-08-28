#!/usr/bin/env python3
"""
Script para crear las tablas manualmente usando SQL directo
"""

import sys
from sqlalchemy import create_engine, text

def main():
    try:
        print("🔧 Creando tablas manualmente...")
        
        # URL de la base de datos
        database_url = "postgresql://jveyes:a?HC!2.*1#?[==:|289qAI=)#V4kDzl$@ls-abe25e9bea57818f0ee32555c0e7b4a10e361535.ctobuhtlkwoj.us-east-1.rds.amazonaws.com:5432/paqueteria"
        
        engine = create_engine(database_url)
        
        # SQL para crear las tablas principales
        create_tables_sql = """
        -- Crear tabla users
        CREATE TABLE IF NOT EXISTS users (
            id UUID PRIMARY KEY,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            username VARCHAR(50) NOT NULL UNIQUE,
            email VARCHAR(100) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            phone VARCHAR(20),
            is_active BOOLEAN DEFAULT true,
            role VARCHAR(20) DEFAULT 'USER',
            permissions JSON,
            last_login TIMESTAMP
        );

        -- Crear tabla customers
        CREATE TABLE IF NOT EXISTS customers (
            id UUID PRIMARY KEY,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            name VARCHAR(100) NOT NULL,
            phone VARCHAR(20) NOT NULL,
            tracking_number VARCHAR(50) NOT NULL UNIQUE
        );

        -- Crear tabla packages
        CREATE TABLE IF NOT EXISTS packages (
            id UUID PRIMARY KEY,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            tracking_number VARCHAR(50) NOT NULL UNIQUE,
            customer_name VARCHAR(100) NOT NULL,
            customer_phone VARCHAR(20) NOT NULL,
            status VARCHAR(20) DEFAULT 'pendiente',
            package_type VARCHAR(20) DEFAULT 'normal',
            package_condition VARCHAR(20),
            storage_cost NUMERIC(10,2),
            delivery_cost NUMERIC(10,2),
            total_cost NUMERIC(10,2),
            observations TEXT,
            announced_at TIMESTAMP,
            received_at TIMESTAMP,
            delivered_at TIMESTAMP,
            customer_id UUID REFERENCES customers(id)
        );

        -- Crear tabla package_announcements
        CREATE TABLE IF NOT EXISTS package_announcements (
            id UUID PRIMARY KEY,
            customer_name VARCHAR(100) NOT NULL,
            phone_number VARCHAR(20) NOT NULL,
            guide_number VARCHAR(50) NOT NULL UNIQUE,
            is_active BOOLEAN NOT NULL DEFAULT true,
            is_processed BOOLEAN NOT NULL DEFAULT false,
            announced_at TIMESTAMP NOT NULL,
            processed_at TIMESTAMP,
            customer_id UUID REFERENCES customers(id),
            package_id UUID REFERENCES packages(id),
            created_at TIMESTAMP NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
            tracking_code VARCHAR(4) NOT NULL UNIQUE
        );

        -- Crear tabla notifications
        CREATE TABLE IF NOT EXISTS notifications (
            id UUID PRIMARY KEY,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            package_id UUID REFERENCES packages(id),
            user_id UUID REFERENCES users(id),
            notification_type VARCHAR(20) NOT NULL,
            message TEXT NOT NULL,
            status VARCHAR(20) DEFAULT 'pending',
            sent_at TIMESTAMP,
            delivery_confirmation JSON
        );

        -- Crear tabla rates
        CREATE TABLE IF NOT EXISTS rates (
            id UUID PRIMARY KEY,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            rate_type VARCHAR(20) NOT NULL,
            base_price NUMERIC(10,2) NOT NULL,
            daily_storage_rate NUMERIC(10,2),
            delivery_rate NUMERIC(10,2),
            package_type_multiplier NUMERIC(10,2),
            is_active BOOLEAN DEFAULT true,
            valid_from TIMESTAMP,
            valid_to TIMESTAMP
        );

        -- Crear tabla files
        CREATE TABLE IF NOT EXISTS files (
            id UUID PRIMARY KEY,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            package_id UUID REFERENCES packages(id),
            uploaded_by_user_id UUID REFERENCES users(id),
            filename VARCHAR(255) NOT NULL,
            file_path VARCHAR(500) NOT NULL,
            file_size INTEGER NOT NULL,
            mime_type VARCHAR(100) NOT NULL,
            upload_date TIMESTAMP
        );

        -- Crear tabla messages
        CREATE TABLE IF NOT EXISTS messages (
            id UUID PRIMARY KEY,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            sender_id UUID NOT NULL REFERENCES users(id),
            subject VARCHAR(200) NOT NULL,
            content TEXT NOT NULL,
            message_type VARCHAR(20),
            is_read BOOLEAN DEFAULT false,
            read_at TIMESTAMP
        );

        -- Crear tabla password_reset_tokens
        CREATE TABLE IF NOT EXISTS password_reset_tokens (
            id SERIAL PRIMARY KEY,
            token VARCHAR(255) NOT NULL UNIQUE,
            user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            expires_at TIMESTAMP NOT NULL,
            used BOOLEAN NOT NULL DEFAULT false,
            created_at TIMESTAMP NOT NULL DEFAULT NOW()
        );

        -- Crear tabla alembic_version
        CREATE TABLE IF NOT EXISTS alembic_version (
            version_num VARCHAR(32) NOT NULL PRIMARY KEY
        );
        """
        
        print("📋 Ejecutando comandos SQL...")
        with engine.connect() as conn:
            # Dividir el SQL en comandos individuales
            commands = create_tables_sql.split(';')
            
            for command in commands:
                command = command.strip()
                if command:
                    try:
                        conn.execute(text(command))
                        print(f"✅ Ejecutado: {command[:50]}...")
                    except Exception as e:
                        if "already exists" not in str(e):
                            print(f"⚠️  Error: {e}")
            
            conn.commit()
        
        print("✅ Tablas creadas")
        
        # Crear usuario de prueba
        print("👤 Creando usuario de prueba...")
        create_user_sql = """
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
        
        with engine.connect() as conn:
            try:
                conn.execute(text(create_user_sql))
                conn.commit()
                print("✅ Usuario de prueba creado")
            except Exception as e:
                print(f"⚠️  Usuario ya existe: {e}")
        
        # Verificar
        print("🔍 Verificando tablas creadas...")
        with engine.connect() as conn:
            result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name"))
            tables = result.fetchall()
            print(f"✅ Se encontraron {len(tables)} tablas:")
            for table in tables:
                print(f"   - {table[0]}")
            
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
        print("🔐 Usuario: jveyes / jveyes@gmail.com")
        
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
