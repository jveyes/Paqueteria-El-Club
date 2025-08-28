#!/bin/bash

# 🚀 SCRIPT DE SINCRONIZACIÓN GITHUB ↔ AWS
# Paquetes El Club v3.1

# Configuración
LOCAL_PATH="/home/stk/Insync/dispapyrussas@gmail.com/Google Drive/PAPYRUS/EL CLUB/SERVICIO DE PAQUETERIA/Paqueteria v3.1"
AWS_HOST="18.214.124.14"
AWS_PATH="/home/ubuntu/Paquetes"
SSH_KEY="~/.ssh/PAPYRUS.pem"
GITHUB_REPO="https://github.com/TU_USUARIO/paquetes-el-club-v3.1.git"

echo "🚀 ========================================"
echo "🚀 SINCRONIZACIÓN GITHUB ↔ AWS"
echo "🚀 PAQUETES EL CLUB v3.1"
echo "🚀 ========================================"
echo ""

# Verificar que existe el directorio local
if [ ! -d "$LOCAL_PATH" ]; then
    echo "❌ Error: No se encuentra el directorio local: $LOCAL_PATH"
    exit 1
fi

cd "$LOCAL_PATH"

# Verificar si es un repositorio Git
if [ ! -d ".git" ]; then
    echo "⚠️  No es un repositorio Git. ¿Quieres inicializarlo?"
    read -p "¿Inicializar repositorio Git? (y/n): " INIT_GIT
    
    if [ "$INIT_GIT" = "y" ] || [ "$INIT_GIT" = "Y" ]; then
        echo "🔧 Inicializando repositorio Git..."
        git init
        
        # Crear .gitignore si no existe
        if [ ! -f ".gitignore" ]; then
            echo "📝 Creando .gitignore..."
            cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Environment variables
.env
.env.local
.env.production
.env.staging

# Docker
.dockerignore

# Logs
logs/
*.log

# Database
*.db
*.sqlite3

# SSL Certificates
ssl/
*.pem
*.key
*.crt

# Uploads
uploads/
!uploads/.gitkeep

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# AWS
*.pem
backup-*.tar.gz

# Temporary files
*.tmp
*.temp
EOF
        fi
        
        echo "✅ Repositorio Git inicializado"
    else
        echo "❌ Se requiere un repositorio Git para continuar"
        exit 1
    fi
fi

# Menú principal
echo "🔧 ¿Qué operación quieres realizar?"
echo "1) 📤 Subir cambios a GitHub (push)"
echo "2) 📥 Bajar cambios desde GitHub (pull)"
echo "3) 🔄 Sincronización completa (push + pull en AWS)"
echo "4) 🚀 Deploy automático (push + pull + restart en AWS)"
echo "5) 📋 Ver estado del repositorio"
echo "6) 🔧 Configurar repositorio remoto"
read -p "Selecciona una opción (1-6): " OPERATION

echo ""

