#!/bin/bash

# ========================================
# PAQUETES EL CLUB v3.1 - Diagnóstico de Caché
# ========================================

echo "🔍 DIAGNÓSTICO DE CACHÉ - PAQUETES EL CLUB v3.1"
echo "================================================"
echo ""

# 1. VERIFICAR ESTADO DE CONTENEDORES
echo "📦 1. ESTADO DE CONTENEDORES"
echo "----------------------------"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.CreatedAt}}"
echo ""

# 2. VERIFICAR CACHÉ DE DOCKER
echo "🐳 2. CACHÉ DE DOCKER"
echo "---------------------"
echo "📊 Imágenes Docker:"
docker images | grep paqueteria
echo ""
echo "📊 Volúmenes Docker:"
docker volume ls | grep paqueteria
echo ""

# 3. VERIFICAR CACHÉ DE NGINX
echo "🌐 3. CACHÉ DE NGINX"
echo "-------------------"
echo "📊 Headers de respuesta de Nginx:"
curl -I http://localhost 2>/dev/null | grep -E "(Cache-Control|ETag|Last-Modified|Expires)"
echo ""
echo "📊 Logs recientes de Nginx:"
docker logs paqueteria_v31_nginx --tail=5 2>/dev/null
echo ""

# 4. VERIFICAR CACHÉ DE FASTAPI
echo "⚡ 4. CACHÉ DE FASTAPI"
echo "---------------------"
echo "📊 Headers de respuesta de FastAPI:"
curl -I http://localhost:8001 2>/dev/null | grep -E "(Cache-Control|ETag|Last-Modified|Expires)"
echo ""
echo "📊 Logs recientes de FastAPI:"
docker logs paqueteria_v31_app --tail=5 2>/dev/null
echo ""

# 5. VERIFICAR CACHÉ DE TEMPLATES
echo "📄 5. CACHÉ DE TEMPLATES"
echo "-----------------------"
echo "📊 Contenido actual de la página principal:"
echo "Título de la página:"
curl -s http://localhost | grep -o '<title>[^<]*</title>'
echo ""
echo "📊 Verificar si el template se está cargando correctamente:"
docker exec paqueteria_v31_app ls -la /app/templates/ 2>/dev/null || echo "❌ No se puede acceder al contenedor"
echo ""

# 6. VERIFICAR CACHÉ DE ARCHIVOS ESTÁTICOS
echo "📁 6. CACHÉ DE ARCHIVOS ESTÁTICOS"
echo "--------------------------------"
echo "📊 Headers de archivos estáticos:"
curl -I http://localhost/static/ 2>/dev/null | grep -E "(Cache-Control|ETag|Last-Modified|Expires)"
echo ""

# 7. VERIFICAR CACHÉ DE BASE DE DATOS
echo "🗄️  7. CACHÉ DE BASE DE DATOS"
echo "----------------------------"
echo "📊 Estado de PostgreSQL:"
docker exec paqueteria_v31_postgres psql -U postgres -c "SELECT version();" 2>/dev/null || echo "❌ No se puede conectar a PostgreSQL"
echo ""

# 8. VERIFICAR CACHÉ DE REDIS
echo "🔴 8. CACHÉ DE REDIS"
echo "-------------------"
echo "📊 Estado de Redis:"
docker exec paqueteria_v31_redis redis-cli ping 2>/dev/null || echo "❌ No se puede conectar a Redis"
echo ""
echo "📊 Información de memoria de Redis:"
docker exec paqueteria_v31_redis redis-cli info memory 2>/dev/null | head -10 || echo "❌ No se puede obtener info de Redis"
echo ""

# 9. VERIFICAR CACHÉ DEL NAVEGADOR
echo "🌍 9. CACHÉ DEL NAVEGADOR"
echo "------------------------"
echo "📊 Headers de caché para el navegador:"
curl -I http://localhost 2>/dev/null | grep -E "(Cache-Control|Pragma|Expires)"
echo ""

# 10. VERIFICAR TIMESTAMPS DE ARCHIVOS
echo "⏰ 10. TIMESTAMPS DE ARCHIVOS"
echo "---------------------------"
echo "📊 Archivos principales modificados recientemente:"
find . -name "*.py" -o -name "*.html" -o -name "*.conf" | head -10 | xargs ls -la 2>/dev/null
echo ""

# 11. VERIFICAR CONFIGURACIÓN DE CACHÉ
echo "⚙️  11. CONFIGURACIÓN DE CACHÉ"
echo "----------------------------"
echo "📊 Configuración de caché en Nginx:"
grep -n "cache\|expires\|Cache-Control" code/nginx/conf.d/default.conf 2>/dev/null || echo "❌ No se encontró configuración de caché"
echo ""

# 12. RECOMENDACIONES
echo "💡 12. RECOMENDACIONES"
echo "---------------------"
echo "🔧 Para limpiar caché de Docker:"
echo "   docker-compose down --volumes"
echo "   docker system prune -f"
echo "   docker-compose up -d --build"
echo ""
echo "🔧 Para limpiar caché del navegador:"
echo "   Ctrl+Shift+R (Hard Refresh)"
echo "   Ctrl+F5 (Forzar recarga)"
echo "   Limpiar caché del navegador"
echo ""
echo "🔧 Para verificar cambios en tiempo real:"
echo "   docker-compose logs -f app"
echo "   docker-compose logs -f nginx"
echo ""

echo "✅ Diagnóstico completado"
echo "📝 Revisa las recomendaciones arriba para resolver problemas de caché"
