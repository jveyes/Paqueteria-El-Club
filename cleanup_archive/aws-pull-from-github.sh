#!/bin/bash

# 📥 SCRIPT PARA HACER PULL DESDE GITHUB EN AWS
# Paquetes El Club v3.1

# Configuración
AWS_HOST="18.214.124.14"
AWS_PATH="/home/ubuntu/Paquetes"
SSH_KEY="~/.ssh/PAPYRUS.pem"

echo "📥 ========================================"
echo "📥 PULL DESDE GITHUB EN AWS"
echo "📥 PAQUETES EL CLUB v3.1"
echo "📥 ========================================"
echo ""

# Verificar conexión SSH
echo "🔍 Verificando conexión SSH..."
if ! ssh -i $SSH_KEY -o ConnectTimeout=10 ubuntu@$AWS_HOST "echo '✅ Conexión SSH exitosa'" 2>/dev/null; then
    echo "❌ Error: No se puede conectar al servidor AWS"
    echo "🔧 Verificar:"
    echo "   - Clave SSH: $SSH_KEY"
    echo "   - IP del servidor: $AWS_HOST"
    echo "   - Usuario: ubuntu"
    exit 1
fi

# Menú de opciones
echo "🔧 ¿Qué operación quieres realizar en AWS?"
echo "1) 📥 Pull desde GitHub (sin reiniciar contenedores)"
echo "2) 🔄 Pull + Reiniciar contenedores"
echo "3) 🚀 Pull + Rebuild completo (docker-compose down/up)"
echo "4) 📋 Ver estado del repositorio en AWS"
echo "5) 🔍 Ver logs de los contenedores"
echo "6) 🧹 Limpiar y resetear completamente"
read -p "Selecciona una opción (1-6): " AWS_OPERATION

echo ""