case $OPERATION in
    1)
        echo "📤 SUBIENDO CAMBIOS A GITHUB"
        echo "============================="
        
        # Verificar estado del repositorio
        echo "📋 Estado actual del repositorio:"
        git status --porcelain
        
        if [ -z "$(git status --porcelain)" ]; then
            echo "✅ No hay cambios para subir"
            exit 0
        fi
        
        # Preguntar por el mensaje de commit
        echo ""
        echo "💬 ¿Qué tipo de cambio es?"
        echo "1) ✨ Nueva funcionalidad (feat)"
        echo "2) 🐛 Corrección de bug (fix)"
        echo "3) 📝 Documentación (docs)"
        echo "4) 🎨 Mejora de código (style)"
        echo "5) ♻️  Refactorización (refactor)"
        echo "6) ⚡ Mejora de rendimiento (perf)"
        echo "7) 🧪 Test (test)"
        echo "8) 🔧 Configuración (chore)"
        read -p "Selecciona el tipo (1-8): " COMMIT_TYPE
        
        case $COMMIT_TYPE in
            1) TYPE="feat";;
            2) TYPE="fix";;
            3) TYPE="docs";;
            4) TYPE="style";;
            5) TYPE="refactor";;
            6) TYPE="perf";;
            7) TYPE="test";;
            8) TYPE="chore";;
            *) TYPE="feat";;
        esac
        
        read -p "📝 Descripción del cambio: " DESCRIPTION
        
        # Crear commit
        echo "💾 Creando commit..."
        git add .
        git commit -m "✨ $TYPE: $DESCRIPTION"
        
        # Preguntar por la rama
        echo ""
        echo "🌿 ¿A qué rama quieres hacer push?"
        echo "1) main (producción)"
        echo "2) develop (desarrollo)"
        echo "3) Nueva rama"
        read -p "Selecciona opción (1-3): " BRANCH_OPTION
        
        case $BRANCH_OPTION in
            1)
                BRANCH="main"
                ;;
            2)
                BRANCH="develop"
                ;;
            3)
                read -p "📝 Nombre de la nueva rama: " NEW_BRANCH
                BRANCH="$NEW_BRANCH"
                git checkout -b "$BRANCH"
                ;;
            *)
                BRANCH="develop"
                ;;
        esac
        
        # Hacer push
        echo "📤 Haciendo push a GitHub..."
        if git push origin "$BRANCH"; then
            echo "✅ Push exitoso a rama: $BRANCH"
        else
            echo "❌ Error en el push. ¿Quieres configurar el remoto?"
            read -p "¿Configurar remoto? (y/n): " SETUP_REMOTE
            if [ "$SETUP_REMOTE" = "y" ] || [ "$SETUP_REMOTE" = "Y" ]; then
                read -p "🔗 URL del repositorio GitHub: " GITHUB_URL
                git remote add origin "$GITHUB_URL"
                git push -u origin "$BRANCH"
            fi
        fi
        ;;
        
    2)
        echo "📥 BAJANDO CAMBIOS DESDE GITHUB"
        echo "==============================="
        
        # Verificar si hay cambios locales
        if [ -n "$(git status --porcelain)" ]; then
            echo "⚠️  Tienes cambios locales sin commitear"
            echo "📋 Cambios pendientes:"
            git status --porcelain
            echo ""
            read -p "¿Quieres hacer stash de los cambios? (y/n): " STASH_CHANGES
            if [ "$STASH_CHANGES" = "y" ] || [ "$STASH_CHANGES" = "Y" ]; then
                git stash
                echo "✅ Cambios guardados en stash"
            else
                echo "❌ No se pueden bajar cambios con cambios locales pendientes"
                exit 1
            fi
        fi
        
        # Preguntar por la rama
        echo ""
        echo "🌿 ¿De qué rama quieres hacer pull?"
        echo "1) main (producción)"
        echo "2) develop (desarrollo)"
        echo "3) Otra rama"
        read -p "Selecciona opción (1-3): " PULL_BRANCH_OPTION
        
        case $PULL_BRANCH_OPTION in
            1) PULL_BRANCH="main";;
            2) PULL_BRANCH="develop";;
            3)
                read -p "📝 Nombre de la rama: " PULL_BRANCH
                ;;
            *) PULL_BRANCH="develop";;
        esac
        
        # Cambiar a la rama
        git checkout "$PULL_BRANCH"
        
        # Hacer pull
        echo "📥 Haciendo pull desde GitHub..."
        if git pull origin "$PULL_BRANCH"; then
            echo "✅ Pull exitoso desde rama: $PULL_BRANCH"
            
            # Restaurar stash si existe
            if [ "$STASH_CHANGES" = "y" ] || [ "$STASH_CHANGES" = "Y" ]; then
                echo "🔄 Restaurando cambios del stash..."
                git stash pop
            fi
        else
            echo "❌ Error en el pull"
        fi
        ;;
        
    3)
        echo "🔄 SINCRONIZACIÓN COMPLETA"
        echo "=========================="
        
        # Primero hacer push
        echo "📤 Paso 1: Subiendo cambios a GitHub..."
        git add .
        read -p "📝 Mensaje de commit: " COMMIT_MSG
        git commit -m "$COMMIT_MSG"
        
        read -p "🌿 Rama para push (main/develop): " SYNC_BRANCH
        git push origin "$SYNC_BRANCH"
        
        # Luego hacer pull en AWS
        echo "📥 Paso 2: Bajando cambios en AWS..."
        ssh -i $SSH_KEY ubuntu@$AWS_HOST "cd $AWS_PATH && git fetch origin && git reset --hard origin/$SYNC_BRANCH"
        
        echo "✅ Sincronización completa realizada"
        ;;
        
    4)
        echo "🚀 DEPLOY AUTOMÁTICO"
        echo "===================="
        
        # Hacer push
        echo "📤 Paso 1: Subiendo cambios a GitHub..."
        git add .
        read -p "📝 Mensaje de commit: " DEPLOY_COMMIT_MSG
        git commit -m "$DEPLOY_COMMIT_MSG"
        
        read -p "🌿 Rama para deploy (main/develop): " DEPLOY_BRANCH
        git push origin "$DEPLOY_BRANCH"
        
        # Deploy en AWS
        echo "🚀 Paso 2: Deployando en AWS..."
        ssh -i $SSH_KEY ubuntu@$AWS_HOST "cd $AWS_PATH && git fetch origin && git reset --hard origin/$DEPLOY_BRANCH && docker-compose down && docker-compose up -d --build"
        
        echo "✅ Deploy automático completado"
        echo "🌐 Verificar en: https://guia.papyrus.com.co"
        ;;
        
    5)
        echo "📋 ESTADO DEL REPOSITORIO"
        echo "========================="
        
        echo "🌿 Rama actual:"
        git branch --show-current
        
        echo ""
        echo "📤 Estado de commits:"
        git status
        
        echo ""
        echo "📋 Últimos commits:"
        git log --oneline -5
        
        echo ""
        echo "🌐 Remotos configurados:"
        git remote -v
        
        echo ""
        echo "📊 Diferencias con remoto:"
        git status --porcelain
        ;;
        
    6)
        echo "🔧 CONFIGURACIÓN DE REPOSITORIO REMOTO"
        echo "====================================="
        
        echo "🌐 Remotos actuales:"
        git remote -v
        
        echo ""
        echo "🔧 Opciones:"
        echo "1) Agregar nuevo remoto"
        echo "2) Cambiar URL del remoto origin"
        echo "3) Eliminar remoto"
        read -p "Selecciona opción (1-3): " REMOTE_OPTION
        
        case $REMOTE_OPTION in
            1)
                read -p "📝 Nombre del remoto: " REMOTE_NAME
                read -p "🔗 URL del repositorio: " REMOTE_URL
                git remote add "$REMOTE_NAME" "$REMOTE_URL"
                echo "✅ Remoto agregado: $REMOTE_NAME"
                ;;
            2)
                read -p "🔗 Nueva URL del repositorio: " NEW_URL
                git remote set-url origin "$NEW_URL"
                echo "✅ URL del remoto origin actualizada"
                ;;
            3)
                read -p "📝 Nombre del remoto a eliminar: " REMOTE_TO_DELETE
                git remote remove "$REMOTE_TO_DELETE"
                echo "✅ Remoto eliminado: $REMOTE_TO_DELETE"
                ;;
        esac
        ;;
        
    *)
        echo "❌ Opción no válida"
        exit 1
        ;;
esac

echo ""
echo "🎉 Operación completada exitosamente!"
echo ""
echo "📋 Próximos pasos sugeridos:"
case $OPERATION in
    1|3|4)
        echo "1. Verificar que los cambios están en GitHub"
        echo "2. Crear Pull Request si es necesario"
        echo "3. Verificar que el deploy funciona correctamente"
        ;;
    2)
        echo "1. Revisar los cambios descargados"
        echo "2. Resolver conflictos si los hay"
        echo "3. Probar que todo funciona correctamente"
        ;;
esac

echo ""
echo "🌐 URLs útiles:"
echo "🔗 Aplicación: https://guia.papyrus.com.co"
echo "🔗 GitHub: https://github.com/TU_USUARIO/paquetes-el-club-v3.1"
