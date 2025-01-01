#!/usr/bin/env python3
"""
Script para optimizar archivos estáticos de PAQUETES EL CLUB v3.1
"""

import os
import shutil
import hashlib
from pathlib import Path
import mimetypes
import gzip
import json
from datetime import datetime

class StaticOptimizer:
    def __init__(self, static_dir="static", output_dir="static_optimized"):
        self.static_dir = Path(static_dir)
        self.output_dir = Path(output_dir)
        self.manifest_file = self.output_dir / "manifest.json"
        self.manifest = {}
        
    def setup_directories(self):
        """Crear directorios necesarios"""
        self.output_dir.mkdir(exist_ok=True)
        (self.output_dir / "css").mkdir(exist_ok=True)
        (self.output_dir / "js").mkdir(exist_ok=True)
        (self.output_dir / "images").mkdir(exist_ok=True)
        (self.output_dir / "fonts").mkdir(exist_ok=True)
        
    def get_file_hash(self, file_path):
        """Generar hash MD5 del archivo"""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()[:8]
    
    def should_compress(self, file_path):
        """Determinar si un archivo debe ser comprimido"""
        compressible_extensions = {'.css', '.js', '.html', '.xml', '.txt', '.json'}
        return file_path.suffix.lower() in compressible_extensions
    
    def compress_file(self, source_path, dest_path):
        """Comprimir archivo con gzip"""
        try:
            with open(source_path, 'rb') as f_in:
                with gzip.open(dest_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            return True
        except Exception as e:
            print(f"Error comprimiendo {source_path}: {e}")
            return False
    
    def optimize_image(self, source_path, dest_path):
        """Optimizar imagen (placeholder para futuras implementaciones)"""
        # Por ahora solo copiamos la imagen
        shutil.copy2(source_path, dest_path)
        return True
    
    def process_file(self, file_path, relative_path):
        """Procesar un archivo individual"""
        # Determinar el tipo de archivo
        if file_path.suffix.lower() in {'.css', '.js'}:
            category = file_path.suffix[1:]  # 'css' o 'js'
        elif file_path.suffix.lower() in {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico'}:
            category = 'images'
        elif file_path.suffix.lower() in {'.woff', '.woff2', '.ttf', '.eot'}:
            category = 'fonts'
        else:
            category = 'other'
        
        # Crear directorio de destino
        dest_dir = self.output_dir / category
        dest_dir.mkdir(exist_ok=True)
        
        # Generar nombre de archivo con hash
        file_hash = self.get_file_hash(file_path)
        name_without_ext = file_path.stem
        ext = file_path.suffix
        new_filename = f"{name_without_ext}.{file_hash}{ext}"
        dest_path = dest_dir / new_filename
        
        # Copiar archivo
        shutil.copy2(file_path, dest_path)
        
        # Comprimir si es necesario
        if self.should_compress(file_path):
            gzip_path = dest_path.with_suffix(dest_path.suffix + '.gz')
            self.compress_file(dest_path, gzip_path)
        
        # Actualizar manifest
        self.manifest[str(relative_path)] = {
            'path': str(dest_path.relative_to(self.output_dir)),
            'hash': file_hash,
            'size': dest_path.stat().st_size,
            'mime_type': mimetypes.guess_type(file_path)[0] or 'application/octet-stream',
            'compressed': self.should_compress(file_path)
        }
        
        print(f"✓ Procesado: {relative_path} -> {dest_path.name}")
    
    def optimize_static_files(self):
        """Optimizar todos los archivos estáticos"""
        print("🚀 Iniciando optimización de archivos estáticos...")
        
        if not self.static_dir.exists():
            print(f"❌ Directorio {self.static_dir} no encontrado")
            return False
        
        self.setup_directories()
        
        # Procesar archivos recursivamente
        for file_path in self.static_dir.rglob('*'):
            if file_path.is_file():
                relative_path = file_path.relative_to(self.static_dir)
                self.process_file(file_path, relative_path)
        
        # Guardar manifest
        with open(self.manifest_file, 'w') as f:
            json.dump(self.manifest, f, indent=2)
        
        print(f"✅ Optimización completada. Manifest guardado en: {self.manifest_file}")
        print(f"📊 Total de archivos procesados: {len(self.manifest)}")
        
        return True
    
    def generate_nginx_config(self):
        """Generar configuración Nginx para archivos estáticos optimizados"""
        config = """
# Configuración Nginx para archivos estáticos optimizados
location /static/ {
    alias /var/www/static/;
    expires 1y;
    add_header Cache-Control "public, immutable";
    add_header X-Content-Type-Options "nosniff";
    
    # Compresión gzip
    gzip on;
    gzip_vary on;
    gzip_min_length 1000;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/json
        application/javascript
        application/xml+rss
        application/atom+xml
        image/svg+xml;
    
    # Servir archivos comprimidos si existen
    location ~* \\.(css|js|html|xml|txt|json)\\.gz$ {
        gzip_static on;
        add_header Content-Encoding gzip;
    }
}

# Configuración específica para imágenes
location ~* \\.(png|jpg|jpeg|gif|ico|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
    add_header X-Content-Type-Options "nosniff";
}

# Configuración específica para fuentes
location ~* \\.(woff|woff2|ttf|eot)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
    add_header Access-Control-Allow-Origin "*";
}
"""
        
        config_path = self.output_dir / "nginx_static.conf"
        with open(config_path, 'w') as f:
            f.write(config)
        
        print(f"📝 Configuración Nginx generada en: {config_path}")
        return config_path

def main():
    """Función principal"""
    print("=" * 60)
    print("🔧 OPTIMIZADOR DE ARCHIVOS ESTÁTICOS - PAQUETES EL CLUB v3.1")
    print("=" * 60)
    
    optimizer = StaticOptimizer()
    
    if optimizer.optimize_static_files():
        optimizer.generate_nginx_config()
        print("\n🎉 Optimización completada exitosamente!")
    else:
        print("\n❌ Error en la optimización")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
