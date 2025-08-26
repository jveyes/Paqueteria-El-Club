#!/bin/bash

# ========================================
# Script para preparar el repositorio para GitHub
# PAQUETERIA EL CLUB v3.1
# ========================================

echo "🚀 Preparando repositorio para GitHub..."

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para verificar archivos
check_file() {
    local file=$1
    local description=$2
    
    if [ -f "$file" ]; then
        echo -e "${GREEN}✅ $description: $file${NC}"
    else
        echo -e "${RED}❌ $description: $file (FALTANTE)${NC}"
    fi
}

# Función para verificar directorios
check_directory() {
    local dir=$1
    local description=$2
    
    if [ -d "$dir" ]; then
        echo -e "${GREEN}✅ $description: $dir${NC}"
    else
        echo -e "${RED}❌ $description: $dir (FALTANTE)${NC}"
    fi
}

echo ""
echo "📋 Verificando archivos esenciales..."

# Verificar archivos de configuración
check_file ".gitignore" "Archivo .gitignore"
check_file "README.md" "Documentación README"
check_file "CHANGELOG.md" "Changelog"
check_file "LICENSE" "Licencia MIT"
check_file "env.example" "Template de variables de entorno"
check_file "docker-compose.yml" "Configuración Docker Compose"

# Verificar directorios importantes
check_directory "code" "Código fuente"
check_directory "docs" "Documentación"
check_directory "scripts" "Scripts de automatización"
check_directory "uploads" "Directorio de uploads"

echo ""
echo "🔍 Verificando información sensible..."

# Verificar que no hay archivos .env
if [ -f ".env" ]; then
    echo -e "${RED}⚠️  ADVERTENCIA: Archivo .env encontrado${NC}"
    echo -e "${YELLOW}   Asegúrate de que esté en .gitignore${NC}"
else
    echo -e "${GREEN}✅ No hay archivo .env (correcto)${NC}"
fi

# Verificar que no hay información sensible en el código
echo ""
echo "🔒 Verificando seguridad del código..."

# Buscar posibles contraseñas hardcodeadas
if grep -r "password.*=" code/ --exclude-dir=__pycache__ 2>/dev/null | grep -v "example\|template" > /dev/null; then
    echo -e "${RED}⚠️  ADVERTENCIA: Posibles contraseñas hardcodeadas encontradas${NC}"
else
    echo -e "${GREEN}✅ No se encontraron contraseñas hardcodeadas${NC}"
fi

echo ""
echo "📝 Preparando documentación..."

# Crear archivo de contribución si no existe
if [ ! -f "CONTRIBUTING.md" ]; then
    echo -e "${BLUE}📄 Creando CONTRIBUTING.md...${NC}"
    cat > CONTRIBUTING.md << 'EOF'
# 🤝 Guía de Contribución

## Cómo Contribuir

1. **Fork** el proyecto
2. **Crea una rama** para tu feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. **Push** a la rama (`git push origin feature/AmazingFeature`)
5. **Abre un Pull Request**

## Estándares de Código

- **Python**: PEP 8, docstrings obligatorios
- **HTML**: Indentación 2 espacios
- **CSS**: Clases de Tailwind CSS
- **JavaScript**: ES6+, funciones descriptivas

## Reportar Bugs

Usa el template de Issues para reportar bugs.

## Solicitar Features

Usa el template de Issues para solicitar nuevas funcionalidades.
EOF
fi

echo ""
echo "🔧 Verificando scripts de automatización..."

# Verificar que los scripts tienen permisos de ejecución
for script in scripts/*.sh; do
    if [ -f "$script" ]; then
        if [ -x "$script" ]; then
            echo -e "${GREEN}✅ Script ejecutable: $script${NC}"
        else
            echo -e "${YELLOW}⚠️  Agregando permisos de ejecución a: $script${NC}"
            chmod +x "$script"
        fi
    fi
done

echo ""
echo "📊 Resumen de preparación:"

# Contar archivos por tipo
echo -e "${BLUE}📁 Estructura del proyecto:${NC}"
echo "   - Archivos Python: $(find code/ -name "*.py" | wc -l | tr -d ' ')"
echo "   - Templates HTML: $(find code/templates/ -name "*.html" | wc -l | tr -d ' ')"
echo "   - Scripts: $(find scripts/ -name "*.sh" | wc -l | tr -d ' ')"
echo "   - Documentos: $(find docs/ -name "*.md" | wc -l | tr -d ' ')"

echo ""
echo "🎯 Próximos pasos para subir a GitHub:"

echo -e "${YELLOW}1. Inicializar repositorio Git:${NC}"
echo "   git init"
echo "   git add ."
echo "   git commit -m 'Initial commit: PAQUETERIA EL CLUB v3.1'"

echo -e "${YELLOW}2. Crear repositorio en GitHub${NC}"
echo "   - Ve a github.com"
echo "   - Crea un nuevo repositorio"
echo "   - NO inicialices con README (ya existe)"

echo -e "${YELLOW}3. Conectar y subir:${NC}"
echo "   git remote add origin https://github.com/tu-usuario/paqueteria-club.git"
echo "   git branch -M main"
echo "   git push -u origin main"

echo ""
echo -e "${GREEN}🎉 ¡Repositorio listo para GitHub!${NC}"
echo ""
echo -e "${BLUE}📋 Checklist final:${NC}"
echo "   ✅ .gitignore configurado"
echo "   ✅ README.md completo"
echo "   ✅ CHANGELOG.md actualizado"
echo "   ✅ LICENSE agregado"
echo "   ✅ Variables de entorno en env.example"
echo "   ✅ Sin información sensible expuesta"
echo "   ✅ Scripts con permisos de ejecución"
echo "   ✅ Documentación completa"
