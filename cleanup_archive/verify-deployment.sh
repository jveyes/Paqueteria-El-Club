#!/bin/bash

# ========================================
# PAQUETES EL CLUB v3.1 - Verificación de Despliegue
# ========================================
# Fecha: 25 de Agosto, 2025
# Versión: 1.0
# Descripción: Verifica que todos los servicios estén funcionando correctamente

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para logging
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
}

success() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] ✅ $1${NC}"
}

fail() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ❌ $1${NC}"
}

# Variables de estado
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Función para ejecutar test
run_test() {
    local test_name="$1"
    local test_command="$2"
    local expected_result="$3"
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    echo -n "Probando: $test_name... "
    
    if eval "$test_command" > /dev/null 2>&1; then
        success "$test_name"
        PASSED_TESTS=$((PASSED_TESTS + 1))
        return 0
    else
        fail "$test_name"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        return 1
    fi
}

# Función para verificar contenedores
check_containers() {
    log "Verificando contenedores Docker..."
    
    local containers=(
        "paqueteria_v31_postgres"
        "paqueteria_v31_redis"
        "paqueteria_v31_app"
        "paqueteria_v31_celery_worker"
        "paqueteria_v31_nginx"
    )
    
    for container in "${containers[@]}"; do
        run_test "Contenedor $container está corriendo" \
                "docker ps --format '{{.Names}}' | grep -q '^$container$'" \
                "running"
    done
}

# Función para verificar puertos
check_ports() {
    log "Verificando puertos de servicios..."
    
    local ports=(
        "80:nginx"
        "443:nginx-ssl"
        "8001:fastapi"
        "5432:postgresql"
        "6380:redis"
    )
    
    for port_info in "${ports[@]}"; do
        local port=$(echo $port_info | cut -d: -f1)
        local service=$(echo $port_info | cut -d: -f2)
        
        run_test "Puerto $port ($service) está abierto" \
                "netstat -tuln | grep -q ':$port ' || ss -tuln | grep -q ':$port '" \
                "open"
    done
}

# Función para verificar endpoints HTTP
check_http_endpoints() {
    log "Verificando endpoints HTTP..."
    
    # Health check
    run_test "Health check endpoint" \
            "curl -s -f http://localhost/health > /dev/null" \
            "200 OK"
    
    # Página principal
    run_test "Página principal" \
            "curl -s -f http://localhost > /dev/null" \
            "200 OK"
    
    # API docs
    run_test "API documentation" \
            "curl -s -f http://localhost:8001/docs > /dev/null" \
            "200 OK"
    
    # API directa
    run_test "API directa" \
            "curl -s -f http://localhost:8001/health > /dev/null" \
            "200 OK"
}

# Función para verificar base de datos
check_database() {
    log "Verificando conexión a base de datos..."
    
    run_test "PostgreSQL está respondiendo" \
            "docker exec paqueteria_v31_postgres pg_isready -U paqueteria_user -d paqueteria" \
            "ready"
}

# Función para verificar Redis
check_redis() {
    log "Verificando conexión a Redis..."
    
    run_test "Redis está respondiendo" \
            "docker exec paqueteria_v31_redis redis-cli ping" \
            "PONG"
}

# Función para verificar logs
check_logs() {
    log "Verificando logs de servicios..."
    
    local services=("app" "postgres" "redis" "nginx")
    
    for service in "${services[@]}"; do
        run_test "Logs de $service están disponibles" \
                "docker-compose logs --tail=1 $service > /dev/null 2>&1" \
                "available"
    done
}

# Función para verificar recursos del sistema
check_system_resources() {
    log "Verificando recursos del sistema..."
    
    # Verificar memoria disponible
    local available_memory=$(free -m | awk 'NR==2{printf "%.0f", $7}')
    if [ $available_memory -gt 512 ]; then
        success "Memoria disponible: ${available_memory}MB"
    else
        warn "Memoria disponible baja: ${available_memory}MB"
    fi
    
    # Verificar espacio en disco
    local available_disk=$(df -BG . | awk 'NR==2{print $4}' | sed 's/G//')
    if [ $available_disk -gt 10 ]; then
        success "Espacio en disco disponible: ${available_disk}GB"
    else
        warn "Espacio en disco bajo: ${available_disk}GB"
    fi
    
    # Verificar uso de CPU
    local cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | sed 's/%us,//')
    if (( $(echo "$cpu_usage < 80" | bc -l) )); then
        success "Uso de CPU: ${cpu_usage}%"
    else
        warn "Uso de CPU alto: ${cpu_usage}%"
    fi
}

# Función para verificar archivos críticos
check_critical_files() {
    log "Verificando archivos críticos..."
    
    local files=(
        ".env"
        "code/.env"
        "code/src/main.py"
        "code/templates/index.html"
        "docker-compose.yml"
    )
    
    for file in "${files[@]}"; do
        run_test "Archivo $file existe" \
                "test -f '$file'" \
                "exists"
    done
}

# Función para mostrar resumen
show_summary() {
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}        RESUMEN DE VERIFICACIÓN        ${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    echo -e "Total de tests: ${TOTAL_TESTS}"
    echo -e "Tests exitosos: ${GREEN}${PASSED_TESTS}${NC}"
    echo -e "Tests fallidos: ${RED}${FAILED_TESTS}${NC}"
    echo ""
    
    if [ $FAILED_TESTS -eq 0 ]; then
        echo -e "${GREEN}🎉 ¡TODOS LOS TESTS PASARON!${NC}"
        echo -e "${GREEN}✅ El despliegue está funcionando correctamente${NC}"
    else
        echo -e "${YELLOW}⚠️  Algunos tests fallaron${NC}"
        echo -e "${YELLOW}Revisa los logs para más detalles${NC}"
    fi
    
    echo ""
    echo -e "${BLUE}URLs de Acceso:${NC}"
    echo -e "  • Aplicación: ${BLUE}http://localhost${NC}"
    echo -e "  • Health: ${BLUE}http://localhost/health${NC}"
    echo -e "  • API Docs: ${BLUE}http://localhost:8001/docs${NC}"
    echo ""
}

# Función para mostrar información de diagnóstico
show_diagnostic_info() {
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}        INFORMACIÓN DE DIAGNÓSTICO     ${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    
    echo -e "${YELLOW}Estado de contenedores:${NC}"
    docker-compose ps
    
    echo ""
    echo -e "${YELLOW}Uso de recursos:${NC}"
    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"
    
    echo ""
    echo -e "${YELLOW}Logs recientes de la aplicación:${NC}"
    docker-compose logs --tail=5 app
}

# Función principal
main() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}  PAQUETES EL CLUB v3.1 - VERIFICACIÓN ${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    
    # Verificar que estamos en el directorio correcto
    if [ ! -f "docker-compose.yml" ]; then
        error "No se encontró docker-compose.yml. Ejecuta este script desde el directorio raíz del proyecto."
        exit 1
    fi
    
    # Ejecutar verificaciones
    check_critical_files
    check_containers
    check_ports
    check_database
    check_redis
    check_http_endpoints
    check_logs
    check_system_resources
    
    # Mostrar resumen
    show_summary
    
    # Si hay fallos, mostrar información de diagnóstico
    if [ $FAILED_TESTS -gt 0 ]; then
        show_diagnostic_info
    fi
}

# Ejecutar función principal
main "$@"
