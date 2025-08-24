# ========================================
# PAQUETES EL CLUB v3.0 - Configuración Segura para GitHub
# ========================================

import os
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Configuración centralizada de la aplicación - Versión segura para GitHub"""
    
    # Configuración de la Aplicación
    app_name: str = "PAQUETES EL CLUB"
    app_version: str = "3.0.0"
    debug: bool = True
    environment: str = "development"
    
    # Base de Datos - Usar variables de entorno
    database_url: str = os.getenv("DATABASE_URL", "postgresql://paqueteria_user:password@postgres:5432/paqueteria")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD", "your_postgres_password")
    postgres_user: str = os.getenv("POSTGRES_USER", "paqueteria_user")
    postgres_db: str = os.getenv("POSTGRES_DB", "paqueteria")
    postgres_host: str = os.getenv("POSTGRES_HOST", "postgres")
    postgres_port: int = int(os.getenv("POSTGRES_PORT", "5432"))
    
    # Cache Redis - Usar variables de entorno
    redis_url: str = os.getenv("REDIS_URL", "redis://:password@redis:6379/0")
    redis_password: str = os.getenv("REDIS_PASSWORD", "your_redis_password")
    redis_host: str = os.getenv("REDIS_HOST", "redis")
    redis_port: int = int(os.getenv("REDIS_PORT", "6379"))
    redis_db: int = int(os.getenv("REDIS_DB", "0"))
    
    # Seguridad - Usar variables de entorno
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Configuración SMTP - Usar variables de entorno
    smtp_host: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port: int = int(os.getenv("SMTP_PORT", "587"))
    smtp_user: str = os.getenv("SMTP_USER", "your-email@gmail.com")
    smtp_password: str = os.getenv("SMTP_PASSWORD", "your-app-password")
    smtp_from_name: str = os.getenv("SMTP_FROM_NAME", "PAQUETES EL CLUB")
    smtp_from_email: str = os.getenv("SMTP_FROM_EMAIL", "your-email@gmail.com")
    
    # Configuración SMS (LIWA.co) - Usar variables de entorno
    liwa_api_key: Optional[str] = os.getenv("LIWA_API_KEY")
    liwa_phone_number: Optional[str] = os.getenv("LIWA_PHONE_NUMBER")
    liwa_from_name: str = os.getenv("LIWA_FROM_NAME", "PAQUETES EL CLUB")
    
    # Configuración de Tarifas
    base_storage_rate: int = int(os.getenv("BASE_STORAGE_RATE", "1000"))
    base_delivery_rate: int = int(os.getenv("BASE_DELIVERY_RATE", "1500"))
    normal_package_multiplier: int = int(os.getenv("NORMAL_PACKAGE_MULTIPLIER", "1500"))
    extra_dimension_package_multiplier: int = int(os.getenv("EXTRA_DIMENSION_PACKAGE_MULTIPLIER", "2000"))
    currency: str = os.getenv("CURRENCY", "COP")
    
    # Configuración de Archivos
    upload_dir: str = os.getenv("UPLOAD_DIR", "./uploads")
    max_file_size: int = int(os.getenv("MAX_FILE_SIZE", "5242880"))  # 5MB
    allowed_extensions: str = os.getenv("ALLOWED_EXTENSIONS", "jpg,jpeg,png,gif,webp")
    
    # Configuración de la Empresa
    company_name: str = os.getenv("COMPANY_NAME", "PAQUETES EL CLUB")
    company_address: str = os.getenv("COMPANY_ADDRESS", "Cra. 91 #54-120, Local 12")
    company_phone: str = os.getenv("COMPANY_PHONE", "3334004007")
    company_email: str = os.getenv("COMPANY_EMAIL", "guia@papyrus.com.co")
    
    # Configuración de Monitoreo - Usar variables de entorno
    grafana_password: str = os.getenv("GRAFANA_PASSWORD", "your_grafana_password")
    prometheus_port: int = int(os.getenv("PROMETHEUS_PORT", "9090"))
    grafana_port: int = int(os.getenv("GRAFANA_PORT", "3000"))
    
    # Configuración de Logs
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    log_file: str = os.getenv("LOG_FILE", "./logs/app.log")
    
    # Configuración de PWA
    pwa_name: str = os.getenv("PWA_NAME", "PAQUETES EL CLUB")
    pwa_short_name: str = os.getenv("PWA_SHORT_NAME", "Paquetes")
    pwa_description: str = os.getenv("PWA_DESCRIPTION", "Sistema de gestión de paquetería")
    pwa_theme_color: str = os.getenv("PWA_THEME_COLOR", "#3B82F6")
    pwa_background_color: str = os.getenv("PWA_BACKGROUND_COLOR", "#FFFFFF")
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Instancia global de configuración
settings = Settings()
