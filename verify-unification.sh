#!/bin/bash

# ========================================
# PAQUETES EL CLUB v3.1 - Verificación de Unificación de Base de Datos
# ========================================

echo "🗄️ Verificación de Unificación de Base de Datos"
echo "=================================================="
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

echo -e "${BLUE}1. Verificando configuración de la aplicación...${NC}"
cd code
if python3 -c "from src.config import settings; print('DATABASE_URL:', settings.database_url[:50] + '...')" > /dev/null 2>&1; then
    show_result 0 "Configuración de la aplicación cargada correctamente"
    python3 -c "from src.config import settings; print('   URL: ' + settings.database_url[:50] + '...')"
else
    show_result 1 "Error al cargar configuración de la aplicación"
fi

echo ""
echo -e "${BLUE}2. Verificando conexión a AWS RDS...${NC}"
if python3 scripts/test-rds-connection.py > /dev/null 2>&1; then
    show_result 0 "Conexión a AWS RDS exitosa"
else
    show_result 1 "Error de conexión a AWS RDS"
fi

echo ""
echo -e "${BLUE}3. Verificando que no hay contenedores PostgreSQL locales...${NC}"
if docker ps | grep postgres > /dev/null 2>&1; then
    show_result 1 "Hay contenedores PostgreSQL ejecutándose localmente"
    docker ps | grep postgres
else
    show_result 0 "No hay contenedores PostgreSQL locales ejecutándose"
fi

echo ""
echo -e "${BLUE}4. Verificando importación de modelos...${NC}"
if python3 -c "from src.models import User, Package, Customer; print('Modelos importados')" > /dev/null 2>&1; then
    show_result 0 "Modelos importados correctamente"
else
    show_result 1 "Error al importar modelos"
fi

echo ""
echo -e "${BLUE}5. Verificando inicialización de base de datos...${NC}"
if python3 -c "from src.database.database import init_db; init_db(); print('BD inicializada')" > /dev/null 2>&1; then
    show_result 0 "Base de datos inicializada correctamente"
else
    show_result 1 "Error al inicializar base de datos"
fi

echo ""
echo -e "${BLUE}6. Verificando configuración de Docker Compose...${NC}"
cd ..
if docker-compose -f docker-compose-aws-fixed.yml config > /dev/null 2>&1; then
    show_result 0 "Docker Compose configurado correctamente"
else
    show_result 1 "Error en configuración de Docker Compose"
fi

echo ""
echo -e "${BLUE}7. Verificando archivos de configuración...${NC}"

# Verificar que env.aws existe y tiene la configuración correcta
if grep -q "ls-abe25e9bea57818f0ee32555c0e7b4a10e361535.ctobuhtlkwoj.us-east-1.rds.amazonaws.com" code/env.aws; then
    show_result 0 "Archivo env.aws configurado correctamente"
else
    show_result 1 "Archivo env.aws no configurado correctamente"
fi

# Verificar que no hay referencias a bases de datos locales
if grep -r "paqueteria_user:Paqueteria2025!Secure@postgres:5432" code/ --include="*.yml" --include="*.py" > /dev/null 2>&1; then
    show_result 1 "Se encontraron referencias a bases de datos locales"
else
    show_result 0 "No hay referencias a bases de datos locales"
fi

echo ""
echo -e "${BLUE}8. Verificando estructura de la base de datos...${NC}"
cd code
if python3 -c "
from src.database.database import engine
from sqlalchemy import text
conn = engine.connect()
result = conn.execute(text('SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = \\'public\\''))
print('Tablas en la base de datos:', result.fetchone()[0])
conn.close()
" > /dev/null 2>&1; then
    show_result 0 "Estructura de base de datos verificada"
else
    show_result 1 "Error al verificar estructura de base de datos"
fi

echo ""
echo "=================================================="
echo -e "${BLUE}📊 RESUMEN DE VERIFICACIÓN${NC}"
echo "=================================================="

# Contar verificaciones exitosas
success_count=0
total_count=8

# Verificaciones individuales
echo -e "${BLUE}1. Configuración de la aplicación${NC}"
if python3 -c "from src.config import settings; print('OK')" > /dev/null 2>&1; then
    echo -e "${GREEN}   ✅ EXITOSA${NC}"
    ((success_count++))
