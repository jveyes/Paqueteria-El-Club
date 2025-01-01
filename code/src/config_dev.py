# ========================================
# PAQUETES EL CLUB v3.1 - Configuración de Desarrollo
# ========================================

import os
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Configuración centralizada de la aplicación para desarrollo"""
    
    # Configuración de la Aplicación
    app_name: str = "PAQUETES EL CLUB"
    app_version: str = "3.1.0"
    debug: bool = True
    environment: str = "development"
    
    # Base de Datos AWS RDS (ÚNICA FUENTE)
    database_url: str = "postgresql://jveyes:a?HC!2.*1#?[==:|289qAI=)#V4kDzl$@ls-abe25e9bea57818f0ee32555c0e7b4a10e361535.ctobuhtlkwoj.us-east-1.rds.amazonaws.com:5432/paqueteria"
    
    # Cache Redis
    redis_url: str = "redis://redis:6379/0"
    redis_password: str = ""
    redis_host: str = "redis"
    redis_port: int = 6379
    redis_db: int = 0
    
    # Seguridad
    secret_key: str = "paqueteria-secret-key-2025-super-secure-jwt-token-key-for-authentication"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Configuración SMTP
    smtp_host: Optional[str] = None
    smtp_port: Optional[int] = 587
    smtp_user: Optional[str] = None
    smtp_password: Optional[str] = None
    smtp_from_name: str = "PAQUETES EL CLUB"
    smtp_from_email: str = "guia@papyrus.com.co"
    
    # Configuración SMS (LIWA.co)
    liwa_api_key: Optional[str] = None
    liwa_phone_number: Optional[str] = None
    liwa_from_name: str = "PAQUETES EL CLUB"
    
    # Configuración de Tarifas
    base_storage_rate: int = 1000
    base_delivery_rate: int = 1500
    normal_package_multiplier: int = 1500
    extra_dimension_package_multiplier: int = 2000
    currency: str = "COP"
    
    # Configuración de Archivos
    upload_dir: str = "./uploads"
    max_file_size: int = 5242880  # 5MB
    allowed_extensions: str = "jpg,jpeg,png,gif,webp"
    
    # Configuración de la Empresa
    company_name: str = "PAQUETES EL CLUB"
    company_address: str = "Cra. 91 #54-120, Local 12"
    company_phone: str = "3334004007"
    company_email: str = "guia@papyrus.com.co"
    
    # Configuración de Monitoreo
    grafana_password: str = "Grafana2025!Secure"
    prometheus_port: int = 9090
    grafana_port: int = 3000
    
    # Configuración de Logs
    log_level: str = "INFO"
    log_file: str = "./logs/app.log"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Configuración de PWA
    pwa_name: str = "PAQUETES EL CLUB"
    pwa_short_name: str = "Paquetes"
    pwa_description: str = "Sistema de gestión de paquetería"
    pwa_theme_color: str = "#3B82F6"
    pwa_background_color: str = "#FFFFFF"
    
    class Config:
        env_file = "env.aws"  # Cambiado a env.aws para usar solo AWS RDS
        case_sensitive = False
        extra = "ignore"  # Ignorar variables extra

# Instancia global de configuración
settings = Settings()
