# ========================================
# PAQUETES EL CLUB v3.1 - Configuración Centralizada
# ========================================

import os
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Configuración centralizada de la aplicación"""
    
    # Configuración de la Aplicación
    app_name: str = "PAQUETES EL CLUB"
    app_version: str = "3.1.0"
    debug: bool = True
    environment: str = "development"
    
    # Base de Datos PostgreSQL AWS RDS (ÚNICA FUENTE)
    database_url: str = "postgresql://jveyes:a?HC!2.*1#?[==:|289qAI=)#V4kDzl$@ls-abe25e9bea57818f0ee32555c0e7b4a10e361535.ctobuhtlkwoj.us-east-1.rds.amazonaws.com:5432/paqueteria"
    postgres_password: str = "a?HC!2.*1#?[==:|289qAI=)#V4kDzl$"
    postgres_user: str = "jveyes"
    postgres_db: str = "paqueteria"
    postgres_host: str = "ls-abe25e9bea57818f0ee32555c0e7b4a10e361535.ctobuhtlkwoj.us-east-1.rds.amazonaws.com"
    postgres_port: int = 5432
    
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
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    smtp_from_name: str = "PAQUETERIA EL CLUB"
    smtp_from_email: str = ""
    
    # Configuración SMS (LIWA.co) - SOLO SMS
    liwa_api_key: str = "c52d8399ac63a24563ee8a967bafffc6cb8d8dfa"
    liwa_account: str = "00486396309"
    liwa_password: str = "6fEuRnd*$$#NfFAS"
    liwa_auth_url: str = "https://api.liwa.co/v2/auth/login"
    liwa_from_name: str = "PAQUETES EL CLUB"
    
    # NOTA: WhatsApp no está habilitado en esta versión
    # whatsapp_enabled: bool = False
    
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
    
    # Configuración de autenticación
    secret_key: str = "paqueteria-secret-key-2025-super-secure-jwt-token-key-for-authentication"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Configuración de PWA
    pwa_name: str = "PAQUETES EL CLUB"
    pwa_short_name: str = "Paquetes"
    pwa_description: str = "Sistema de gestión de paquetería"
    pwa_theme_color: str = "#3B82F6"
    pwa_background_color: str = "#FFFFFF"
    
    class Config:
        case_sensitive = False
        extra = "ignore"  # Ignorar variables extra

# Instancia global de configuración
try:
    settings = Settings()
except Exception as e:
    print(f"Error cargando configuración: {e}")
    # Usar configuración simple como fallback
    from .config_simple import settings
