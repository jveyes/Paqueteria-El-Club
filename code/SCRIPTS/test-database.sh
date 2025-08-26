#!/bin/bash

# ========================================
# PAQUETES EL CLUB v3.0 - Pruebas de Base de Datos
# ========================================

set -e

echo "🗄️ Probando base de datos de PAQUETES EL CLUB v3.0..."

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para logging
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Variables
RESULTS_DIR="TEST/results/database-queries"
LOGS_DIR="TEST/results/logs"

# Crear directorios si no existen
mkdir -p "$RESULTS_DIR"
mkdir -p "$LOGS_DIR"

# Inicializar contadores
total_tests=0
passed_tests=0
failed_tests=0

# Función para ejecutar test
run_test() {
    local test_name=$1
    local command=$2
    
    total_tests=$((total_tests + 1))
    
    log_info "Ejecutando: $test_name"
    
    if eval "$command" > "$RESULTS_DIR/${test_name// /_}.log" 2>&1; then
        log_success "$test_name - PASÓ"
        passed_tests=$((passed_tests + 1))
        return 0
    else
        log_error "$test_name - FALLÓ"
        failed_tests=$((failed_tests + 1))
        return 1
    fi
}

# Función para verificar conexión PostgreSQL
test_postgres_connection() {
    log_info "Verificando conexión a PostgreSQL..."
    
    if docker-compose exec -T postgres pg_isready -U paqueteria_user > /dev/null 2>&1; then
        log_success "PostgreSQL está listo"
        return 0
    else
        log_error "PostgreSQL no está respondiendo"
        return 1
    fi
}

# Función para verificar base de datos
test_database_exists() {
    log_info "Verificando que la base de datos existe..."
    
    local query="SELECT datname FROM pg_database WHERE datname = 'paqueteria';"
    local result=$(docker-compose exec -T postgres psql -U paqueteria_user -d paqueteria -t -c "$query" 2>/dev/null | tr -d ' ')
    
    if [ "$result" = "paqueteria" ]; then
        log_success "Base de datos 'paqueteria' existe"
        return 0
    else
        log_error "Base de datos 'paqueteria' no existe"
        return 1
    fi
}

