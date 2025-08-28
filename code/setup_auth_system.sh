#!/bin/bash
# ========================================
# PAQUETES EL CLUB v3.1 - Setup del Sistema de Autenticación
# ========================================

set -e

echo "🚀 Configurando sistema de autenticación..."

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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

# Verificar que estamos en el directorio correcto
if [ ! -f "src/main.py" ]; then
    print_error "Este script debe ejecutarse desde el directorio 'code'"
    exit 1
fi

print_status "Verificando estructura del proyecto..."

# Verificar que existan los archivos necesarios
required_files=(
    "src/main.py"
    "src/routers/auth.py"
    "src/models/user.py"
    "src/schemas/auth.py"
    "src/dependencies.py"
    "src/config.py"
)

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        print_error "Archivo requerido no encontrado: $file"
        exit 1
    fi
done

print_success "Estructura del proyecto verificada"

# Crear directorio de logs si no existe
print_status "Creando directorio de logs..."
mkdir -p logs
print_success "Directorio de logs creado"

# Verificar si Docker está ejecutándose
print_status "Verificando estado de Docker..."
if ! docker info > /dev/null 2>&1; then
    print_warning "Docker no está ejecutándose. Iniciando servicios..."
    
    # Intentar iniciar los servicios
    if [ -f "docker-compose.yml" ]; then
        print_status "Iniciando servicios con Docker Compose..."
        docker-compose up -d postgres redis
        
        # Esperar a que PostgreSQL esté listo
        print_status "Esperando a que PostgreSQL esté listo..."
        sleep 10
    else
        print_error "No se encontró docker-compose.yml"
        exit 1
    fi
else
    print_success "Docker está ejecutándose"
fi

# Crear usuario administrador
print_status "Creando usuario administrador..."
cd src
python scripts/create_admin_user.py
cd ..

print_success "Usuario administrador creado"

# Verificar que el servidor esté ejecutándose
print_status "Verificando que el servidor esté ejecutándose..."
if ! curl -s http://localhost:8000/health > /dev/null; then
    print_warning "El servidor no está ejecutándose en el puerto 8000"
    print_status "Iniciando servidor en segundo plano..."
    
    # Iniciar servidor en segundo plano
    nohup python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload > logs/server.log 2>&1 &
    SERVER_PID=$!
    
    # Esperar a que el servidor esté listo
    print_status "Esperando a que el servidor esté listo..."
    sleep 5
    
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

# Ejecutar pruebas del sistema
print_status "Ejecutando pruebas del sistema de autenticación..."
python test_auth_system.py

print_success "Configuración completada"
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
echo "📋 Para detener el servidor:"
echo "   kill \$(cat logs/server.pid)"
echo ""
echo "📋 Para ver logs del servidor:"
echo "   tail -f logs/server.log"
