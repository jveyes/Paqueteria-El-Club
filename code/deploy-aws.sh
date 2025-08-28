#!/bin/bash

# ========================================
# Script de Deployment para AWS
# PAQUETES EL CLUB v3.1
# ========================================

set -e

echo "🚀 INICIANDO DEPLOYMENT EN AWS"
echo "=================================="

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir mensajes
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar si estamos en el directorio correcto
if [ ! -f "docker-compose.aws.yml" ]; then
    print_error "No se encontró docker-compose.aws.yml. Ejecuta este script desde el directorio code/"
    exit 1
fi

# Verificar si existe el archivo de variables de entorno
if [ ! -f "env.aws" ]; then
    print_error "No se encontró env.aws. Asegúrate de que el archivo existe."
    exit 1
fi

print_status "Verificando configuración..."

# Copiar archivo de variables de entorno
if [ -f "env.aws" ]; then
    cp env.aws .env
    print_success "Archivo de variables de entorno copiado"
else
    print_warning "Archivo env.aws no encontrado. Usando .env existente"
fi

# Verificar que Docker esté instalado
if ! command -v docker &> /dev/null; then
    print_error "Docker no está instalado. Instala Docker primero."
    exit 1
fi

# Verificar que Docker Compose esté instalado
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose no está instalado. Instala Docker Compose primero."
    exit 1
fi

print_success "Docker y Docker Compose verificados"

# Detener servicios existentes si están corriendo
print_status "Deteniendo servicios existentes..."
docker-compose -f docker-compose.aws.yml down --remove-orphans 2>/dev/null || true

# Limpiar imágenes y contenedores no utilizados
print_status "Limpiando recursos no utilizados..."
docker system prune -f

# Construir y levantar servicios
print_status "Construyendo y levantando servicios..."
docker-compose -f docker-compose.aws.yml up -d --build

# Esperar a que los servicios estén listos
print_status "Esperando a que los servicios estén listos..."
sleep 30

# Verificar estado de los servicios
print_status "Verificando estado de los servicios..."
docker-compose -f docker-compose.aws.yml ps

# Verificar logs de la aplicación
print_status "Verificando logs de la aplicación..."
docker-compose -f docker-compose.aws.yml logs app --tail=20

# Verificar health check
print_status "Verificando health check..."
sleep 10

# Verificar que la aplicación responda
if curl -f http://localhost/health > /dev/null 2>&1; then
    print_success "Health check exitoso"
else
    print_warning "Health check falló. Revisa los logs."
fi

# Mostrar información final
echo ""
echo "🎉 DEPLOYMENT COMPLETADO"
echo "========================"
echo ""
print_success "Servicios desplegados:"
echo "  - Nginx: http://localhost"
echo "  - API: http://localhost/docs"
echo "  - Health: http://localhost/health"
echo ""
print_success "Comandos útiles:"
echo "  - Ver logs: docker-compose -f docker-compose.aws.yml logs -f"
echo "  - Ver estado: docker-compose -f docker-compose.aws.yml ps"
echo "  - Detener: docker-compose -f docker-compose.aws.yml down"
echo "  - Reiniciar: docker-compose -f docker-compose.aws.yml restart"
echo ""

# Verificar puertos en uso
print_status "Puertos en uso:"
netstat -tlnp | grep -E ':(80|443|8000|6380)' || true

print_success "¡Deployment completado exitosamente!"
