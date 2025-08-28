#!/bin/bash

# ========================================
# PAQUETES EL CLUB v3.1 - Verificador de Volúmenes
# ========================================
# Fecha: 25 de Agosto, 2025
# Versión: 3.1.0
# Descripción: Verifica que los volúmenes estén montados correctamente

echo "🔍 Verificando volúmenes de desarrollo..."

# Verificar que los contenedores estén ejecutándose
echo "📦 Estado de los contenedores:"
docker-compose ps

echo ""
echo "📁 Verificando volúmenes montados en el contenedor app:"

# Verificar volúmenes específicos
volumes_to_check=(
    "/app/src"
    "/app/templates"
    "/app/static"
    "/app/uploads"
    "/app/logs"
    "/app/database"
    "/app/SCRIPTS"
    "/app/TEST"
    "/app/docs"
    "/app/monitoring"
)

for volume in "${volumes_to_check[@]}"; do
    echo "🔍 Verificando $volume..."
    if docker exec paqueteria_v31_app test -d "$volume"; then
        echo "✅ $volume está montado correctamente"
        echo "   📄 Archivos en $volume:"
        docker exec paqueteria_v31_app ls -la "$volume" | head -5
    else
        echo "❌ $volume NO está montado"
    fi
    echo ""
done

echo "🌐 Verificando acceso a archivos estáticos:"
echo "   📄 Archivos en /app/static/images:"
docker exec paqueteria_v31_app ls -la /app/static/images/ 2>/dev/null || echo "   ❌ No se puede acceder a /app/static/images"

echo ""
echo "📋 Verificando templates:"
echo "   📄 Archivos en /app/templates/components:"
docker exec paqueteria_v31_app ls -la /app/templates/components/ 2>/dev/null || echo "   ❌ No se puede acceder a /app/templates/components"

echo ""
echo "🔧 Verificando configuración de nginx:"
echo "   📄 Archivos estáticos en nginx:"
docker exec paqueteria_v31_nginx ls -la /var/www/static/ 2>/dev/null || echo "   ❌ No se puede acceder a /var/www/static"

echo ""
echo "✅ Verificación completada!"
