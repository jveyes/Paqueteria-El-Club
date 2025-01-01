#!/bin/bash

# ========================================
# PAQUETERIA v3.1 - Ejecutor de Validación Automática
# ========================================

echo "🛡️  SISTEMA DE VALIDACIÓN AUTOMÁTICA"
echo "======================================"
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

# Función para mostrar información
show_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Función para mostrar advertencia
show_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Función para mostrar error
show_error() {
    echo -e "${RED}💥 $1${NC}"
}

# Función para mostrar éxito
show_success() {
    echo -e "${GREEN}🎉 $1${NC}"
}

# Verificar que estamos en el directorio correcto
if [ ! -f "validate-all.py" ]; then
    show_error "Este script debe ejecutarse desde el directorio raíz del proyecto"
    show_info "Directorio actual: $(pwd)"
    show_info "Archivos esperados: validate-all.py, validate-model-sync.py, etc."
    exit 1
fi

# Verificar que Python esté disponible
if ! command -v python3 &> /dev/null; then
    show_error "Python3 no está disponible"
    show_info "Instala Python3 o verifica que esté en el PATH"
    exit 1
fi

# Verificar que Docker esté disponible
if ! command -v docker &> /dev/null; then
    show_warning "Docker no está disponible"
    show_info "Algunas validaciones pueden fallar"
fi

# Verificar que los scripts de validación existan
required_scripts=(
    "validate-all.py"
    "validate-model-sync.py"
    "validate-migrations.py"
    "advanced-health-check.py"
)

missing_scripts=()
for script in "${required_scripts[@]}"; do
    if [ ! -f "$script" ]; then
        missing_scripts+=("$script")
    fi
done

if [ ${#missing_scripts[@]} -gt 0 ]; then
    show_error "Scripts de validación faltantes:"
    for script in "${missing_scripts[@]}"; do
        echo "   - $script"
    done
    exit 1
fi

show_success "Todos los scripts de validación están presentes"

# Función para ejecutar validación individual
run_single_validator() {
    local script_name=$1
    local description=$2
    
    echo ""
    show_info "Ejecutando: $description"
    echo "Script: $script_name"
    echo "----------------------------------------"
    
    if python3 "$script_name"; then
        show_success "$description completado exitosamente"
        return 0
    else
        show_error "$description falló"
        return 1
    fi
}

# Función para ejecutar validación completa
run_complete_validation() {
    echo ""
    show_info "Ejecutando validación completa del sistema..."
    echo "=================================================="
    
    if python3 validate-all.py; then
        show_success "Validación completa exitosa"
        return 0
    else
        show_error "Validación completa falló"
        return 1
    fi
}

# Función para mostrar menú
show_menu() {
    echo ""
    echo "📋 MENÚ DE VALIDACIÓN:"
    echo "1. Validación de Sincronización de Modelos"
    echo "2. Validación de Migraciones Alembic"
    echo "3. Health Check Avanzado"
    echo "4. Validación Completa del Sistema"
    echo "5. Ejecutar todas las validaciones en secuencia"
    echo "6. Salir"
    echo ""
    read -p "Selecciona una opción (1-6): " choice
}

# Función para ejecutar opción del menú
execute_option() {
    case $1 in
        1)
            run_single_validator "validate-model-sync.py" "Validación de Sincronización de Modelos"
            ;;
        2)
            run_single_validator "validate-migrations.py" "Validación de Migraciones Alembic"
            ;;
        3)
            run_single_validator "advanced-health-check.py" "Health Check Avanzado"
            ;;
        4)
            run_complete_validation
            ;;
        5)
            run_all_validations
            ;;
        6)
            show_info "Saliendo..."
            exit 0
            ;;
        *)
            show_error "Opción inválida: $1"
            ;;
    esac
}

# Función para ejecutar todas las validaciones en secuencia
run_all_validations() {
    echo ""
    show_info "Ejecutando todas las validaciones en secuencia..."
    echo "=================================================="
    
    local success_count=0
    local total_count=4
    
    # 1. Validación de Modelos
    if run_single_validator "validate-model-sync.py" "Validación de Sincronización de Modelos"; then
        ((success_count++))
    fi
    
    # 2. Validación de Migraciones
    if run_single_validator "validate-migrations.py" "Validación de Migraciones Alembic"; then
        ((success_count++))
    fi
    
    # 3. Health Check
    if run_single_validator "advanced-health-check.py" "Health Check Avanzado"; then
        ((success_count++))
    fi
    
    # 4. Validación Completa
    if run_complete_validation; then
        ((success_count++))
    fi
    
    # Resumen final
    echo ""
    echo "=================================================="
    echo "📊 RESUMEN FINAL DE VALIDACIONES"
    echo "=================================================="
    echo "Total de validaciones: $total_count"
    echo "Validaciones exitosas: $success_count"
    echo "Validaciones fallidas: $((total_count - success_count))"
    
    if [ $success_count -eq $total_count ]; then
        show_success "¡TODAS LAS VALIDACIONES EXITOSAS!"
    else
        show_warning "Algunas validaciones fallaron. Revisa los resultados arriba."
    fi
}

# Función para modo automático
run_automatic_mode() {
    echo ""
    show_info "Modo automático activado"
    show_info "Ejecutando validación completa..."
    
    if run_complete_validation; then
        show_success "Sistema validado correctamente"
        exit 0
    else
        show_error "Sistema tiene problemas que requieren atención"
        exit 1
    fi
}

# Función para modo interactivo
run_interactive_mode() {
    while true; do
        show_menu
        execute_option "$choice"
        
        echo ""
        read -p "¿Continuar con más validaciones? (s/n): " continue_choice
        if [[ ! "$continue_choice" =~ ^[Ss]$ ]]; then
            break
        fi
    done
}

# Función principal
main() {
    echo "🛡️  SISTEMA DE VALIDACIÓN AUTOMÁTICA - PAQUETERIA v3.1"
    echo "========================================================"
    echo ""
    show_info "Este sistema te ayudará a prevenir problemas como:"
    echo "   - Columnas faltantes en la base de datos"
    echo "   - Migraciones no aplicadas"
    echo "   - Servicios Docker no funcionando"
    echo "   - Problemas de configuración"
    echo ""
    
    # Verificar argumentos de línea de comandos
    if [ "$1" = "--auto" ] || [ "$1" = "-a" ]; then
        run_automatic_mode
    elif [ "$1" = "--interactive" ] || [ "$1" = "-i" ]; then
        run_interactive_mode
    elif [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
        echo "Uso: $0 [OPCIÓN]"
        echo ""
        echo "Opciones:"
        echo "  --auto, -a        Ejecutar validación automática y salir"
        echo "  --interactive, -i Ejecutar en modo interactivo"
        echo "  --help, -h        Mostrar esta ayuda"
        echo ""
        echo "Sin opciones: Modo interactivo por defecto"
        exit 0
    else
        # Modo por defecto: preguntar al usuario
        echo "Selecciona el modo de ejecución:"
        echo "1. Automático (ejecuta y sale)"
        echo "2. Interactivo (menú de opciones)"
        echo ""
        read -p "Selecciona modo (1-2): " mode_choice
        
        case $mode_choice in
            1)
                run_automatic_mode
                ;;
            2)
                run_interactive_mode
                ;;
            *)
                show_info "Modo no válido, usando modo interactivo por defecto"
                run_interactive_mode
                ;;
        esac
    fi
}

# Ejecutar función principal
main "$@"
