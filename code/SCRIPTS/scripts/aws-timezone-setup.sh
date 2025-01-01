#!/bin/bash

# ========================================
# PAQUETES EL CLUB v3.1 - Configuración de Zona Horaria en AWS
# ========================================
# Script para configurar la zona horaria de Colombia en el servidor AWS

echo "🕐 Configurando zona horaria de Colombia en AWS..."
echo "=================================================="

# Configurar zona horaria en el servidor host
echo "🌍 Configurando zona horaria del servidor..."
ssh papyrus "sudo timedatectl set-timezone America/Bogota"

# Verificar configuración del servidor
echo "✅ Verificando configuración del servidor:"
ssh papyrus "date && timedatectl"

# Aplicar zona horaria a contenedores existentes
echo ""
echo "📦 Aplicando zona horaria a contenedores en AWS..."

# Lista de contenedores en AWS
containers=(
    "paqueteria_v31_nginx"
    "paqueteria_v31_redis"
    "paqueteria_v31_app"
    "paqueteria_v31_celery_worker"
)

# Aplicar a cada contenedor
for container in "${containers[@]}"; do
    echo "📦 Configurando: $container"
    ssh papyrus "docker exec $container ln -sf /usr/share/zoneinfo/America/Bogota /etc/localtime 2>/dev/null || true"
    ssh papyrus "docker exec $container echo 'America/Bogota' > /etc/timezone 2>/dev/null || true"
    ssh papyrus "docker exec $container export TZ=America/Bogota 2>/dev/null || true"
done

echo ""
echo "=================================================="
echo "✅ Configuración de zona horaria completada en AWS"
echo ""
echo "📋 Para aplicar permanentemente:"
echo "1. Conectar a AWS: ssh papyrus"
echo "2. Ir al directorio: cd /opt/paqueteria"
echo "3. Detener contenedores: docker-compose -f docker-compose.aws.yml down"
echo "4. Reconstruir: docker-compose -f docker-compose.aws.yml build"
echo "5. Iniciar: docker-compose -f docker-compose.aws.yml up -d"
echo ""
echo "🔍 Para verificar: ssh papyrus 'docker exec paqueteria_v31_app date'"