case $AWS_OPERATION in
    1)
        echo "📥 PULL DESDE GITHUB (SIN REINICIAR)"
        echo "===================================="
        
        # Preguntar por la rama
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
        
        echo "📥 Haciendo pull desde rama: $PULL_BRANCH"
        
        # Ejecutar pull en AWS
        ssh -i $SSH_KEY ubuntu@$AWS_HOST "cd $AWS_PATH && git fetch origin && git reset --hard origin/$PULL_BRANCH"
        
        if [ $? -eq 0 ]; then
            echo "✅ Pull exitoso desde rama: $PULL_BRANCH"
        else
            echo "❌ Error en el pull"
            exit 1
        fi
        ;;
        
    2)
        echo "🔄 PULL + REINICIAR CONTENEDORES"
        echo "================================"
        
        # Preguntar por la rama
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
        
        echo "📥 Haciendo pull desde rama: $PULL_BRANCH"
        
        # Ejecutar pull y reiniciar contenedores
        ssh -i $SSH_KEY ubuntu@$AWS_HOST "cd $AWS_PATH && git fetch origin && git reset --hard origin/$PULL_BRANCH && docker-compose restart"
        
        if [ $? -eq 0 ]; then
            echo "✅ Pull y reinicio completados"
        else
            echo "❌ Error en la operación"
            exit 1
        fi
        ;;
        
    3)
        echo "🚀 PULL + REBUILD COMPLETO"
        echo "==========================="
        
        # Preguntar por la rama
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
        
        echo "⚠️  ATENCIÓN: Esta operación detendrá todos los contenedores"
        read -p "¿Continuar? (y/n): " CONFIRM_REBUILD
        
        if [ "$CONFIRM_REBUILD" != "y" ] && [ "$CONFIRM_REBUILD" != "Y" ]; then
            echo "❌ Operación cancelada"
            exit 0
        fi
        
        echo "📥 Haciendo pull desde rama: $PULL_BRANCH"
        echo "🐳 Reconstruyendo contenedores..."
        
        # Ejecutar pull y rebuild completo
        ssh -i $SSH_KEY ubuntu@$AWS_HOST "cd $AWS_PATH && git fetch origin && git reset --hard origin/$PULL_BRANCH && docker-compose down && docker-compose up -d --build"
        
        if [ $? -eq 0 ]; then
            echo "✅ Pull y rebuild completados"
        else
            echo "❌ Error en la operación"
            exit 1
        fi
        ;;
        
    4)
        echo "📋 ESTADO DEL REPOSITORIO EN AWS"
        echo "================================"
        
        # Mostrar estado del repositorio
        ssh -i $SSH_KEY ubuntu@$AWS_HOST "cd $AWS_PATH && echo '🌿 Rama actual:' && git branch --show-current && echo '' && echo '📤 Estado:' && git status --porcelain && echo '' && echo '📋 Últimos commits:' && git log --oneline -5"
        ;;
        
    5)
        echo "🔍 LOGS DE LOS CONTENEDORES"
        echo "============================"
        
        # Menú de logs
        echo "🔍 ¿Qué logs quieres ver?"
        echo "1) 📱 Aplicación (app)"
        echo "2) 🌐 Nginx"
        echo "3) 🔴 Redis"
        echo "4) ⚡ Celery Worker"
        echo "5) 📊 Todos los contenedores"
        read -p "Selecciona una opción (1-5): " LOG_OPTION
        
        case $LOG_OPTION in
            1)
                echo "📱 Logs de la aplicación:"
                ssh -i $SSH_KEY ubuntu@$AWS_HOST "docker logs paqueteria_v31_app --tail 50"
                ;;
            2)
                echo "🌐 Logs de Nginx:"
                ssh -i $SSH_KEY ubuntu@$AWS_HOST "docker logs paqueteria_v31_nginx --tail 50"
                ;;
            3)
                echo "🔴 Logs de Redis:"
                ssh -i $SSH_KEY ubuntu@$AWS_HOST "docker logs paqueteria_v31_redis --tail 50"
                ;;
            4)
                echo "⚡ Logs de Celery Worker:"
                ssh -i $SSH_KEY ubuntu@$AWS_HOST "docker logs paqueteria_v31_celery_worker --tail 50"
                ;;
            5)
                echo "📊 Logs de todos los contenedores:"
                ssh -i $SSH_KEY ubuntu@$AWS_HOST "docker-compose logs --tail 20"
                ;;
            *)
                echo "❌ Opción no válida"
                exit 1
                ;;
        esac
        ;;
        
    6)
        echo "🧹 LIMPIEZA Y RESETEO COMPLETO"
        echo "=============================="
        
        echo "⚠️  ATENCIÓN: Esta operación es destructiva"
        echo "Se eliminarán:"
        echo "  - Todos los contenedores"
        echo "  - Imágenes Docker"
        echo "  - Volúmenes (excepto datos importantes)"
        echo "  - Código actual"
        echo ""
        read -p "¿Estás seguro? Escribe 'SI' para confirmar: " CONFIRM_CLEAN
        
        if [ "$CONFIRM_CLEAN" != "SI" ]; then
            echo "❌ Operación cancelada"
            exit 0
        fi
        
        echo "🧹 Limpiando completamente..."
        
        # Limpieza completa
        ssh -i $SSH_KEY ubuntu@$AWS_HOST "cd $AWS_PATH && docker-compose down -v && docker system prune -f && docker volume prune -f && git reset --hard HEAD && git clean -fd"
        
        if [ $? -eq 0 ]; then
            echo "✅ Limpieza completada"
            echo "🔄 Ahora puedes hacer pull desde la rama deseada"
        else
            echo "❌ Error en la limpieza"
            exit 1
        fi
        ;;
        
    *)
        echo "❌ Opción no válida"
        exit 1
        ;;
esac

echo ""
echo "🎉 Operación completada exitosamente!"

# Verificar estado final
if [ "$AWS_OPERATION" != "4" ] && [ "$AWS_OPERATION" != "5" ]; then
    echo ""
    echo "🔍 Verificando estado de los contenedores..."
    ssh -i $SSH_KEY ubuntu@$AWS_HOST "cd $AWS_PATH && docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'"
    
    echo ""
    echo "🌐 URLs de la aplicación:"
    echo "🔗 Aplicación: https://guia.papyrus.com.co"
    echo "🔗 Health Check: https://guia.papyrus.com.co/health"
    echo "🔗 Login: https://guia.papyrus.com.co/login"
fi

echo ""
echo "📋 Próximos pasos sugeridos:"
echo "1. Verificar que la aplicación funciona correctamente"
echo "2. Revisar logs si hay errores"
echo "3. Probar funcionalidades críticas"
