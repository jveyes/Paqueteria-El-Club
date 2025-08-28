#!/bin/bash

# ========================================
# PAQUETES EL CLUB v3.1 - MONITOREO DE RECURSOS
# ========================================

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para logging
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

error() {
    echo -e "${RED}❌ $1${NC}"
}

# Función para obtener uso de CPU
get_cpu_usage() {
    top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1
}

# Función para obtener uso de memoria
get_memory_usage() {
    free | grep Mem | awk '{printf "%.1f", $3/$2 * 100.0}'
}

# Función para obtener uso de disco
get_disk_usage() {
    df / | tail -1 | awk '{print $5}' | cut -d'%' -f1
}

# Función para obtener estadísticas de Docker
get_docker_stats() {
    echo "=== ESTADÍSTICAS DE CONTENEDORES ==="
    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}\t{{.NetIO}}\t{{.BlockIO}}"
    echo ""
}

# Función para obtener logs de errores recientes
get_recent_errors() {
    echo "=== LOGS DE ERRORES RECIENTES ==="
    docker-compose logs --tail=10 | grep -i error || echo "No se encontraron errores recientes"
    echo ""
}

# Función para verificar conectividad de servicios
check_services() {
    echo "=== VERIFICACIÓN DE SERVICIOS ==="
    
    # PostgreSQL
    if docker exec paqueteria_v31_postgres pg_isready -U postgres >/dev/null 2>&1; then
        success "PostgreSQL: Conectado"
    else
        error "PostgreSQL: Error de conexión"
    fi
    
    # Redis
    if docker exec paqueteria_v31_redis redis-cli ping >/dev/null 2>&1; then
        success "Redis: Conectado"
    else
        error "Redis: Error de conexión"
    fi
    
    # FastAPI
    if curl -s http://localhost:8001/health >/dev/null 2>&1; then
        success "FastAPI: Respondiendo"
    else
        error "FastAPI: No responde"
    fi
    
    # Nginx
    if curl -s http://localhost >/dev/null 2>&1; then
        success "Nginx: Respondiendo"
    else
        error "Nginx: No responde"
    fi
    
    echo ""
}

# Función principal de monitoreo
main() {
    log "Iniciando monitoreo de recursos..."
    echo ""
    
    # Información del sistema
    echo "========================================"
    echo "    MONITOREO DE RECURSOS v3.1          "
    echo "========================================"
    echo ""
    
    # CPU
    cpu_usage=$(get_cpu_usage)
    echo "CPU Usage: ${cpu_usage}%"
    if (( $(echo "$cpu_usage > 80" | bc -l) )); then
        warning "CPU usage alto"
    elif (( $(echo "$cpu_usage > 60" | bc -l) )); then
        warning "CPU usage moderado"
    else
        success "CPU usage normal"
    fi
    
    # Memoria
    mem_usage=$(get_memory_usage)
    echo "Memory Usage: ${mem_usage}%"
    if (( $(echo "$mem_usage > 80" | bc -l) )); then
        warning "Memory usage alto"
    elif (( $(echo "$mem_usage > 60" | bc -l) )); then
        warning "Memory usage moderado"
    else
        success "Memory usage normal"
    fi
    
    # Disco
    disk_usage=$(get_disk_usage)
    echo "Disk Usage: ${disk_usage}%"
    if (( $(echo "$disk_usage > 80" | bc -l) )); then
        warning "Disk usage alto"
    elif (( $(echo "$disk_usage > 60" | bc -l) )); then
        warning "Disk usage moderado"
    else
        success "Disk usage normal"
    fi
    
    echo ""
    
    # Verificar servicios
    check_services
    
    # Estadísticas de Docker
    get_docker_stats
    
    # Logs de errores
    get_recent_errors
    
    # Resumen
    echo "========================================"
    echo "           RESUMEN DEL SISTEMA          "
    echo "========================================"
    echo "CPU: ${cpu_usage}% | Memoria: ${mem_usage}% | Disco: ${disk_usage}%"
    echo ""
    
    # Recomendaciones
    if (( $(echo "$cpu_usage > 80" || echo "$mem_usage > 80" || echo "$disk_usage > 80" | bc -l) )); then
        warning "⚠️  Se recomienda revisar el uso de recursos"
    else
        success "✅ Sistema funcionando correctamente"
    fi
}

# Ejecutar función principal
main "$@"
