#!/bin/bash

# ========================================
# PAQUETES EL CLUB v3.1 - Reiniciar Servicios AWS
# ========================================
# Script para reiniciar todos los servicios en AWS

echo "🔄 Reiniciando servicios en AWS..."
echo "=================================="

# Configuración del servidor AWS
AWS_HOST="ec2-54-167-87-8.compute-1.amazonaws.com"
AWS_USER="ubuntu"
AWS_KEY="~/.ssh/papyrus.pem"

echo ""
echo "📋 Configuración:"
echo "   Host: $AWS_HOST"
echo "   Usuario: $AWS_USER"
echo "   Key: $AWS_KEY"

echo ""
echo "🛑 Deteniendo servicios en AWS..."

# Detener servicios
ssh -i $AWS_KEY $AWS_USER@$AWS_HOST << 'EOF'
cd /opt/paqueteria
echo "Deteniendo contenedores..."
docker-compose down
echo "Limpiando recursos..."
docker system prune -f
docker volume prune -f
echo "Servicios detenidos correctamente"
EOF

echo ""
echo "⏳ Esperando 5 segundos..."
sleep 5

echo ""
echo "🚀 Iniciando servicios en AWS..."

# Iniciar servicios
ssh -i $AWS_KEY $AWS_USER@$AWS_HOST << 'EOF'
cd /opt/paqueteria
echo "Iniciando contenedores..."
docker-compose up -d
echo "Esperando que los servicios estén listos..."
sleep 10
echo "Verificando estado de los contenedores..."
docker-compose ps
echo "Servicios iniciados correctamente"
EOF

echo ""
echo "✅ Reinicio de servicios AWS completado"
echo ""
echo "🌐 URLs de acceso:"
echo "   - Aplicación: https://paqueteria.papyrus.com.co"
echo "   - API: https://paqueteria.papyrus.com.co/api"
echo ""
echo "🔧 Para verificar logs:"
echo "   ssh -i ~/.ssh/papyrus.pem ubuntu@ec2-54-167-87-8.compute-1.amazonaws.com"
echo "   cd /opt/paqueteria && docker-compose logs -f"
