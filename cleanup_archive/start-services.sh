#!/bin/bash

# ========================================
# PAQUETES EL CLUB v3.0 - Iniciar Servicios
# ========================================

set -e

echo "🚀 Iniciando servicios de PAQUETES EL CLUB v3.0..."

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

# Verificar que estamos en el directorio correcto
if [ ! -f "docker-compose.yml" ]; then
    log_error "No se encontró docker-compose.yml. Ejecuta este script desde el directorio raíz del proyecto."
    exit 1
fi

# Verificar que Docker esté ejecutándose
if ! docker info > /dev/null 2>&1; then
    log_error "Docker no está ejecutándose. Por favor inicia Docker primero."
    exit 1
fi

# Detener servicios existentes si están corriendo
log_info "Deteniendo servicios existentes..."
docker-compose down --remove-orphans 2>/dev/null || true
log_success "Servicios detenidos"

# Construir imágenes si es necesario
log_info "Construyendo imágenes Docker..."
docker-compose build --no-cache
log_success "Imágenes construidas"

# Iniciar servicios
log_info "Iniciando servicios..."
docker-compose up -d

# Esperar a que los servicios estén listos
log_info "Esperando a que los servicios estén listos..."
sleep 10

# Verificar estado de los servicios
log_info "Verificando estado de los servicios..."

# Función para verificar servicio
check_service() {
    local service_name=$1
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if docker-compose ps $service_name | grep -q "Up"; then
            log_success "$service_name está ejecutándose"
            return 0
        fi
        
        log_info "Esperando $service_name... (intento $attempt/$max_attempts)"
        sleep 2
        attempt=$((attempt + 1))
    done
    
    log_error "$service_name no pudo iniciarse"
    return 1
}

# Verificar cada servicio
services=("postgres" "redis" "fastapi" "nginx" "prometheus" "grafana")
all_services_ok=true

for service in "${services[@]}"; do
    if ! check_service $service; then
        all_services_ok=false
    fi
done

if [ "$all_services_ok" = false ]; then
    log_error "Algunos servicios no pudieron iniciarse correctamente"
    log_info "Revisando logs..."
    docker-compose logs --tail=20
    exit 1
fi

# Verificar conectividad de servicios
log_info "Verificando conectividad..."

# Verificar PostgreSQL
if docker-compose exec -T postgres pg_isready -U paqueteria_user > /dev/null 2>&1; then
    log_success "PostgreSQL está listo"
else
    log_error "PostgreSQL no está respondiendo"
    all_services_ok=false
fi

# Verificar Redis
if docker-compose exec -T redis redis-cli ping > /dev/null 2>&1; then
    log_success "Redis está listo"
else
    log_error "Redis no está respondiendo"
    all_services_ok=false
fi

# Verificar FastAPI
if curl -s http://localhost/health > /dev/null 2>&1; then
    log_success "FastAPI está respondiendo"
else
    log_warning "FastAPI aún no está respondiendo (puede tardar unos segundos más)"
fi

# Verificar Nginx
if curl -s http://localhost > /dev/null 2>&1; then
    log_success "Nginx está respondiendo"
else
    log_warning "Nginx aún no está respondiendo"
fi

# Mostrar información de acceso
echo ""
log_success "🎉 Servicios iniciados exitosamente!"
echo ""
echo "📋 Información de acceso:"
echo "├── 🌐 Aplicación:     http://localhost"
echo "├── 📚 API Docs:       http://localhost/api/docs"
echo "├── 🔍 Health Check:   http://localhost/health"
echo "├── 📊 Prometheus:     http://localhost:9090"
echo "├── 📈 Grafana:        http://localhost:3000"
echo "└── 🗄️  PostgreSQL:    localhost:5432"
echo ""
echo "👤 Credenciales por defecto:"
echo "├── Grafana: admin / Grafana2025!Secure"
echo "└── PostgreSQL: paqueteria_user / Paqueteria2025!Secure"
echo ""

# Guardar información en log
{
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Servicios iniciados"
    echo "Aplicación: http://localhost"
    echo "API Docs: http://localhost/api/docs"
    echo "Health Check: http://localhost/health"
    echo "Prometheus: http://localhost:9090"
    echo "Grafana: http://localhost:3000"
} > TEST/results/logs/services-started.log

# Mostrar logs de servicios
log_info "Últimos logs de servicios:"
docker-compose logs --tail=10

echo ""
log_info "Para ver logs en tiempo real: docker-compose logs -f"
log_info "Para detener servicios: ./SCRIPTS/stop-services.sh"
