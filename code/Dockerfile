# ========================================
# PAQUETES EL CLUB v3.1 - Dockerfile de Producción
# ========================================
# Fecha: 25 de Agosto, 2025
# Versión: 3.1.0
# Descripción: Imagen Docker optimizada para producción

# Usar imagen base oficial de Python 3.11
FROM python:3.11-slim

# Metadatos de la imagen
LABEL maintainer="PAQUETES EL CLUB <guia@papyrus.com.co>"
LABEL version="3.1.0"
LABEL description="Sistema de gestión de paquetería optimizado para 50 usuarios simultáneos"
LABEL vendor="PAQUETES EL CLUB"

# Variables de entorno para optimización
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Crear usuario no-root para seguridad
RUN groupadd -r appuser && useradd -r -g appuser -m -s /bin/bash appuser

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY requirements.txt requirements-dev.txt ./

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY . .

# Crear directorios necesarios
RUN mkdir -p /app/uploads /app/logs /app/static /app/templates /app/monitoring

# Crear directorios de configuración si no existen
RUN mkdir -p /etc/nginx/conf.d

# Copiar scripts de gestión
COPY scripts/ /app/scripts/
RUN chmod +x /app/scripts/*.sh

# Copiar documentación
COPY README.md /app/
COPY docs/ /app/docs/

# Copiar esquema de base de datos
COPY database/database.sql /app/

# Cambiar propietario de archivos
RUN chown -R appuser:appuser /app

# Cambiar al usuario no-root
USER appuser

# Exponer puerto de la aplicación
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Comando por defecto
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
