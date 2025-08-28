#!/usr/bin/env python3
# ========================================
# PAQUETES EL CLUB v3.1 - Test del Sistema de Emails
# ========================================

import sys
import os
from pathlib import Path

# Agregar el directorio src al path
sys.path.append(str(Path(__file__).parent / "src"))

from src.services.notification_service import NotificationService
from src.database.database import SessionLocal
from src.models.user import User
import asyncio

def test_email_system():
    """Probar el sistema de emails"""
    
    print("🚀 Probando sistema de emails...")
    print("=" * 50)
    
    # Crear una sesión de base de datos
    db = SessionLocal()
    
    try:
        # Crear un usuario de prueba
        test_user = User(
            username="test_email",
            email="test@example.com",
            hashed_password="test_hash",
            first_name="Usuario",
            last_name="Prueba",
            phone="1234567890"
        )
        
        # Crear el servicio de notificaciones
        notification_service = NotificationService(db)
        
        # Token de prueba
        test_token = "test_token_12345"
        
        print("📧 Enviando email de recuperación de contraseña...")
        
        # Ejecutar el envío de email
        result = asyncio.run(
            notification_service.send_password_reset_email(test_user, test_token)
        )
        
        if result:
            print("✅ Email enviado exitosamente")
            print("📧 Verifica tu bandeja de entrada (o spam)")
        else:
            print("❌ Error al enviar email")
            
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
    finally:
        db.close()

def test_smtp_connection():
    """Probar conexión SMTP"""
    
    print("🔍 Probando conexión SMTP...")
    print("=" * 50)
    
    try:
        import smtplib
        import ssl
        from src.config import settings
        
        # Configurar contexto SSL
        context = ssl.create_default_context()
        
        print(f"Conectando a: {settings.smtp_host}:{settings.smtp_port}")
        print(f"Usuario: {settings.smtp_user}")
        
        # Intentar conexión
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
            server.starttls(context=context)
            
            # Intentar autenticación
            server.login(settings.smtp_user, settings.smtp_password)
            
            print("✅ Conexión SMTP exitosa")
            print("✅ Autenticación exitosa")
            
            # Probar envío de email simple
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            
            msg = MIMEMultipart()
            msg['Subject'] = "Test Email - PAQUETES EL CLUB"
            msg['From'] = f"{settings.smtp_from_name} <{settings.smtp_from_email}>"
            msg['To'] = "test@example.com"
            
            text = "Este es un email de prueba del sistema PAQUETES EL CLUB."
            msg.attach(MIMEText(text, 'plain'))
            
            server.send_message(msg)
            print("✅ Email de prueba enviado exitosamente")
            
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Error de autenticación SMTP: {e}")
    except smtplib.SMTPServerDisconnected as e:
        print(f"❌ Servidor SMTP desconectado: {e}")
    except Exception as e:
        print(f"❌ Error de conexión SMTP: {e}")

def main():
    """Ejecutar todas las pruebas"""
    
    print("🔧 PAQUETES EL CLUB v3.1 - Test del Sistema de Emails")
    print("=" * 60)
    
    # Probar conexión SMTP
    test_smtp_connection()
    
    print()
    
    # Probar sistema de emails
    test_email_system()
    
    print()
    print("=" * 60)
    print("✅ Pruebas completadas")
    print()
    print("📝 Notas:")
    print("   - Si las pruebas fallan, verifica la configuración SMTP")
    print("   - En modo desarrollo, los emails se simulan")
    print("   - Revisa los logs para más detalles")

if __name__ == "__main__":
    main()
