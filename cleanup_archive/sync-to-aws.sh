#!/bin/bash

# 🚀 SCRIPT DE SINCRONIZACIÓN LOCAL → AWS
# Paquetes El Club v3.1

# Configuración
LOCAL_PATH="/home/stk/Insync/dispapyrussas@gmail.com/Google Drive/PAPYRUS/EL CLUB/SERVICIO DE PAQUETERIA/Paqueteria v3.1/code"
AWS_HOST="18.214.124.14"
AWS_PATH="/home/ubuntu/Paquetes"
SSH_KEY="~/.ssh/PAPYRUS.pem"
BACKUP_NAME="backup-$(date +%Y%m%d_%H%M%S)"

echo "🚀 ========================================"
echo "🚀 SINCRONIZACIÓN LOCAL → AWS"
echo "🚀 PAQUETES EL CLUB v3.1"
echo "🚀 ========================================"
echo ""

# Verificar que existe el directorio local
if [ ! -d "$LOCAL_PATH" ]; then
    echo "❌ Error: No se encuentra el directorio local: $LOCAL_PATH"
    exit 1
fi

echo "📁 Directorio local: $LOCAL_PATH"
echo "🌐 Servidor AWS: $AWS_HOST"
echo "📂 Directorio AWS: $AWS_PATH"
echo ""

# Preguntar qué tipo de sincronización hacer
echo "🔧 ¿Qué tipo de sincronización quieres hacer?"
echo "1) Sincronización completa (todo el código)"
echo "2) Sincronización selectiva (archivos específicos)"
echo "3) Solo configuración (.env, docker-compose.yml)"
echo "4) Solo plantillas HTML"
echo "5) Solo código Python"
echo "6) Solo archivos estáticos (CSS, JS, imágenes)"
read -p "Selecciona una opción (1-6): " SYNC_TYPE

echo ""

