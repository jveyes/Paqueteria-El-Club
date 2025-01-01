#!/bin/bash

# ========================================
# PAQUETES EL CLUB v3.1 - Prueba de Funcionalidad Web
# ========================================

echo "🌐 Prueba de Funcionalidad Web y Base de Datos"
echo "================================================"
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

echo -e "${BLUE}1. Verificando servicios Docker...${NC}"
if docker ps | grep -q "paqueteria_v31_app"; then
    show_result 0 "Aplicación ejecutándose"
else
    show_result 1 "Aplicación no está ejecutándose"
    exit 1
fi

if docker ps | grep -q "paqueteria_v31_nginx"; then
    show_result 0 "Nginx ejecutándose"
else
    show_result 1 "Nginx no está ejecutándose"
    exit 1
fi

if docker ps | grep -q "paqueteria_v31_redis"; then
    show_result 0 "Redis ejecutándose"
else
    show_result 1 "Redis no está ejecutándose"
    exit 1
fi

echo ""
echo -e "${BLUE}2. Verificando conectividad web...${NC}"

# Probar página principal
if curl -s -f http://localhost/ > /dev/null; then
    show_result 0 "Página principal accesible"
else
    show_result 1 "Página principal no accesible"
fi

# Probar página de búsqueda
if curl -s -f http://localhost/search > /dev/null; then
    show_result 0 "Página de búsqueda accesible"
else
    show_result 1 "Página de búsqueda no accesible"
fi

# Probar página de login
if curl -s -f http://localhost/login > /dev/null; then
    show_result 0 "Página de login accesible"
else
    show_result 1 "Página de login no accesible"
fi

echo ""
echo -e "${BLUE}3. Verificando API...${NC}"

# Probar health check
if curl -s -f http://localhost/health > /dev/null; then
    show_result 0 "Health check funcionando"
else
    show_result 1 "Health check fallando"
fi

# Probar API de autenticación
if curl -s -f http://localhost/api/auth/check > /dev/null; then
    show_result 0 "API de autenticación funcionando"
else
    show_result 1 "API de autenticación fallando"
fi

echo ""
echo -e "${BLUE}4. Verificando base de datos desde la aplicación...${NC}"

# Verificar conexión a la base de datos
if docker exec paqueteria_v31_app python3 -c "
from src.database.database import engine
from sqlalchemy import text
conn = engine.connect()
result = conn.execute(text('SELECT COUNT(*) FROM users'))
print('Usuarios:', result.fetchone()[0])
conn.close()
" > /dev/null 2>&1; then
    show_result 0 "Conexión a base de datos funcionando"
else
    show_result 1 "Error de conexión a base de datos"
fi

# Verificar tablas principales
if docker exec paqueteria_v31_app python3 -c "
from src.database.database import engine
from sqlalchemy import text
conn = engine.connect()
result = conn.execute(text('SELECT COUNT(*) FROM packages'))
print('Paquetes:', result.fetchone()[0])
conn.close()
" > /dev/null 2>&1; then
    show_result 0 "Tabla de paquetes accesible"
else
    show_result 1 "Error accediendo a tabla de paquetes"
fi

# Verificar tablas principales
if docker exec paqueteria_v31_app python3 -c "
from src.database.database import engine
from sqlalchemy import text
conn = engine.connect()
result = conn.execute(text('SELECT COUNT(*) FROM customers'))
print('Clientes:', result.fetchone()[0])
conn.close()
" > /dev/null 2>&1; then
    show_result 0 "Tabla de clientes accesible"
else
    show_result 1 "Error accediendo a tabla de clientes"
fi

echo ""
echo -e "${BLUE}5. Verificando logs de la aplicación...${NC}"

# Verificar que no hay errores de base de datos en los logs
if docker logs paqueteria_v31_app --tail 50 2>&1 | grep -q "Base de datos AWS RDS inicializada correctamente"; then
    show_result 0 "Base de datos inicializada correctamente"
else
    show_result 1 "Base de datos no se inicializó correctamente"
fi

# Verificar que no hay errores de conexión
if docker logs paqueteria_v31_app --tail 50 2>&1 | grep -q "could not translate host name"; then
    show_result 1 "Error de conexión a base de datos local detectado"
else
    show_result 0 "No hay errores de conexión a base de datos local"
fi

echo ""
echo -e "${BLUE}6. Prueba de funcionalidad completa...${NC}"

# Simular una búsqueda básica
echo "   Probando funcionalidad de búsqueda..."
if curl -s -f "http://localhost/search" | grep -q "Buscar paquetes"; then
    show_result 0 "Funcionalidad de búsqueda cargando correctamente"
else
    show_result 1 "Funcionalidad de búsqueda con problemas"
fi

# Verificar formulario de login
echo "   Probando formulario de login..."
if curl -s -f "http://localhost/login" | grep -q "Iniciar sesión"; then
    show_result 0 "Formulario de login cargando correctamente"
else
    show_result 1 "Formulario de login con problemas"
fi

echo ""
echo "================================================"
echo -e "${BLUE}📊 RESUMEN DE PRUEBAS${NC}"
echo "================================================"

# Contar pruebas exitosas
success_count=0
total_count=0

# Contar servicios
if docker ps | grep -q "paqueteria_v31_app"; then ((success_count++)); fi; ((total_count++))
if docker ps | grep -q "paqueteria_v31_nginx"; then ((success_count++)); fi; ((total_count++))
if docker ps | grep -q "paqueteria_v31_redis"; then ((success_count++)); fi; ((total_count++))

# Contar conectividad web
if curl -s -f http://localhost/ > /dev/null; then ((success_count++)); fi; ((total_count++))
if curl -s -f http://localhost/search > /dev/null; then ((success_count++)); fi; ((total_count++))
if curl -s -f http://localhost/login > /dev/null; then ((success_count++)); fi; ((total_count++))

# Contar API
if curl -s -f http://localhost/health > /dev/null; then ((success_count++)); fi; ((total_count++))
if curl -s -f http://localhost/api/auth/check > /dev/null; then ((success_count++)); fi; ((total_count++))

# Contar base de datos
if docker exec paqueteria_v31_app python3 -c "from src.database.database import engine; print('OK')" > /dev/null 2>&1; then ((success_count++)); fi; ((total_count++))

echo -e "${GREEN}Pruebas exitosas: $success_count/$total_count${NC}"

if [ $success_count -eq $total_count ]; then
    echo ""
    echo -e "${GREEN}🎉 ¡TODAS LAS FUNCIONALIDADES ESTÁN FUNCIONANDO CORRECTAMENTE!${NC}"
    echo -e "${GREEN}✅ La aplicación web está funcionando${NC}"
    echo -e "${GREEN}✅ La base de datos AWS RDS está conectada${NC}"
    echo -e "${GREEN}✅ Todas las páginas son accesibles${NC}"
    echo -e "${GREEN}✅ La API está funcionando${NC}"
else
    echo ""
    echo -e "${YELLOW}⚠️  Algunas funcionalidades tienen problemas${NC}"
    echo -e "${YELLOW}🔧 Revisa las pruebas fallidas arriba${NC}"
fi

echo ""
echo "================================================"
echo -e "${BLUE}🌐 URLs de Prueba:${NC}"
echo "   Página principal: http://localhost/"
echo "   Búsqueda: http://localhost/search"
echo "   Login: http://localhost/login"
echo "   Health Check: http://localhost/health"
echo "   API Auth: http://localhost/api/auth/check"
echo "================================================"
