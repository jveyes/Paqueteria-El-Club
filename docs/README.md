# 📚 Documentación - Paquetes El Club v3.1

## 📋 Índice de Documentación

### 🚀 Guías de Despliegue
- [Guía de Despliegue General](deployment/DEPLOYMENT-GUIDE.md) - Instrucciones generales de despliegue
- [Guía de Despliegue AWS](deployment/AWS_DEPLOYMENT_GUIDE.md) - Despliegue específico en AWS

### ⚙️ Configuración
- [Configuración de Zona Horaria](configuration/TIMEZONE_CONFIGURATION.md) - Configuración de zona horaria Colombia

### 📊 Reportes y Análisis
- [Resumen de Organización](ORGANIZATION_SUMMARY.md) - Resumen de la organización del proyecto
- [Reporte de Análisis de Nginx](reports/nginx-analysis-report.md)
- [Estado Completo del Sistema](reports/complete-system-status.md)
- [Estado Final del Backend](reports/final-backend-status.md)
- [Reporte de Limpieza](reports/cleanup-report.md)
- [Prueba Integral](reports/comprehensive-test.md)
- [Reporte de Organización de Archivos](reports/file_organization_report.md)
- [Prueba de API](reports/api-test.md)
- [Reporte de Análisis del Backend](reports/backend-analysis-report.md)
- [Resumen Ejecutivo](reports/executive-summary.md)

## 🎯 Descripción del Proyecto

**Paquetes El Club v3.1** es una aplicación de gestión de paquetería desarrollada con FastAPI, PostgreSQL y Docker. El sistema permite el seguimiento de paquetes, gestión de clientes y envío de notificaciones por correo electrónico.

## 🏗️ Arquitectura

- **Backend**: FastAPI (Python)
- **Base de Datos**: PostgreSQL (AWS RDS)
- **Cache**: Redis
- **Web Server**: Nginx
- **Contenedores**: Docker & Docker Compose
- **Despliegue**: AWS Lightsail

## 🔧 Configuración Actual

- **Zona Horaria**: America/Bogota (UTC-5)
- **Base de Datos**: AWS RDS PostgreSQL (pública)
- **Puerto**: 8000 (local), 80 (AWS)
- **Modo**: Desarrollo con recarga automática

## 🚀 Inicio Rápido

### Desarrollo Local
```bash
# Iniciar servicios
./scripts/start-with-rds.sh

# Acceder a la aplicación
http://localhost:8000
```

### Despliegue AWS
```bash
# Conectar al servidor
ssh papyrus

# Desplegar servicios
docker-compose -f docker-compose.aws.yml up -d
```

## 📝 Notas Importantes

- La base de datos RDS está configurada como pública para desarrollo
- Todos los contenedores usan zona horaria Colombia
- Los scripts de prueba están disponibles en `scripts/`
- La documentación se organiza por categorías para fácil navegación
