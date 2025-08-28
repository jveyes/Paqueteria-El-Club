#!/bin/bash
# ========================================
# PAQUETES EL CLUB v3.1 - Limpieza de Contenedores
# ========================================
#
# 🎯 OBJETIVO: Limpiar todos los contenedores Docker relacionados con PAQUETES EL CLUB v3.1
# 📅 FECHA: 2025-08-25
# 👤 AUTOR: Equipo de Desarrollo PAQUETES EL CLUB
# 🔄 VERSIÓN: 3.1.0
#
# 📋 USO:
#   ./cleanup-containers.sh
#
# 📊 RESULTADOS:
#   - Contenedores detenidos y eliminados
#   - Volúmenes no utilizados limpiados
#   - Redes no utilizadas limpiadas
#
# ⚠️ DEPENDENCIAS:
#   - Docker
#   - Docker Compose
#
# ========================================

echo "🧹 Limpiando contenedores de PAQUETES EL CLUB v3.1..."

# Detener y eliminar contenedores específicos
echo "📦 Deteniendo contenedores..."
docker stop paqueteria_v31_postgres paqueteria_v31_redis paqueteria_v31_app paqueteria_v31_celery_worker paqueteria_v31_nginx 2>/dev/null || true

echo "🗑️ Eliminando contenedores..."
docker rm paqueteria_v31_postgres paqueteria_v31_redis paqueteria_v31_app paqueteria_v31_celery_worker paqueteria_v31_nginx 2>/dev/null || true

# Eliminar contenedores que contengan "paqueteria" en el nombre
echo "🔍 Buscando contenedores relacionados..."
docker ps -a --filter "name=paqueteria" --format "table {{.Names}}\t{{.Status}}" | grep -v "NAMES" | while read line; do
    if [ ! -z "$line" ]; then
        container_name=$(echo $line | awk '{print $1}')
        echo "🗑️ Eliminando contenedor: $container_name"
        docker stop $container_name 2>/dev/null || true
        docker rm $container_name 2>/dev/null || true
    fi
done

# Limpiar volúmenes no utilizados
echo "🧹 Limpiando volúmenes no utilizados..."
docker volume prune -f

# Limpiar redes no utilizadas
echo "🌐 Limpiando redes no utilizadas..."
docker network prune -f

echo "✅ Limpieza completada!"
echo "📝 Contenedores eliminados:"
echo "   - paqueteria_v31_postgres"
echo "   - paqueteria_v31_redis"
echo "   - paqueteria_v31_app"
echo "   - paqueteria_v31_celery_worker"
echo "   - paqueteria_v31_nginx"
