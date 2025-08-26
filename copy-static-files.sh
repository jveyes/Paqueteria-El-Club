#!/bin/bash

# Script para copiar archivos estáticos al contenedor
echo "Copiando archivos estáticos al contenedor..."

# Crear directorios en el contenedor
docker exec paqueteria_v31_app mkdir -p /app/static/images
docker exec paqueteria_v31_app mkdir -p /app/static/documents

# Copiar archivos
echo "Copiando imagen de Papyrus..."
docker cp code/static/images/papyrus-logo.png paqueteria_v31_app:/app/static/images/

echo "Copiando documentos..."
docker cp code/static/documents/. paqueteria_v31_app:/app/static/documents/

echo "Verificando archivos copiados..."
docker exec paqueteria_v31_app ls -la /app/static/images/
docker exec paqueteria_v31_app ls -la /app/static/documents/

echo "¡Archivos estáticos copiados exitosamente!"
