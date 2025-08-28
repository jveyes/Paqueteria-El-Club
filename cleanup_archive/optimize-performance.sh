#!/bin/bash

# ========================================
# PAQUETES EL CLUB v3.1 - OPTIMIZACIÓN DE RENDIMIENTO
# ========================================

set -e

# Colores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Función para logging
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

error() {
    echo -e "${RED}❌ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Función para optimizar PostgreSQL
optimize_postgresql() {
    log "Optimizando PostgreSQL..."
    
    # Configuraciones recomendadas para 1GB RAM
    docker exec paqueteria_v31_postgres psql -U postgres -d paqueteria -c "
        ALTER SYSTEM SET shared_buffers = '128MB';
        ALTER SYSTEM SET effective_cache_size = '256MB';
        ALTER SYSTEM SET work_mem = '4MB';
        ALTER SYSTEM SET maintenance_work_mem = '32MB';
        ALTER SYSTEM SET max_connections = 50;
        ALTER SYSTEM SET checkpoint_completion_target = 0.9;
        ALTER SYSTEM SET wal_buffers = '4MB';
        ALTER SYSTEM SET default_statistics_target = 100;
        ALTER SYSTEM SET random_page_cost = 1.1;
        ALTER SYSTEM SET effective_io_concurrency = 200;
    "
    
    # Recargar configuración
    docker exec paqueteria_v31_postgres psql -U postgres -d paqueteria -c "SELECT pg_reload_conf();"
    
    success "PostgreSQL optimizado"
}

# Función para optimizar Redis
optimize_redis() {
    log "Optimizando Redis..."
    
    # Configuraciones para 1GB RAM
    docker exec paqueteria_v31_redis redis-cli CONFIG SET maxmemory "64mb"
    docker exec paqueteria_v31_redis redis-cli CONFIG SET maxmemory-policy "allkeys-lru"
    docker exec paqueteria_v31_redis redis-cli CONFIG SET maxclients 50
    docker exec paqueteria_v31_redis redis-cli CONFIG SET save ""
    docker exec paqueteria_v31_redis redis-cli CONFIG SET appendonly "no"
    
    success "Redis optimizado"
}

# Función para limpiar logs y archivos temporales
cleanup_system() {
    log "Limpiando sistema..."
    
    # Limpiar logs de Docker
    docker system prune -f
    
    # Limpiar archivos temporales
    find /tmp -type f -mtime +7 -delete 2>/dev/null || true
    find /var/tmp -type f -mtime +7 -delete 2>/dev/null || true
    
    # Limpiar logs antiguos
    find . -name "*.log" -mtime +7 -delete 2>/dev/null || true
    
    success "Sistema limpiado"
}

# Función para verificar rendimiento
check_performance() {
    log "Verificando rendimiento..."
    
    echo "=== RENDIMIENTO ACTUAL ==="
    
    # CPU
    cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
    echo "CPU Usage: ${cpu_usage}%"
    
    # Memoria
    mem_usage=$(free | grep Mem | awk '{printf "%.1f", $3/$2 * 100.0}')
    echo "Memory Usage: ${mem_usage}%"
    
    # PostgreSQL
    pg_connections=$(docker exec paqueteria_v31_postgres psql -U postgres -d paqueteria -t -c "SELECT count(*) FROM pg_stat_activity;" 2>/dev/null || echo "0")
    echo "PostgreSQL Connections: $pg_connections"
    
    # Redis
    redis_memory=$(docker exec paqueteria_v31_redis redis-cli info memory | grep "used_memory_human" | cut -d: -f2)
    echo "Redis Memory: $redis_memory"
    
    # Contenedores
    echo "Contenedores activos:"
    docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep paqueteria_v31
    
    echo ""
}

# Función para generar reporte de optimización
generate_report() {
    log "Generando reporte de optimización..."
    
    cat > "optimization_report_$(date +%Y%m%d_%H%M%S).md" << EOF
# Reporte de Optimización - PAQUETES EL CLUB v3.1

**Fecha:** $(date)
**Versión:** 3.1.0

## Configuraciones Aplicadas

### PostgreSQL
- shared_buffers: 128MB
- effective_cache_size: 256MB
- work_mem: 4MB
- maintenance_work_mem: 32MB
- max_connections: 50
- checkpoint_completion_target: 0.9
- wal_buffers: 4MB
- default_statistics_target: 100
- random_page_cost: 1.1
- effective_io_concurrency: 200

### Redis
- maxmemory: 64mb
- maxmemory-policy: allkeys-lru
- maxclients: 50
- save: "" (deshabilitado)
- appendonly: no

### Sistema
- Limpieza de logs antiguos
- Limpieza de archivos temporales
- Optimización de Docker

## Recomendaciones para Producción

1. **Monitoreo Continuo**
   - Ejecutar \`./code/SCRIPTS/monitor-resources.sh\` cada hora
   - Configurar alertas para uso de CPU > 80%

2. **Backups Automáticos**
   - Ejecutar \`./code/SCRIPTS/backup-automatic.sh\` diariamente
   - Mantener backups de los últimos 7 días

3. **Escalabilidad**
   - Para más de 50 usuarios, considerar aumentar recursos
   - Monitorear tiempos de respuesta de APIs

4. **Seguridad**
   - Cambiar contraseñas por defecto
   - Configurar firewall
   - Habilitar SSL/TLS

## Comandos Útiles

\`\`\`bash
# Verificar rendimiento
./code/SCRIPTS/monitor-resources.sh

# Crear backup
./code/SCRIPTS/backup-automatic.sh

# Testing de APIs
./code/SCRIPTS/test-api-simple.sh

# Verificar despliegue
./code/SCRIPTS/verify-deployment.sh
\`\`\`
EOF
    
    success "Reporte generado: optimization_report_$(date +%Y%m%d_%H%M%S).md"
}

# Función principal
main() {
    log "Iniciando optimización de rendimiento..."
    echo ""
    
    # Verificar rendimiento antes
    log "Rendimiento antes de la optimización:"
    check_performance
    echo ""
    
    # Aplicar optimizaciones
    optimize_postgresql
    optimize_redis
    cleanup_system
    
    echo ""
    
    # Verificar rendimiento después
    log "Rendimiento después de la optimización:"
    check_performance
    echo ""
    
    # Generar reporte
    generate_report
    
    echo "========================================"
    echo "     OPTIMIZACIÓN COMPLETADA            "
    echo "========================================"
    success "🎉 Sistema optimizado para máximo rendimiento"
    echo ""
    warning "Recomendación: Reiniciar servicios para aplicar cambios completos"
    echo "Comando: docker-compose restart"
}

# Ejecutar función principal
main "$@"
