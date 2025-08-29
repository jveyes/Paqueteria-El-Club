#!/bin/bash

# ========================================
# PAQUETES EL CLUB v3.1 - Aplicador de Zona Horaria
# ========================================
# Script para aplicar la zona horaria de Colombia a contenedores existentes

echo "🕐 Aplicando zona horaria de Colombia a contenedores..."
echo "======================================================"

# Función para aplicar zona horaria a un contenedor
apply_timezone() {
    local container=$1
    echo "📦 Aplicando zona horaria a: $container"
    
    # Verificar si el contenedor está ejecutándose
    if docker ps --format "table {{.Names}}" | grep -q "$container"; then
        # Aplicar zona horaria temporalmente
        docker exec "$container" ln -sf /usr/share/zoneinfo/America/Bogota /etc/localtime 2>/dev/null || true
        docker exec "$container" echo "America/Bogota" > /etc/timezone 2>/dev/null || true
        docker exec "$container" export TZ=America/Bogota 2>/dev/null || true
        
        echo "✅ Zona horaria aplicada a $container"
    else
        echo "⚠️  Contenedor $container no está ejecutándose"
    fi
}

# Lista de contenedores
containers=(
    "paqueteria_v31_postgres"
    "paqueteria_v31_redis"
    "paqueteria_v31_app"
    "paqueteria_v31_celery_worker"
    "paqueteria_v31_nginx"
)

# Aplicar a cada contenedor
for container in "${containers[@]}"; do
    apply_timezone "$container"
done

echo ""
echo "======================================================"
echo "✅ Configuración de zona horaria aplicada"
echo ""
echo "📋 Para aplicar permanentemente:"
echo "1. Detener los contenedores: docker-compose down"
echo "2. Reconstruir las imágenes: docker-compose build"
echo "3. Iniciar los contenedores: docker-compose up -d"
echo ""
echo "🔍 Para verificar: ./scripts/check-timezone.sh"