else
    echo -e "${RED}   ❌ FALLIDA${NC}"
fi

echo -e "${BLUE}2. Conexión a AWS RDS${NC}"
if python3 scripts/test-rds-connection.py > /dev/null 2>&1; then
    echo -e "${GREEN}   ✅ EXITOSA${NC}"
    ((success_count++))
else
    echo -e "${RED}   ❌ FALLIDA${NC}"
fi

echo -e "${BLUE}3. Sin contenedores PostgreSQL locales${NC}"
if ! docker ps | grep postgres > /dev/null 2>&1; then
    echo -e "${GREEN}   ✅ EXITOSA${NC}"
    ((success_count++))
else
    echo -e "${RED}   ❌ FALLIDA${NC}"
fi

echo -e "${BLUE}4. Importación de modelos${NC}"
if python3 -c "from src.models import User, Package, Customer; print('OK')" > /dev/null 2>&1; then
    echo -e "${GREEN}   ✅ EXITOSA${NC}"
    ((success_count++))
else
    echo -e "${RED}   ❌ FALLIDA${NC}"
fi

echo -e "${BLUE}5. Inicialización de base de datos${NC}"
if python3 -c "from src.database.database import init_db; init_db(); print('OK')" > /dev/null 2>&1; then
    echo -e "${GREEN}   ✅ EXITOSA${NC}"
    ((success_count++))
else
    echo -e "${RED}   ❌ FALLIDA${NC}"
fi

echo -e "${BLUE}6. Configuración de Docker Compose${NC}"
cd ..
if docker-compose -f docker-compose-aws-fixed.yml config > /dev/null 2>&1; then
    echo -e "${GREEN}   ✅ EXITOSA${NC}"
    ((success_count++))
else
    echo -e "${RED}   ❌ FALLIDA${NC}"
fi

echo -e "${BLUE}7. Archivos de configuración${NC}"
if grep -q "ls-abe25e9bea57818f0ee32555c0e7b4a10e361535.ctobuhtlkwoj.us-east-1.rds.amazonaws.com" code/env.aws; then
    echo -e "${GREEN}   ✅ EXITOSA${NC}"
    ((success_count++))
else
    echo -e "${RED}   ❌ FALLIDA${NC}"
fi

echo -e "${BLUE}8. Estructura de base de datos${NC}"
cd code
if python3 -c "
from src.database.database import engine
from sqlalchemy import text
conn = engine.connect()
result = conn.execute(text('SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = \\'public\\''))
print('OK')
conn.close()
" > /dev/null 2>&1; then
    echo -e "${GREEN}   ✅ EXITOSA${NC}"
    ((success_count++))
else
    echo -e "${RED}   ❌ FALLIDA${NC}"
fi

echo ""
echo "=================================================="
echo -e "${BLUE}📈 RESULTADO FINAL${NC}"
echo "=================================================="
echo -e "${GREEN}Verificaciones exitosas: $success_count/$total_count${NC}"

if [ $success_count -eq $total_count ]; then
    echo ""
    echo -e "${GREEN}🎉 ¡UNIFICACIÓN COMPLETADA EXITOSAMENTE!${NC}"
    echo -e "${GREEN}✅ La aplicación está configurada para usar únicamente AWS RDS${NC}"
    echo -e "${GREEN}✅ No hay contenedores PostgreSQL locales ejecutándose${NC}"
    echo -e "${GREEN}✅ Todas las configuraciones están unificadas${NC}"
else
    echo ""
    echo -e "${YELLOW}⚠️  La unificación tiene algunos problemas${NC}"
    echo -e "${YELLOW}🔧 Revisa las verificaciones fallidas arriba${NC}"
fi

echo ""
echo "=================================================="
echo -e "${BLUE}🚀 Próximos pasos recomendados:${NC}"
echo "1. Probar la aplicación en Docker"
echo "2. Verificar funcionalidad completa"
echo "3. Configurar monitoreo de AWS RDS"
echo "4. Implementar respaldos automáticos"
echo "=================================================="
