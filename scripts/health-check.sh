#!/bin/bash

# Script de health check para PAQUETERIA EL CLUB v3.1
# Verifica el estado de todos los servicios

set -e

echo "🏥 Verificando estado de los servicios..."

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para verificar estado
check_service() {
    local service_name=$1
    local container_name=$2
    
    if docker ps --format "table {{.Names}}" | grep -q "$container_name"; then
        echo -e "${GREEN}✅ $service_name: RUNNING${NC}"
        return 0
    else
        echo -e "${RED}❌ $service_name: STOPPED${NC}"
        return 1
    fi
}

# Función para verificar puerto
check_port() {
    local port=$1
    local service_name=$2
    
    if netstat -tuln 2>/dev/null | grep -q ":$port "; then
        echo -e "${GREEN}✅ $service_name (puerto $port): ACCESIBLE${NC}"
        return 0
    else
        echo -e "${RED}❌ $service_name (puerto $port): NO ACCESIBLE${NC}"
        return 1
    fi
}

# Verificar contenedores
echo ""
echo "🐳 Estado de contenedores:"
check_service "PostgreSQL" "paqueteria_v31_postgres"
check_service "Redis" "paqueteria_v31_redis"
check_service "App" "paqueteria_v31_app"
check_service "Celery Worker" "paqueteria_v31_celery_worker"
check_service "Nginx" "paqueteria_v31_nginx"

# Verificar puertos
echo ""
echo "🌐 Estado de puertos:"
check_port "5432" "PostgreSQL"
check_port "6380" "Redis"
check_port "8001" "App"
check_port "80" "Nginx"

# Verificar API
echo ""
echo "🔌 Verificando API:"
if curl -s http://localhost:8001/health > /dev/null; then
    echo -e "${GREEN}✅ API: RESPONDIENDO${NC}"
else
    echo -e "${RED}❌ API: NO RESPONDE${NC}"
fi

# Verificar base de datos
echo ""
echo "🗄️ Verificando base de datos:"
if docker exec paqueteria_v31_postgres pg_isready -U paqueteria_user > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Base de datos: CONECTADA${NC}"
else
    echo -e "${RED}❌ Base de datos: NO CONECTADA${NC}"
fi

# Verificar logs
echo ""
echo "📋 Últimos errores en logs:"
if [ -f "logs/app/app.log" ]; then
    echo -e "${YELLOW}App logs (últimas 5 líneas):${NC}"
    tail -n 5 logs/app/app.log 2>/dev/null || echo "No hay logs disponibles"
else
    echo -e "${YELLOW}No se encontraron logs de la aplicación${NC}"
fi

echo ""
echo "🎯 Health check completado!"
