#!/usr/bin/env python3
"""
Script completo para configurar la base de datos y restaurar datos
"""

import os
import sys
sys.path.append('/app')

def main():
    try:
        print("🔧 Configurando base de datos completa...")
        
        # Importar después de agregar el path
        from sqlalchemy import create_engine, text
        from src.database.database import Base
        
        # URL de la base de datos
        database_url = "postgresql://jveyes:a?HC!2.*1#?[==:|289qAI=)#V4kDzl$@ls-abe25e9bea57818f0ee32555c0e7b4a10e361535.ctobuhtlkwoj.us-east-1.rds.amazonaws.com:5432/paqueteria"
        
        engine = create_engine(database_url)
        
        print("1️⃣ Creando tablas...")
        Base.metadata.create_all(engine)
        print("✅ Tablas creadas")
        
        print("2️⃣ Verificando tablas creadas...")
        with engine.connect() as conn:
            result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name"))
            tables = result.fetchall()
            print(f"✅ Se crearon {len(tables)} tablas:")
            for table in tables:
                print(f"   - {table[0]}")
        
        print("3️⃣ Restaurando datos del backup...")
        backup_file = "/home/ubuntu/Paquetes/migration_backup/paqueteria_local_20250828_083834.sql"
        
        if os.path.exists(backup_file):
            print(f"📖 Leyendo backup: {backup_file}")
            
            # Leer el backup y ejecutar solo las partes SQL válidas
            with open(backup_file, 'r') as f:
                content = f.read()
            
            # Dividir el contenido en comandos SQL
            sql_commands = []
            current_command = ""
            
            for line in content.split('\n'):
                line = line.strip()
                if line.startswith('--') or not line:  # Comentarios o líneas vacías
                    continue
                if line.startswith('\\'):  # Comandos de psql
                    continue
                if line.endswith(';'):
                    current_command += line
                    if current_command.strip():
                        sql_commands.append(current_command.strip())
                    current_command = ""
                else:
                    current_command += line + " "
            
            print(f"📊 Ejecutando {len(sql_commands)} comandos SQL...")
            
            with engine.connect() as conn:
                for i, command in enumerate(sql_commands):
                    try:
                        if command.strip():
                            conn.execute(text(command))
                            if i % 10 == 0:  # Mostrar progreso cada 10 comandos
                                print(f"   Progreso: {i+1}/{len(sql_commands)}")
                    except Exception as e:
                        # Ignorar errores de comandos que ya existen
                        if "already exists" not in str(e) and "does not exist" not in str(e):
                            print(f"⚠️  Error en comando {i+1}: {e}")
                
                conn.commit()
            
            print("✅ Datos restaurados")
        else:
            print("❌ No se encontró el archivo de backup")
            return False
        
        print("4️⃣ Verificando datos restaurados...")
        with engine.connect() as conn:
            # Verificar usuarios
            result = conn.execute(text("SELECT COUNT(*) FROM users"))
            user_count = result.fetchone()[0]
            print(f"👥 Usuarios: {user_count}")
            
            # Verificar anuncios
            result = conn.execute(text("SELECT COUNT(*) FROM package_announcements"))
            ann_count = result.fetchone()[0]
            print(f"📦 Anuncios: {ann_count}")
            
            # Verificar paquetes
            result = conn.execute(text("SELECT COUNT(*) FROM packages"))
            pack_count = result.fetchone()[0]
            print(f"📦 Paquetes: {pack_count}")
            
            # Mostrar usuarios específicos
            if user_count > 0:
                print("\n👤 Usuarios disponibles:")
                result = conn.execute(text("SELECT username, email, first_name, last_name, role FROM users"))
                users = result.fetchall()
                for user in users:
                    username, email, first_name, last_name, role = user
                    print(f"   - {username} ({email}) - {first_name} {last_name} - {role}")
        
        print("\n✅ Configuración de base de datos completada")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 ¡Base de datos configurada exitosamente!")
        print("🌐 Puedes acceder a: https://guia.papyrus.com.co")
    else:
        print("\n❌ Error en la configuración")
