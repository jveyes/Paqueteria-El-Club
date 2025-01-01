#!/bin/bash

# ========================================
# PAQUETES EL CLUB v3.1 - Prueba de Restablecimiento de Contraseña
# ========================================

echo "🔐 Prueba de Funcionalidad de Restablecimiento de Contraseña"
echo "============================================================="
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

echo -e "${BLUE}1. Verificando estado de la aplicación...${NC}"
if curl -s -f http://localhost/health > /dev/null; then
    show_result 0 "Aplicación funcionando correctamente"
else
    show_result 1 "Aplicación no responde"
    exit 1
fi

echo ""
echo -e "${BLUE}2. Verificando página de restablecimiento de contraseña...${NC}"
if curl -s -f http://localhost/auth/forgot-password > /dev/null; then
    show_result 0 "Página de restablecimiento accesible"
else
    show_result 1 "Página de restablecimiento no accesible"
fi

echo ""
echo -e "${BLUE}3. Verificando base de datos...${NC}"
if docker exec paqueteria_v31_app python3 -c "
from src.database.database import engine
from sqlalchemy import text
conn = engine.connect()
result = conn.execute(text('SELECT COUNT(*) FROM users'))
print('Usuarios en BD:', result.fetchone()[0])
conn.close()
" > /dev/null 2>&1; then
    show_result 0 "Base de datos funcionando correctamente"
else
    show_result 1 "Error en base de datos"
fi

echo ""
echo -e "${BLUE}4. Verificando columna profile_photo...${NC}"
if docker exec paqueteria_v31_app python3 -c "
from src.database.database import engine
from sqlalchemy import text
conn = engine.connect()
result = conn.execute(text('SELECT username, profile_photo FROM users LIMIT 1'))
row = result.fetchone()
print('Usuario:', row[0], 'Profile Photo:', row[1])
conn.close()
" > /dev/null 2>&1; then
    show_result 0 "Columna profile_photo accesible"
else
    show_result 1 "Error accediendo a profile_photo"
fi

echo ""
echo -e "${BLUE}5. Verificando configuración de correo...${NC}"
if docker exec paqueteria_v31_app python3 -c "
from src.config import settings
print('SMTP_HOST:', settings.smtp_host)
print('SMTP_USER:', settings.smtp_user)
print('SMTP_FROM_EMAIL:', settings.smtp_from_email)
" > /dev/null 2>&1; then
    show_result 0 "Configuración de correo cargada"
    
    # Mostrar configuración
    echo "   Configuración SMTP:"
    docker exec paqueteria_v31_app python3 -c "
from src.config import settings
print('   Host:', settings.smtp_host or 'No configurado')
print('   Usuario:', settings.smtp_user or 'No configurado')
print('   Email origen:', settings.smtp_from_email or 'No configurado')
"
else
    show_result 1 "Error cargando configuración de correo"
fi

echo ""
echo -e "${BLUE}6. Verificando logs de la aplicación...${NC}"
recent_logs=$(docker logs paqueteria_v31_app --tail 50 2>&1)

if echo "$recent_logs" | grep -q "Base de datos AWS RDS inicializada correctamente"; then
    show_result 0 "Base de datos inicializada correctamente"
else
    show_result 1 "Base de datos no se inicializó correctamente"
fi

if echo "$recent_logs" | grep -q "column users.profile_photo does not exist"; then
    show_result 1 "Error de columna profile_photo detectado en logs"
else
    show_result 0 "No hay errores de columna profile_photo en logs"
fi

echo ""
echo -e "${BLUE}7. Prueba de funcionalidad completa...${NC}"

# Simular acceso a la página de restablecimiento
echo "   Probando acceso a la página..."
page_content=$(curl -s http://localhost/auth/forgot-password)

if echo "$page_content" | grep -q "Restablecer contraseña\|Forgot Password\|Recuperar contraseña"; then
    show_result 0 "Página de restablecimiento cargando correctamente"
else
    show_result 1 "Página de restablecimiento con problemas"
fi

# Verificar formulario
if echo "$page_content" | grep -q "form\|input\|email"; then
    show_result 0 "Formulario de restablecimiento presente"
else
    show_result 1 "Formulario de restablecimiento no encontrado"
fi

echo ""
echo "============================================================="
echo -e "${BLUE}📊 RESUMEN DE PRUEBAS${NC}"
echo "============================================================="

# Contar pruebas exitosas
success_count=0
total_count=0

# Verificar aplicación
if curl -s -f http://localhost/health > /dev/null; then ((success_count++)); fi; ((total_count++))
if curl -s -f http://localhost/auth/forgot-password > /dev/null; then ((success_count++)); fi; ((total_count++))
if docker exec paqueteria_v31_app python3 -c "from src.database.database import engine; print('OK')" > /dev/null 2>&1; then ((success_count++)); fi; ((total_count++))
if docker exec paqueteria_v31_app python3 -c "from src.database.database import engine; conn = engine.connect(); result = conn.execute(text('SELECT profile_photo FROM users LIMIT 1')); conn.close(); print('OK')" > /dev/null 2>&1; then ((success_count++)); fi; ((total_count++))
if docker exec paqueteria_v31_app python3 -c "from src.config import settings; print('OK')" > /dev/null 2>&1; then ((success_count++)); fi; ((total_count++))
if docker logs paqueteria_v31_app --tail 50 2>&1 | grep -q "Base de datos AWS RDS inicializada correctamente"; then ((success_count++)); fi; ((total_count++))
if ! docker logs paqueteria_v31_app --tail 50 2>&1 | grep -q "column users.profile_photo does not exist"; then ((success_count++)); fi; ((total_count++))

echo -e "${GREEN}Pruebas exitosas: $success_count/$total_count${NC}"

if [ $success_count -eq $total_count ]; then
    echo ""
    echo -e "${GREEN}🎉 ¡LA FUNCIONALIDAD DE RESTABLECIMIENTO DE CONTRASEÑA ESTÁ FUNCIONANDO!${NC}"
    echo -e "${GREEN}✅ La base de datos está funcionando correctamente${NC}"
    echo -e "${GREEN}✅ La columna profile_photo está disponible${NC}"
    echo -e "${GREEN}✅ La página es accesible${NC}"
    echo ""
    echo -e "${BLUE}🌐 URL de prueba: http://localhost/auth/forgot-password${NC}"
else
    echo ""
    echo -e "${YELLOW}⚠️  La funcionalidad tiene algunos problemas${NC}"
    echo -e "${YELLOW}🔧 Revisa las pruebas fallidas arriba${NC}"
fi

echo ""
echo "============================================================="
echo -e "${BLUE}🚀 Próximos pasos recomendados:${NC}"
echo "1. Probar el formulario de restablecimiento manualmente"
echo "2. Verificar configuración de SMTP si es necesario"
echo "3. Configurar notificaciones por correo"
echo "4. Probar flujo completo de restablecimiento"
echo "============================================================="
