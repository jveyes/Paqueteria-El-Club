#!/bin/bash

# ========================================
# PAQUETES EL CLUB v3.0 - Prueba Rápida del Sistema
# ========================================

echo "🚀 Prueba rápida del sistema PAQUETES EL CLUB v3.0..."

# Colores
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# Función para logging
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Verificar Docker
log_info "Verificando Docker..."
if docker info > /dev/null 2>&1; then
    log_success "Docker está ejecutándose"
else
    log_error "Docker no está ejecutándose"
    exit 1
fi

# Verificar archivos del proyecto
log_info "Verificando archivos del proyecto..."
if [ -f "docker-compose.yml" ]; then
    log_success "docker-compose.yml encontrado"
else
    log_error "docker-compose.yml no encontrado"
    exit 1
fi

if [ -f "src/main.py" ]; then
    log_success "main.py encontrado"
else
    log_error "main.py no encontrado"
    exit 1
fi

# Verificar estructura de directorios
log_info "Verificando estructura de directorios..."
directories=("src" "src/models" "src/routers" "src/services" "src/utils" "TEST" "SCRIPTS")
for dir in "${directories[@]}"; do
    if [ -d "$dir" ]; then
        log_success "Directorio $dir existe"
    else
        log_error "Directorio $dir no existe"
    fi
done

# Verificar servicios Docker
log_info "Verificando servicios Docker..."
if docker-compose ps | grep -q "Up"; then
    log_success "Servicios Docker están ejecutándose"
    
    # Verificar FastAPI
    if curl -s http://localhost/health > /dev/null 2>&1; then
        log_success "FastAPI está respondiendo"
    else
        log_warning "FastAPI no está respondiendo (puede estar iniciando)"
    fi
else
    log_warning "Servicios Docker no están ejecutándose"
    log_info "Para iniciar servicios: docker-compose up -d"
fi

# Verificar base de datos
log_info "Verificando base de datos..."
if docker-compose exec -T postgres pg_isready -U paqueteria_user > /dev/null 2>&1; then
    log_success "PostgreSQL está listo"
else
    log_warning "PostgreSQL no está respondiendo"
fi

# Verificar Redis
log_info "Verificando Redis..."
if docker-compose exec -T redis redis-cli ping > /dev/null 2>&1; then
    log_success "Redis está funcionando"
else
    log_warning "Redis no está respondiendo"
fi

echo ""
log_success "🎉 Prueba rápida completada!"
echo ""
echo "📋 Información de acceso:"
echo "├── 🌐 Aplicación:     http://localhost"
echo "├── 📚 API Docs:       http://localhost/api/docs"
echo "├── 🔍 Health Check:   http://localhost/health"
echo "├── 📊 Prometheus:     http://localhost:9090"
echo "└── 📈 Grafana:        http://localhost:3000"
echo ""
echo "📁 Estructura de pruebas creada:"
echo "├── TEST/config/       # Configuración de pruebas"
echo "├── TEST/data/         # Datos de prueba"
echo "├── TEST/reports/      # Reportes de pruebas"
echo "└── SCRIPTS/           # Scripts de automatización"
