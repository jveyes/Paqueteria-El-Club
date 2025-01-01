#!/bin/bash

# ========================================
# PAQUETES EL CLUB v3.1 - Verificador de Zona Horaria
# ========================================
# Script para verificar que todos los contenedores tengan la zona horaria de Colombia

echo "🔍 Verificando zona horaria en todos los contenedores..."
echo "=================================================="

# Lista de contenedores a verificar
containers=(
    "paqueteria_v31_postgres"
    "paqueteria_v31_redis"
    "paqueteria_v31_app"
    "paqueteria_v31_celery_worker"
    "paqueteria_v31_nginx"
)

# Verificar cada contenedor
for container in "${containers[@]}"; do
    echo ""
    echo "📦 Contenedor: $container"
    echo "----------------------------------------"
    
    # Verificar si el contenedor está ejecutándose
    if docker ps --format "table {{.Names}}" | grep -q "$container"; then
        echo "✅ Contenedor ejecutándose"
        
        # Verificar zona horaria
        echo "🕐 Zona horaria:"
        docker exec "$container" date
        echo "🌍 Variable TZ:"
        docker exec "$container" printenv TZ 2>/dev/null || echo "❌ Variable TZ no encontrada"
        echo "📅 Archivo timezone:"
        docker exec "$container" cat /etc/timezone 2>/dev/null || echo "❌ Archivo timezone no encontrado"
        
    else
        echo "❌ Contenedor no está ejecutándose"
    fi
done

echo ""
echo "=================================================="
echo "✅ Verificación completada"
echo ""
echo "📋 Resumen:"
echo "- Todos los contenedores deben mostrar hora de Colombia (UTC-5)"
echo "- La variable TZ debe ser 'America/Bogota'"
echo "- El archivo /etc/timezone debe contener 'America/Bogota'"
