#!/bin/bash

# ========================================
# PAQUETES EL CLUB v3.0 - Configurar Entorno de Pruebas
# ========================================

set -e

echo "🚀 Configurando entorno de pruebas para PAQUETES EL CLUB v3.0..."

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

log_info "Verificando dependencias..."

# Verificar Docker
if ! command -v docker &> /dev/null; then
    log_error "Docker no está instalado. Por favor instala Docker primero."
    exit 1
fi

# Verificar Docker Compose
if ! command -v docker-compose &> /dev/null; then
    log_error "Docker Compose no está instalado. Por favor instala Docker Compose primero."
    exit 1
fi

# Verificar curl
if ! command -v curl &> /dev/null; then
    log_warning "curl no está instalado. Algunas pruebas de API pueden fallar."
fi

# Verificar jq
if ! command -v jq &> /dev/null; then
    log_warning "jq no está instalado. La validación de JSON puede fallar."
fi

log_success "Dependencias verificadas"

# Crear archivo .env si no existe
if [ ! -f ".env" ]; then
    log_info "Creando archivo .env desde env.example..."
    cp env.example .env
    log_success "Archivo .env creado"
else
    log_info "Archivo .env ya existe"
fi

# Crear directorios de logs si no existen
log_info "Creando directorios de logs..."
mkdir -p logs
mkdir -p TEST/results/logs
log_success "Directorios de logs creados"

# Crear archivo de configuración de pruebas
log_info "Creando configuración de pruebas..."
cat > TEST/config/test-config.json << EOF
{
  "test_environment": {
    "name": "PAQUETES EL CLUB v3.0",
    "version": "3.0.0",
    "base_url": "http://localhost",
    "api_base_url": "http://localhost/api",
    "timeout": 30,
    "retries": 3
  },
  "database": {
    "host": "localhost",
    "port": 5432,
    "name": "paqueteria",
    "user": "paqueteria_user"
  },
  "monitoring": {
    "prometheus_url": "http://localhost:9090",
    "grafana_url": "http://localhost:3000"
  },
  "test_data": {
    "admin_user": {
      "username": "admin",
      "email": "admin@papyrus.com.co",
      "password": "Admin2025!Secure"
    },
    "test_customer": {
      "name": "Cliente Prueba",
      "phone": "3334004007"
    }
  }
}
EOF
log_success "Configuración de pruebas creada"

# Crear datos de prueba
log_info "Creando datos de prueba..."
cat > TEST/data/test-users.json << EOF
[
  {
    "username": "admin",
    "email": "admin@papyrus.com.co",
    "password": "Admin2025!Secure",
    "first_name": "Administrador",
    "last_name": "Sistema",
    "role": "admin"
  },
  {
    "username": "operator",
    "email": "operator@papyrus.com.co",
    "password": "Operator2025!Secure",
    "first_name": "Operador",
    "last_name": "Sistema",
    "role": "operator"
  },
  {
    "username": "user",
    "email": "user@papyrus.com.co",
    "password": "User2025!Secure",
    "first_name": "Usuario",
    "last_name": "Prueba",
    "role": "user"
  }
]
EOF

cat > TEST/data/test-packages.json << EOF
[
  {
    "customer_name": "Juan Pérez",
    "customer_phone": "3334004007",
    "package_type": "normal",
    "package_condition": "bueno",
    "observations": "Paquete de prueba"
  },
  {
    "customer_name": "María García",
    "customer_phone": "3334004008",
    "package_type": "extra_dimensionado",
    "package_condition": "regular",
    "observations": "Paquete grande de prueba"
  }
]
EOF

cat > TEST/data/test-customers.json << EOF
[
  {
    "name": "Juan Pérez",
    "phone": "3334004007"
  },
  {
    "name": "María García",
    "phone": "3334004008"
  },
  {
    "name": "Carlos López",
    "phone": "3334004009"
  }
]
EOF

