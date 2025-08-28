#!/bin/bash

# ========================================
# PAQUETES EL CLUB v3.0 - Script de Configuración
# ========================================

echo "🚀 Configurando PAQUETES EL CLUB v3.0..."

# Crear directorios necesarios
echo "📁 Creando directorios..."
mkdir -p uploads logs static ssl
mkdir -p monitoring/grafana/dashboards
mkdir -p monitoring/grafana/datasources
mkdir -p database/init

# Crear archivo de configuración de Prometheus
echo "📊 Configurando Prometheus..."
cat > monitoring/prometheus.yml << EOF
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  # - "first_rules.yml"
  # - "second_rules.yml"

scrape_configs:
  - job_name: 'paqueteria-app'
    static_configs:
      - targets: ['app:8000']
    metrics_path: '/metrics'
    scrape_interval: 5s

  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
EOF

# Crear configuración de Grafana
echo "📈 Configurando Grafana..."
cat > monitoring/grafana/datasources/prometheus.yml << EOF
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
EOF

echo "✅ Configuración completada!"
echo "📝 Para continuar:"
echo "   1. Copia env.example a .env y ajusta las variables"
echo "   2. Ejecuta: docker-compose up -d"
echo "   3. Accede a: http://localhost"
