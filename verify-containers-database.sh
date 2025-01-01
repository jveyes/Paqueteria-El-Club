#!/bin/bash

# ========================================
# PAQUETES EL CLUB v3.1 - Verificación de Configuración de Base de Datos en Contenedores
# ========================================

echo "🐳 Verificación de Configuración de Base de Datos en Contenedores"
echo "=================================================================="
echo ""

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para mostrar resultados
show_result() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2${NC}"
    else
        echo -e "${RED}❌ $2${NC}"
    fi
}

# Función para verificar contenedor específico
check_container_database_config() {
    local container_name=$1
    local container_desc=$2
    
    echo -e "${BLUE}Verificando $container_desc ($container_name)...${NC}"
    
    # Verificar si el contenedor está ejecutándose
    if docker ps | grep -q "$container_name"; then
        show_result 0 "Contenedor ejecutándose"
        
        # Verificar variables de entorno de base de datos
        if docker exec "$container_name" env | grep -q "DATABASE_URL"; then
            local db_url=$(docker exec "$container_name" env | grep "DATABASE_URL" | cut -d'=' -f2-)
            if echo "$db_url" | grep -q "ls-abe25e9bea57818f0ee32555c0e7b4a10e361535.ctobuhtlkwoj.us-east-1.rds.amazonaws.com"; then
                show_result 0 "DATABASE_URL configurada correctamente (AWS RDS)"
            else
                show_result 1 "DATABASE_URL incorrecta o no es AWS RDS"
                echo "   URL actual: $db_url"
            fi
        else
            show_result 1 "No se encontró DATABASE_URL en variables de entorno"
        fi
        
        # Verificar archivos de configuración si es la aplicación
        if [[ "$container_name" == *"app"* ]]; then
            echo "   Verificando archivos de configuración..."
            
            # Verificar config.py
            if docker exec "$container_name" grep -q "ls-abe25e9bea57818f0ee32555c0e7b4a10e361535.ctobuhtlkwoj.us-east-1.rds.amazonaws.com" /app/src/config.py; then
                show_result 0 "config.py configurado correctamente"
            else
                show_result 1 "config.py no configurado correctamente"
            fi
            
            # Verificar .env
            if docker exec "$container_name" grep -q "ls-abe25e9bea57818f0ee32555c0e7b4a10e361535.ctobuhtlkwoj.us-east-1.rds.amazonaws.com" /app/.env; then
                show_result 0 ".env configurado correctamente"
            else
                show_result 1 ".env no configurado correctamente"
            fi
            
            # Verificar env.aws
            if docker exec "$container_name" grep -q "ls-abe25e9bea57818f0ee32555c0e7b4a10e361535.ctobuhtlkwoj.us-east-1.rds.amazonaws.com" /app/env.aws; then
                show_result 0 "env.aws configurado correctamente"
            else
                show_result 1 "env.aws no configurado correctamente"
            fi
            
            # Verificar env.development
            if docker exec "$container_name" grep -q "ls-abe25e9bea57818f0ee32555c0e7b4a10e361535.ctobuhtlkwoj.us-east-1.rds.amazonaws.com" /app/env.development; then
                show_result 0 "env.development configurado correctamente"
            else
                show_result 1 "env.development no configurado correctamente"
            fi
            
            # Verificar alembic.ini
            if docker exec "$container_name" grep -q "ls-abe25e9bea57818f0ee32555c0e7b4a10e361535.ctobuhtlkwoj.us-east-1.rds.amazonaws.com" /app/alembic.ini; then
                show_result 0 "alembic.ini configurado correctamente"
            else
                show_result 1 "alembic.ini no configurado correctamente"
            fi
            
            # Verificar database.py
            if docker exec "$container_name" grep -q "Base de datos AWS RDS inicializada correctamente" /app/src/database/database.py; then
                show_result 0 "database.py configurado correctamente"
            else
                show_result 1 "database.py no configurado correctamente"
            fi
        fi
        
        # Verificar que no hay URLs de conexión a bases de datos locales
        local_urls=$(docker exec "$container_name" grep -r "postgres://" /app/src/ --include="*.py" 2>/dev/null | grep -v "ls-abe25e9bea57818f0ee32555c0e7b4a10e361535.ctobuhtlkwoj.us-east-1.rds.amazonaws.com" | wc -l)
        if [ "$local_urls" -gt 0 ]; then
            show_result 1 "Se encontraron $local_urls URLs de conexión a bases de datos locales"
        else
            show_result 0 "No hay URLs de conexión a bases de datos locales"
        fi
        
    else
        show_result 1 "Contenedor no está ejecutándose"
    fi
    
    echo ""
}

echo -e "${BLUE}1. Verificando contenedores activos...${NC}"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep "paqueteria_v31_"
echo ""

echo -e "${BLUE}2. Verificando configuración de base de datos en cada contenedor...${NC}"

# Verificar contenedor de aplicación
check_container_database_config "paqueteria_v31_app" "Aplicación Principal"

# Verificar contenedor de Celery
check_container_database_config "paqueteria_v31_celery_worker" "Worker de Celery"

