#!/bin/bash
# ========================================
# PAQUETES EL CLUB v3.1 - Detener Servicios
# ========================================

echo "🛑 Deteniendo servicios de PAQUETES EL CLUB v3.1..."

# Detener servicios
docker-compose down

echo "✅ Servicios detenidos correctamente!"
