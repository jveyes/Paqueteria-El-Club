#!/bin/bash

# ========================================
# Script de Despliegue Rápido de Nginx
# PAQUETES EL CLUB v3.1
# ========================================

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para imprimir mensajes
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar que estamos en el directorio correcto
if [ ! -d "/home/ubuntu/Paquetes" ]; then
    print_error "Directorio /home/ubuntu/Paquetes no existe. Ejecutar primero los pasos manuales."
    exit 1
fi

cd /home/ubuntu/Paquetes

print_status "Iniciando despliegue de Nginx..."

# Verificar Docker
if ! command -v docker &> /dev/null; then
    print_error "Docker no está instalado"
    exit 1
fi

if ! command -v docker compose &> /dev/null; then
    print_error "Docker Compose no está instalado"
    exit 1
fi

print_status "Docker y Docker Compose verificados"

# Detener contenedor existente si existe
if docker ps -q -f name=paqueteria_v31_nginx | grep -q .; then
    print_status "Deteniendo contenedor existente..."
    docker compose -f docker-compose-nginx.yml down
fi

# Verificar que los archivos necesarios existan
required_files=(
    "nginx/nginx.conf"
    "nginx/conf.d/paqueteria.conf"
    "ssl/cert.pem"
    "ssl/key.pem"
    "docker-compose-nginx.yml"
)

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        print_error "Archivo requerido no encontrado: $file"
        exit 1
    fi
done

print_status "Todos los archivos requeridos verificados"

# Crear directorios si no existen
mkdir -p static uploads logs

# Desplegar el contenedor
print_status "Desplegando contenedor de Nginx..."
docker compose -f docker-compose-nginx.yml up -d

# Esperar un momento para que el contenedor inicie
sleep 5

# Verificar que el contenedor esté corriendo
if docker ps -q -f name=paqueteria_v31_nginx | grep -q .; then
    print_status "Contenedor de Nginx desplegado exitosamente"
else
    print_error "El contenedor no se inició correctamente"
    docker logs paqueteria_v31_nginx
    exit 1
fi

# Verificar configuración de nginx
print_status "Verificando configuración de Nginx..."
if docker exec paqueteria_v31_nginx nginx -t; then
    print_status "Configuración de Nginx válida"
else
    print_error "Error en la configuración de Nginx"
    exit 1
fi

# Verificar que los puertos estén abiertos
print_status "Verificando puertos..."
if netstat -tlnp | grep -q ":80 "; then
    print_status "Puerto 80 abierto"
else
    print_warning "Puerto 80 no está abierto"
fi

if netstat -tlnp | grep -q ":443 "; then
    print_status "Puerto 443 abierto"
else
    print_warning "Puerto 443 no está abierto"
fi

# Verificar respuesta HTTP
print_status "Verificando respuesta HTTP..."
if curl -s -o /dev/null -w "%{http_code}" http://localhost | grep -q "301\|200"; then
    print_status "Nginx responde correctamente en HTTP"
else
    print_warning "Nginx no responde en HTTP"
fi

# Verificar respuesta HTTPS
print_status "Verificando respuesta HTTPS..."
if curl -s -o /dev/null -w "%{http_code}" -k https://localhost | grep -q "301\|200"; then
    print_status "Nginx responde correctamente en HTTPS"
else
    print_warning "Nginx no responde en HTTPS"
fi

# Mostrar información del contenedor
print_status "Información del contenedor:"
docker ps -f name=paqueteria_v31_nginx

print_status "Logs del contenedor:"
docker logs paqueteria_v31_nginx

print_status "Despliegue completado exitosamente!"
print_status "Nginx está corriendo en:"
echo "  - HTTP:  http://18.214.124.14"
echo "  - HTTPS: https://18.214.124.14"
echo "  - DNS:   https://guia.papyrus.com.co"

print_warning "Recuerda:"
echo "  - Los certificados SSL son temporales"
echo "  - Configurar certificados reales para producción"
echo "  - Verificar configuración de firewall"
echo "  - Monitorear logs regularmente"