# Verificar contenedor de Redis (no debería tener configuración de BD)
echo -e "${BLUE}Verificando Redis (paqueteria_v31_redis)...${NC}"
if docker ps | grep -q "paqueteria_v31_redis"; then
    show_result 0 "Contenedor ejecutándose"
    if docker exec paqueteria_v31_redis env | grep -q "DATABASE_URL"; then
        show_result 1 "Redis no debería tener DATABASE_URL"
    else
        show_result 0 "Redis correctamente configurado (sin DATABASE_URL)"
    fi
else
    show_result 1 "Contenedor no está ejecutándose"
fi
echo ""

# Verificar contenedor de Nginx (no debería tener configuración de BD)
echo -e "${BLUE}Verificando Nginx (paqueteria_v31_nginx)...${NC}"
if docker ps | grep -q "paqueteria_v31_nginx"; then
    show_result 0 "Contenedor ejecutándose"
    if docker exec paqueteria_v31_nginx env | grep -q "DATABASE_URL"; then
        show_result 1 "Nginx no debería tener DATABASE_URL"
    else
        show_result 0 "Nginx correctamente configurado (sin DATABASE_URL)"
    fi
else
    show_result 1 "Contenedor no está ejecutándose"
fi
echo ""

echo -e "${BLUE}3. Verificando contenedores antiguos que podrían interferir...${NC}"
old_containers=$(docker ps -a --format "{{.Names}}" | grep -E "(paqueteria|postgres)" | grep -v "paqueteria_v31_")

if [ -n "$old_containers" ]; then
    echo "Contenedores antiguos encontrados:"
    for container in $old_containers; do
        status=$(docker inspect "$container" --format='{{.State.Status}}' 2>/dev/null)
        echo "   - $container (Estado: $status)"
        
        # Si está ejecutándose, verificar configuración
        if [ "$status" = "running" ]; then
            echo "     ⚠️  Contenedor ejecutándose - verificando configuración..."
            if docker exec "$container" env 2>/dev/null | grep -q "DATABASE_URL"; then
                db_url=$(docker exec "$container" env 2>/dev/null | grep "DATABASE_URL" | cut -d'=' -f2-)
                if echo "$db_url" | grep -q "postgres:"; then
                    show_result 1 "     Contenedor antiguo usando base de datos local"
                    echo "        URL: $db_url"
                fi
            fi
        fi
    done
else
    show_result 0 "No hay contenedores antiguos ejecutándose"
fi

echo ""
echo -e "${BLUE}4. Verificando conectividad a AWS RDS desde contenedores...${NC}"

# Verificar desde la aplicación
if docker exec paqueteria_v31_app python3 -c "
from src.database.database import engine
from sqlalchemy import text
conn = engine.connect()
result = conn.execute(text('SELECT COUNT(*) FROM users'))
print('Usuarios:', result.fetchone()[0])
conn.close()
" > /dev/null 2>&1; then
    show_result 0 "Aplicación puede conectarse a AWS RDS"
else
    show_result 1 "Aplicación no puede conectarse a AWS RDS"
fi

# Verificar desde Celery
if docker exec paqueteria_v31_celery_worker python3 -c "
from src.database.database import engine
from sqlalchemy import text
conn = engine.connect()
result = conn.execute(text('SELECT COUNT(*) FROM users'))
print('Usuarios:', result.fetchone()[0])
conn.close()
" > /dev/null 2>&1; then
    show_result 0 "Celery puede conectarse a AWS RDS"
else
    show_result 1 "Celery no puede conectarse a AWS RDS"
fi

echo ""
echo "=================================================="
echo -e "${BLUE}📊 RESUMEN DE VERIFICACIÓN${NC}"
echo "=================================================="

# Contar verificaciones exitosas
success_count=0
total_count=0

# Verificar contenedores principales
if docker ps | grep -q "paqueteria_v31_app"; then ((success_count++)); fi; ((total_count++))
if docker ps | grep -q "paqueteria_v31_celery_worker"; then ((success_count++)); fi; ((total_count++))
if docker ps | grep -q "paqueteria_v31_redis"; then ((success_count++)); fi; ((total_count++))
if docker ps | grep -q "paqueteria_v31_nginx"; then ((success_count++)); fi; ((total_count++))

echo -e "${GREEN}Contenedores ejecutándose: $success_count/$total_count${NC}"

if [ $success_count -eq $total_count ]; then
    echo ""
    echo -e "${GREEN}🎉 ¡TODOS LOS CONTENEDORES ESTÁN CONFIGURADOS CORRECTAMENTE!${NC}"
    echo -e "${GREEN}✅ Todos los contenedores usan AWS RDS${NC}"
    echo -e "${GREEN}✅ No hay referencias a bases de datos locales${NC}"
    echo -e "${GREEN}✅ La configuración está unificada${NC}"
else
    echo ""
    echo -e "${YELLOW}⚠️  Algunos contenedores tienen problemas${NC}"
    echo -e "${YELLOW}🔧 Revisa las verificaciones fallidas arriba${NC}"
fi

echo ""
echo "=================================================="
echo -e "${BLUE}🚀 Próximos pasos recomendados:${NC}"
echo "1. Probar funcionalidad completa de la aplicación"
echo "2. Verificar que no hay errores en los logs"
echo "3. Configurar monitoreo de AWS RDS"
echo "4. Implementar respaldos automáticos"
echo "=================================================="
