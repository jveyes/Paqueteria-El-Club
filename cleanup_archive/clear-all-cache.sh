#!/bin/bash

# ========================================
# PAQUETES EL CLUB v3.1 - Limpieza Completa de Caché
# ========================================

echo "🧹 LIMPIEZA COMPLETA DE CACHÉ - PAQUETES EL CLUB v3.1"
echo "===================================================="
echo ""

# 1. PARAR SERVICIOS
echo "🛑 1. Parando servicios..."
docker-compose down
echo "✅ Servicios detenidos"
echo ""

# 2. LIMPIAR CACHÉ DE DOCKER
echo "🐳 2. Limpiando caché de Docker..."
docker system prune -f
docker volume prune -f
echo "✅ Caché de Docker limpiado"
echo ""

# 3. LIMPIAR IMÁGENES ANTIGUAS
echo "📦 3. Limpiando imágenes antiguas..."
docker images | grep paqueteria | awk '{print $3}' | xargs -r docker rmi -f
echo "✅ Imágenes antiguas eliminadas"
echo ""

# 4. LIMPIAR CACHÉ DE REDIS
echo "🔴 4. Limpiando caché de Redis..."
docker run --rm --network paqueteria_v31_default redis:7.0 redis-cli -h paqueteria_v31_redis FLUSHALL 2>/dev/null || echo "⚠️  Redis no disponible"
echo "✅ Caché de Redis limpiado"
echo ""

# 5. REINICIAR SERVICIOS
echo "🚀 5. Reiniciando servicios..."
docker-compose up -d --build
echo "✅ Servicios reiniciados"
echo ""

# 6. ESPERAR A QUE LOS SERVICIOS ESTÉN LISTOS
echo "⏳ 6. Esperando que los servicios estén listos..."
sleep 10

# 7. VERIFICAR ESTADO
echo "🔍 7. Verificando estado de servicios..."
docker ps --format "table {{.Names}}\t{{.Status}}"
echo ""

# 8. VERIFICAR HEADERS ANTI-CACHÉ
echo "🌐 8. Verificando headers anti-caché..."
curl -I http://localhost 2>/dev/null | grep -E "(Cache-Control|Pragma|Expires)"
echo ""

# 9. INSTRUCCIONES PARA EL NAVEGADOR
echo "💡 9. INSTRUCCIONES PARA EL NAVEGADOR:"
echo "   🔧 Limpia la caché del navegador:"
echo "      - Ctrl+Shift+R (Hard Refresh)"
echo "      - Ctrl+F5 (Forzar recarga)"
echo "      - O abre en modo incógnito"
echo ""

echo "✅ Limpieza completa finalizada"
echo "🌐 Accede a: http://localhost"
echo "📝 Si sigues viendo contenido antiguo, es caché del navegador"
