#!/bin/bash

# Script para configurar la estructura de directorios del proyecto PAQUETERIA v3.1

echo "🚀 Configurando estructura de directorios para PAQUETERIA v3.1..."

# Crear directorios principales
mkdir -p uploads
mkdir -p logs/app
mkdir -p logs/nginx
mkdir -p logs/postgres
mkdir -p database/init
mkdir -p database/backups
mkdir -p database/migrations
mkdir -p scripts
mkdir -p tests
mkdir -p docs
mkdir -p monitoring
mkdir -p ssl

# Crear archivos de configuración
touch .env.example
touch docker-compose.override.yml

# Crear archivos de log
touch logs/app/app.log
touch logs/nginx/access.log
touch logs/nginx/error.log
touch logs/postgres/postgres.log

# Crear archivos de documentación
touch docs/README.md
touch docs/DEPLOYMENT.md
touch docs/API.md

# Crear scripts útiles
touch scripts/backup.sh
touch scripts/restore.sh
touch scripts/deploy.sh
touch scripts/health-check.sh

# Crear archivos de test
touch tests/__init__.py
touch tests/test_api.py
touch tests/test_database.py

# Crear archivos de monitoreo
touch monitoring/prometheus.yml
touch monitoring/grafana/dashboards/dashboard.json

# Dar permisos de ejecución a scripts
chmod +x scripts/*.sh

echo "✅ Estructura de directorios creada exitosamente!"
echo ""
echo "📁 Estructura creada:"
echo "├── uploads/           # Archivos subidos por usuarios"
echo "├── logs/              # Logs del sistema"
echo "├── database/          # Base de datos y migraciones"
echo "├── scripts/           # Scripts de automatización"
echo "├── tests/             # Tests automatizados"
echo "├── docs/              # Documentación"
echo "├── monitoring/        # Configuración de monitoreo"
echo "└── ssl/               # Certificados SSL"
echo ""
echo "🎯 Próximos pasos:"
echo "1. Copiar .env.example y configurar variables"
echo "2. Ejecutar: docker-compose up -d"
echo "3. Verificar que todo funcione correctamente"