# Función para verificar tablas
test_tables_exist() {
    log_info "Verificando que las tablas existen..."
    
    local tables=("users" "customers" "packages" "rates" "notifications" "messages" "files")
    local missing_tables=()
    
    for table in "${tables[@]}"; do
        local query="SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = '$table');"
        local result=$(docker-compose exec -T postgres psql -U paqueteria_user -d paqueteria -t -c "$query" 2>/dev/null | tr -d ' ')
        
        if [ "$result" = "t" ]; then
            log_success "Tabla '$table' existe"
        else
            log_error "Tabla '$table' no existe"
            missing_tables+=("$table")
        fi
    done
    
    if [ ${#missing_tables[@]} -eq 0 ]; then
        return 0
    else
        return 1
    fi
}

# Función para verificar migraciones
test_migrations() {
    log_info "Verificando estado de migraciones..."
    
    # Verificar que alembic está configurado
    if [ -f "alembic.ini" ]; then
        log_success "Alembic está configurado"
    else
        log_error "Alembic no está configurado"
        return 1
    fi
    
    # Verificar directorio de migraciones
    if [ -d "alembic/versions" ]; then
        log_success "Directorio de migraciones existe"
    else
        log_error "Directorio de migraciones no existe"
        return 1
    fi
    
    return 0
}

# Función para probar consultas básicas
test_basic_queries() {
    log_info "Probando consultas básicas..."
    
    # Probar SELECT
    local select_query="SELECT COUNT(*) FROM users;"
    local result=$(docker-compose exec -T postgres psql -U paqueteria_user -d paqueteria -t -c "$select_query" 2>/dev/null | tr -d ' ')
    
    if [ ! -z "$result" ] && [ "$result" -ge 0 ]; then
        log_success "Consulta SELECT funciona (usuarios: $result)"
    else
        log_error "Consulta SELECT falló"
        return 1
    fi
    
    # Probar INSERT (con rollback)
    local insert_query="BEGIN; INSERT INTO users (username, email, password_hash, first_name, last_name, role) VALUES ('test_user', 'test@test.com', 'hash', 'Test', 'User', 'user') ON CONFLICT DO NOTHING; ROLLBACK;"
    
    if docker-compose exec -T postgres psql -U paqueteria_user -d paqueteria -c "$insert_query" > /dev/null 2>&1; then
        log_success "Consulta INSERT funciona"
    else
        log_error "Consulta INSERT falló"
        return 1
    fi
    
    return 0
}

# Función para verificar índices
test_indexes() {
    log_info "Verificando índices importantes..."
    
    local indexes=(
        "packages_tracking_number_idx"
        "customers_phone_idx"
        "users_username_idx"
    )
    
    for index in "${indexes[@]}"; do
        local query="SELECT indexname FROM pg_indexes WHERE indexname = '$index';"
        local result=$(docker-compose exec -T postgres psql -U paqueteria_user -d paqueteria -t -c "$query" 2>/dev/null | tr -d ' ')
        
        if [ "$result" = "$index" ]; then
            log_success "Índice '$index' existe"
        else
            log_warning "Índice '$index' no existe"
        fi
    done
    
    return 0
}

# Función para verificar constraints
test_constraints() {
    log_info "Verificando constraints importantes..."
    
    # Verificar unique constraint en tracking_number
    local unique_query="SELECT conname FROM pg_constraint WHERE conname LIKE '%tracking_number%' AND contype = 'u';"
    local result=$(docker-compose exec -T postgres psql -U paqueteria_user -d paqueteria -t -c "$unique_query" 2>/dev/null | tr -d ' ')
    
    if [ ! -z "$result" ]; then
        log_success "Unique constraint en tracking_number existe"
    else
        log_warning "Unique constraint en tracking_number no encontrado"
    fi
    
    return 0
}

# Función para verificar permisos
test_permissions() {
    log_info "Verificando permisos de usuario..."
    
    # Verificar que el usuario puede conectarse
    if docker-compose exec -T postgres psql -U paqueteria_user -d paqueteria -c "SELECT 1;" > /dev/null 2>&1; then
        log_success "Usuario puede conectarse a la base de datos"
    else
        log_error "Usuario no puede conectarse a la base de datos"
        return 1
    fi
    
    # Verificar permisos de lectura
    if docker-compose exec -T postgres psql -U paqueteria_user -d paqueteria -c "SELECT * FROM users LIMIT 1;" > /dev/null 2>&1; then
        log_success "Usuario tiene permisos de lectura"
    else
        log_error "Usuario no tiene permisos de lectura"
        return 1
    fi
    
    return 0
}

# Iniciar pruebas
echo ""
log_info "Iniciando pruebas de base de datos..."

# Ejecutar pruebas
run_test "PostgreSQL Connection" "test_postgres_connection"
run_test "Database Exists" "test_database_exists"
run_test "Tables Exist" "test_tables_exist"
run_test "Migrations Status" "test_migrations"
run_test "Basic Queries" "test_basic_queries"
run_test "Indexes" "test_indexes"
run_test "Constraints" "test_constraints"
run_test "User Permissions" "test_permissions"

# Generar reporte
echo ""
log_info "Generando reporte de base de datos..."

cat > "TEST/reports/database-test.md" << EOF
# Prueba: Base de Datos Test

## 🎯 Objetivo
Verificar la funcionalidad y configuración de la base de datos PostgreSQL

## 🛠️ Configuración
- **Fecha**: $(date '+%Y-%m-%d %H:%M:%S')
- **Entorno**: development
- **Versión**: 3.0.0
- **Base de datos**: PostgreSQL 15
- **Usuario**: paqueteria_user

## 📊 Resultados
- **Estado**: $(if [ $failed_tests -eq 0 ]; then echo "✅ PASS"; else echo "❌ FAIL"; fi)
- **Tiempo de ejecución**: $(date '+%H:%M:%S')
- **Tests ejecutados**: $total_tests
- **Tests exitosos**: $passed_tests
- **Tests fallidos**: $failed_tests

## 🔍 Detalles

### Pruebas ejecutadas:
1. **Conexión PostgreSQL**: $(if test_postgres_connection > /dev/null 2>&1; then echo "✅ PASÓ"; else echo "❌ FALLÓ"; fi)
2. **Existencia de BD**: $(if test_database_exists > /dev/null 2>&1; then echo "✅ PASÓ"; else echo "❌ FALLÓ"; fi)
3. **Existencia de tablas**: $(if test_tables_exist > /dev/null 2>&1; then echo "✅ PASÓ"; else echo "❌ FALLÓ"; fi)
4. **Estado de migraciones**: $(if test_migrations > /dev/null 2>&1; then echo "✅ PASÓ"; else echo "❌ FALLÓ"; fi)
5. **Consultas básicas**: $(if test_basic_queries > /dev/null 2>&1; then echo "✅ PASÓ"; else echo "❌ FALLÓ"; fi)
6. **Índices**: $(if test_indexes > /dev/null 2>&1; then echo "✅ PASÓ"; else echo "❌ FALLÓ"; fi)
7. **Constraints**: $(if test_constraints > /dev/null 2>&1; then echo "✅ PASÓ"; else echo "❌ FALLÓ"; fi)
8. **Permisos de usuario**: $(if test_permissions > /dev/null 2>&1; then echo "✅ PASÓ"; else echo "❌ FALLÓ"; fi)

### Logs guardados en:
\`\`\`
$RESULTS_DIR/
\`\`\`

## 📈 Métricas
- **Tasa de éxito**: $((passed_tests * 100 / total_tests))%
- **Tasa de fallo**: $((failed_tests * 100 / total_tests))%

## ✅ Conclusiones
$(if [ $failed_tests -eq 0 ]; then
    echo "✅ La base de datos está configurada correctamente y funcionando"
else
    echo "❌ Se encontraron $failed_tests problemas en la base de datos"
fi)

## 🚀 Recomendaciones
$(if [ $failed_tests -eq 0 ]; then
    echo "- ✅ La base de datos está lista para uso en desarrollo"
    echo "- ✅ Se pueden proceder con las pruebas de API"
else
    echo "- ⚠️  Revisar la configuración de la base de datos"
    echo "- ⚠️  Verificar que las migraciones se ejecutaron correctamente"
    echo "- ⚠️  Comprobar permisos de usuario"
fi)
EOF

# Mostrar resumen final
echo ""
log_info "=== Resumen de Pruebas de Base de Datos ==="
echo "📊 Total de tests: $total_tests"
echo "✅ Exitosos: $passed_tests"
echo "❌ Fallidos: $failed_tests"
echo "📄 Reporte: TEST/reports/database-test.md"
echo "📁 Logs: $RESULTS_DIR/"

# Guardar log
{
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Database Tests completados"
    echo "Total: $total_tests, Exitosos: $passed_tests, Fallidos: $failed_tests"
} >> "$LOGS_DIR/database-test.log"

# Retornar código de salida
if [ $failed_tests -eq 0 ]; then
    log_success "🎉 Todas las pruebas de base de datos pasaron!"
    exit 0
else
    log_error "❌ $failed_tests pruebas de base de datos fallaron"
    exit 1
fi