cat > TEST/data/test-rates.json << EOF
[
  {
    "rate_type": "storage",
    "base_price": 1000,
    "daily_storage_rate": 100,
    "is_active": true
  },
  {
    "rate_type": "delivery",
    "base_price": 1500,
    "delivery_rate": 1500,
    "is_active": true
  },
  {
    "rate_type": "package_type",
    "package_type_multiplier": 1.5,
    "is_active": true
  }
]
EOF
log_success "Datos de prueba creados"

# Crear endpoints de prueba
log_info "Creando configuración de endpoints..."
cat > TEST/config/api-endpoints.json << EOF
{
  "base_url": "http://localhost",
  "endpoints": {
    "health": "/health",
    "metrics": "/metrics",
    "docs": "/api/docs",
    "auth": {
      "register": "/api/auth/register",
      "login": "/api/auth/login",
      "logout": "/api/auth/logout",
      "me": "/api/auth/me"
    },
    "packages": {
      "announce": "/api/packages/announce",
      "track": "/api/packages/{tracking_number}",
      "list": "/api/packages/",
      "receive": "/api/packages/{id}/receive",
      "deliver": "/api/packages/{id}/deliver",
      "cancel": "/api/packages/{id}/cancel",
      "stats": "/api/packages/stats"
    },
    "customers": {
      "create": "/api/customers/",
      "list": "/api/customers/",
      "get": "/api/customers/{tracking_number}"
    },
    "rates": {
      "list": "/api/rates/",
      "create": "/api/rates/",
      "calculate": "/api/rates/calculate"
    },
    "notifications": {
      "list": "/api/notifications/"
    },
    "admin": {
      "dashboard": "/api/admin/dashboard"
    }
  }
}
EOF
log_success "Configuración de endpoints creada"

# Crear escenarios de prueba
log_info "Creando escenarios de prueba..."
cat > TEST/config/test-scenarios.json << EOF
{
  "scenarios": [
    {
      "name": "infrastructure_test",
      "description": "Pruebas de infraestructura básica",
      "steps": [
        "docker_services_check",
        "database_connection_test",
        "redis_connection_test",
        "nginx_proxy_test"
      ]
    },
    {
      "name": "authentication_test",
      "description": "Pruebas del sistema de autenticación",
      "steps": [
        "user_registration",
        "user_login",
        "jwt_token_validation",
        "user_logout"
      ]
    },
    {
      "name": "packages_test",
      "description": "Pruebas de funcionalidad de paquetes",
      "steps": [
        "create_package",
        "track_package",
        "update_package_status",
        "calculate_costs"
      ]
    },
    {
      "name": "customers_test",
      "description": "Pruebas de gestión de clientes",
      "steps": [
        "create_customer",
        "search_customer",
        "update_customer"
      ]
    },
    {
      "name": "rates_test",
      "description": "Pruebas de cálculo de tarifas",
      "steps": [
        "create_rate",
        "calculate_package_cost",
        "rate_history"
      ]
    },
    {
      "name": "notifications_test",
      "description": "Pruebas de sistema de notificaciones",
      "steps": [
        "send_email_notification",
        "send_sms_notification",
        "notification_status"
      ]
    }
  ]
}
EOF
log_success "Escenarios de prueba creados"

# Hacer ejecutables los scripts
log_info "Configurando permisos de ejecución..."
chmod +x SCRIPTS/*.sh
log_success "Permisos configurados"

# Crear archivo de timestamp
echo "$(date '+%Y-%m-%d %H:%M:%S') - Entorno de pruebas configurado" > TEST/results/logs/setup.log

log_success "🎉 Entorno de pruebas configurado exitosamente!"
echo ""
echo "📋 Próximos pasos:"
echo "1. Ejecutar: ./SCRIPTS/start-services.sh"
echo "2. Ejecutar: ./SCRIPTS/run-migrations.sh"
echo "3. Ejecutar: ./SCRIPTS/run-all-tests.sh"
echo ""
echo "📁 Estructura creada:"
echo "├── TEST/config/          # Configuración de pruebas"
echo "├── TEST/data/            # Datos de prueba"
echo "├── TEST/reports/         # Reportes de pruebas"
echo "├── TEST/results/         # Resultados de pruebas"
echo "└── SCRIPTS/              # Scripts de automatización"
echo ""
