#!/bin/bash
# ========================================
# PAQUETES EL CLUB v3.1 - Setup Completo del Sistema de Autenticación
# ========================================

set -e

echo "🚀 Configurando sistema completo de autenticación con emails..."

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Función para imprimir mensajes
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_step() {
    echo -e "${PURPLE}[STEP]${NC} $1"
}

# Verificar que estamos en el directorio correcto
if [ ! -f "src/main.py" ]; then
    print_error "Este script debe ejecutarse desde el directorio 'code'"
    exit 1
fi

print_step "1. Verificando estructura del proyecto..."

# Verificar que existan los archivos necesarios
required_files=(
    "src/main.py"
    "src/routers/auth.py"
    "src/models/user.py"
    "src/schemas/auth.py"
    "src/dependencies.py"
    "src/config.py"
    "src/services/notification_service.py"
)

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        print_error "Archivo requerido no encontrado: $file"
        exit 1
    fi
done

print_success "Estructura del proyecto verificada"

print_step "2. Creando directorios necesarios..."

# Crear directorios necesarios
mkdir -p logs
mkdir -p uploads
mkdir -p static/images
mkdir -p static/documents

print_success "Directorios creados"

print_step "3. Verificando estado de Docker..."

# Verificar si Docker está ejecutándose
if ! docker info > /dev/null 2>&1; then
    print_warning "Docker no está ejecutándose. Iniciando servicios..."
    
    # Intentar iniciar los servicios
    if [ -f "docker-compose.yml" ]; then
        print_status "Iniciando servicios con Docker Compose..."
        docker-compose up -d postgres redis
        
        # Esperar a que PostgreSQL esté listo
        print_status "Esperando a que PostgreSQL esté listo..."
        sleep 15
    else
        print_error "No se encontró docker-compose.yml"
        exit 1
    fi
else
    print_success "Docker está ejecutándose"
fi

print_step "4. Ejecutando migraciones de base de datos..."

# Ejecutar migraciones
if [ -f "alembic.ini" ]; then
    print_status "Ejecutando migraciones con Alembic..."
    cd src
    alembic upgrade head
    cd ..
    print_success "Migraciones ejecutadas"
else
    print_warning "No se encontró alembic.ini, creando tablas directamente..."
    cd src
    python -c "
from models import base
from database.database import engine
base.Base.metadata.create_all(bind=engine)
print('Tablas creadas exitosamente')
"
    cd ..
fi

print_step "5. Creando usuario administrador..."

# Crear usuario administrador
cd src
python scripts/create_admin_user.py
cd ..

print_success "Usuario administrador creado"

print_step "6. Probando sistema de emails..."

# Probar sistema de emails
print_status "Ejecutando pruebas del sistema de emails..."
python test_email_system.py

print_success "Pruebas de email completadas"

print_step "7. Verificando que el servidor esté ejecutándose..."

# Verificar que el servidor esté ejecutándose
if ! curl -s http://localhost:8000/health > /dev/null; then
    print_warning "El servidor no está ejecutándose en el puerto 8000"
    print_status "Iniciando servidor en segundo plano..."
    
    # Iniciar servidor en segundo plano
    nohup python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload > logs/server.log 2>&1 &
    SERVER_PID=$!
    
    # Esperar a que el servidor esté listo
    print_status "Esperando a que el servidor esté listo..."
    sleep 10
    
    # Verificar que el servidor esté ejecutándose
    if curl -s http://localhost:8000/health > /dev/null; then
        print_success "Servidor iniciado correctamente (PID: $SERVER_PID)"
        echo $SERVER_PID > logs/server.pid
    else
        print_error "No se pudo iniciar el servidor"
        exit 1
    fi
else
    print_success "El servidor ya está ejecutándose"
fi

print_step "8. Ejecutando pruebas del sistema de autenticación..."

# Ejecutar pruebas del sistema
python test_auth_system.py

print_success "Pruebas de autenticación completadas"

print_step "9. Configuración finalizada"

echo ""
echo "🎉 Sistema de autenticación configurado correctamente"
echo ""
echo "📝 Credenciales de administrador:"
echo "   Email: admin@papyrus.com.co"
echo "   Contraseña: Admin2025!"
echo ""
echo "🌐 URLs disponibles:"
echo "   - Login: http://localhost:8000/auth/login"
echo "   - Registro: http://localhost:8000/auth/register"
echo "   - Recuperar contraseña: http://localhost:8000/auth/forgot-password"
echo "   - Dashboard: http://localhost:8000/dashboard"
echo ""
echo "📧 Sistema de Emails:"
echo "   - Configurado para envío real de emails"
echo "   - Servidor SMTP: taylor.mxrouting.net:587"
echo "   - Email: guia@papyrus.com.co"
echo "   - En modo desarrollo, los emails se simulan"
echo ""
echo "🔧 Comandos útiles:"
echo "   - Detener servidor: kill \$(cat logs/server.pid)"
echo "   - Ver logs: tail -f logs/server.log"
echo "   - Probar emails: python test_email_system.py"
echo "   - Probar auth: python test_auth_system.py"
echo ""
echo "⚠️  Notas importantes:"
echo "   - Los emails de recuperación de contraseña funcionan correctamente"
echo "   - El sistema está configurado para producción"
echo "   - Revisa los logs si hay problemas"
echo ""
print_success "¡Configuración completada exitosamente!"
