#!/bin/bash

# ========================================
# PAQUETES EL CLUB v3.1 - Iniciar con RDS
# ========================================
# Script para iniciar los contenedores usando la base de datos RDS de AWS

echo "🚀 Iniciando aplicación con base de datos RDS..."
echo "================================================"

# Verificar que estemos en el directorio correcto
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Error: No se encontró docker-compose.yml"
    echo "   Ejecuta este script desde el directorio code/"
    exit 1
fi

# Verificar que Docker esté corriendo
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker no está corriendo"
    echo "   Inicia Docker y vuelve a intentar"
    exit 1
fi

echo ""
echo "📋 Configuración actual:"
echo "   Base de datos: RDS AWS"
echo "   Host: ls-abe25e9bea57818f0ee32555c0e7b4a10e361535.ctobuhtlkwoj.us-east-1.rds.amazonaws.com"
echo "   Usuario: jveyes"
echo "   Puerto: 5432"

echo ""
echo "🔍 Verificando conexión a RDS..."

# Probar conexión a RDS
if python3 scripts/test-rds-connection.py > /dev/null 2>&1; then
    echo "✅ Conexión a RDS exitosa"
else
    echo "❌ Error conectando a RDS"
    echo "   Verifica la configuración de red y credenciales"
    exit 1
fi

echo ""
echo "🛑 Deteniendo contenedores existentes..."
docker-compose down

echo ""
echo "🧹 Limpiando contenedores y volúmenes..."
docker-compose down -v
docker system prune -f

echo ""
echo "🔨 Reconstruyendo imágenes..."
docker-compose build --no-cache

echo ""
echo "🚀 Iniciando contenedores..."
docker-compose up -d

echo ""
echo "⏳ Esperando que los servicios estén listos..."
sleep 10

echo ""
echo "🔍 Verificando estado de los contenedores..."
docker-compose ps

echo ""
echo "📊 Logs de la aplicación:"
docker-compose logs app --tail=20

echo ""
echo "✅ Aplicación iniciada con RDS"
echo ""
echo "🌐 URLs de acceso:"
echo "   - Aplicación: http://localhost:8001"
echo "   - Nginx: http://localhost"
echo ""
echo "🔧 Comandos útiles:"
echo "   - Ver logs: docker-compose logs -f"
echo "   - Detener: docker-compose down"
echo "   - Reiniciar: docker-compose restart"
echo ""
echo "🧪 Para probar:"
echo "   - Login y email: python3 scripts/test-login-email.py"
echo "   - Conexión RDS: python3 scripts/test-rds-connection.py"