case $SYNC_TYPE in
    1)
        echo "🔄 SINCRONIZACIÓN COMPLETA"
        echo "=================================="
        
        # Crear backup en AWS
        echo "📦 Creando backup en AWS..."
        ssh -i $SSH_KEY ubuntu@$AWS_HOST "cd $AWS_PATH && tar -czf $BACKUP_NAME.tar.gz . 2>/dev/null && echo '✅ Backup creado: $BACKUP_NAME.tar.gz'"
        
        # Crear tarball local
        echo "📦 Creando tarball del código local..."
        cd "$LOCAL_PATH/.."
        tar -czf app-code.tar.gz code/ --exclude='__pycache__' --exclude='*.pyc' --exclude='.git'
        
        # Transferir a AWS
        echo "📤 Transfiriendo código a AWS..."
        scp -i $SSH_KEY app-code.tar.gz ubuntu@$AWS_HOST:$AWS_PATH/
        
        # Extraer en AWS
        echo "📂 Extrayendo código en AWS..."
        ssh -i $SSH_KEY ubuntu@$AWS_HOST "cd $AWS_PATH && tar -xzf app-code.tar.gz --strip-components=1 && rm app-code.tar.gz"
        
        # Limpiar archivo local
        rm app-code.tar.gz
        
        # Reiniciar contenedores
        echo "🐳 Reiniciando contenedores..."
        ssh -i $SSH_KEY ubuntu@$AWS_HOST "cd $AWS_PATH && docker-compose down && docker-compose up -d --build"
        ;;
        
    2)
        echo "🔄 SINCRONIZACIÓN SELECTIVA"
        echo "============================="
        
        echo "📝 Ingresa los archivos/directorios a sincronizar (separados por espacios):"
        echo "Ejemplo: src/main.py templates/login.html static/css/style.css"
        read -p "Archivos: " FILES_TO_SYNC
        
        for file in $FILES_TO_SYNC; do
            if [ -f "$LOCAL_PATH/$file" ] || [ -d "$LOCAL_PATH/$file" ]; then
                echo "📤 Transfiriendo: $file"
                scp -i $SSH_KEY -r "$LOCAL_PATH/$file" ubuntu@$AWS_HOST:$AWS_PATH/$(dirname "$file")/
            else
                echo "⚠️  Archivo no encontrado: $file"
            fi
        done
        
        # Reiniciar solo la aplicación
        echo "🔄 Reiniciando aplicación..."
        ssh -i $SSH_KEY ubuntu@$AWS_HOST "docker restart paqueteria_v31_app"
        ;;
        
    3)
        echo "🔄 SINCRONIZACIÓN DE CONFIGURACIÓN"
        echo "=================================="
        
        echo "📤 Transfiriendo archivos de configuración..."
        scp -i $SSH_KEY "$LOCAL_PATH/.env" ubuntu@$AWS_HOST:$AWS_PATH/
        scp -i $SSH_KEY "$LOCAL_PATH/docker-compose.yml" ubuntu@$AWS_HOST:$AWS_PATH/
        scp -i $SSH_KEY "$LOCAL_PATH/Dockerfile" ubuntu@$AWS_HOST:$AWS_PATH/
        
        echo "🔄 Reiniciando contenedores..."
        ssh -i $SSH_KEY ubuntu@$AWS_HOST "cd $AWS_PATH && docker-compose down && docker-compose up -d"
        ;;
        
    4)
        echo "🔄 SINCRONIZACIÓN DE PLANTILLAS HTML"
        echo "===================================="
        
        echo "📤 Transfiriendo plantillas..."
        scp -i $SSH_KEY -r "$LOCAL_PATH/templates/" ubuntu@$AWS_HOST:$AWS_PATH/
        
        echo "🔄 Reiniciando aplicación..."
        ssh -i $SSH_KEY ubuntu@$AWS_HOST "docker restart paqueteria_v31_app"
        ;;
        
    5)
        echo "🔄 SINCRONIZACIÓN DE CÓDIGO PYTHON"
        echo "==================================="
        
        echo "📤 Transfiriendo código Python..."
        scp -i $SSH_KEY -r "$LOCAL_PATH/src/" ubuntu@$AWS_HOST:$AWS_PATH/
        
        echo "🔄 Reiniciando aplicación..."
        ssh -i $SSH_KEY ubuntu@$AWS_HOST "docker restart paqueteria_v31_app"
        ;;
        
    6)
        echo "🔄 SINCRONIZACIÓN DE ARCHIVOS ESTÁTICOS"
        echo "======================================="
        
        echo "📤 Transfiriendo archivos estáticos..."
        scp -i $SSH_KEY -r "$LOCAL_PATH/static/" ubuntu@$AWS_HOST:$AWS_PATH/
        scp -i $SSH_KEY -r "$LOCAL_PATH/assets/" ubuntu@$AWS_HOST:$AWS_PATH/
        
        echo "🔄 Reiniciando Nginx..."
        ssh -i $SSH_KEY ubuntu@$AWS_HOST "docker restart paqueteria_v31_nginx"
        ;;
        
    *)
        echo "❌ Opción no válida"
        exit 1
        ;;
esac

echo ""
echo "✅ SINCRONIZACIÓN COMPLETADA"
echo "============================="

# Verificar estado de los contenedores
echo "🔍 Verificando estado de los contenedores..."
ssh -i $SSH_KEY ubuntu@$AWS_HOST "cd $AWS_PATH && docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'"

echo ""
echo "🌐 URLs de la aplicación:"
echo "🔗 Aplicación: https://guia.papyrus.com.co"
echo "🔗 Health Check: https://guia.papyrus.com.co/health"
echo "🔗 Login: https://guia.papyrus.com.co/login"

echo ""
echo "📋 Próximos pasos:"
echo "1. Verificar que la aplicación funciona correctamente"
echo "2. Revisar logs si hay errores: docker logs paqueteria_v31_app"
echo "3. Probar funcionalidades críticas"

echo ""
echo "🎉 ¡Sincronización completada exitosamente!"
