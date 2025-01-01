#!/usr/bin/env python3
"""
Script para probar el envío de email desde la aplicación
"""

import asyncio
import sys
import os

# Agregar el directorio src al path
sys.path.append('/app/src')

from src.services.notification_service import NotificationService
from src.database.database import get_db
from src.config import settings

async def test_email_from_app():
    """Probar envío de email desde la aplicación"""
    
    print("🚀 INICIANDO PRUEBA DE EMAIL DESDE LA APLICACIÓN")
    print("=" * 60)
    
    # Obtener sesión de base de datos
    db = next(get_db())
    
    try:
        # Crear instancia del servicio de notificaciones
        notification_service = NotificationService(db)
        
        # Configuración de prueba
        to_email = "jveyes@gmail.com"
        subject = f"Prueba desde Aplicación - {settings.app_name} v{settings.app_version}"
        message = f"""
        <html>
        <body>
            <h2>Prueba de Email desde la Aplicación</h2>
            <p>Este es un email de prueba enviado desde la aplicación PAQUETES EL CLUB.</p>
            <p><strong>Configuración SMTP:</strong></p>
            <ul>
                <li>Host: {settings.smtp_host}</li>
                <li>Puerto: {settings.smtp_port}</li>
                <li>Usuario: {settings.smtp_user}</li>
                <li>From: {settings.smtp_from_name} &lt;{settings.smtp_from_email}&gt;</li>
            </ul>
            <hr>
            <p><em>Enviado desde {settings.app_name} v{settings.app_version}</em></p>
        </body>
        </html>
        """
        
        print("🔍 CONFIGURACIÓN:")
        print(f"   Aplicación: {settings.app_name} v{settings.app_version}")
        print(f"   SMTP Host: {settings.smtp_host}")
        print(f"   SMTP Puerto: {settings.smtp_port}")
        print(f"   SMTP Usuario: {settings.smtp_user}")
        print(f"   From: {settings.smtp_from_name} <{settings.smtp_from_email}>")
        print(f"   To: {to_email}")
        print()
        
        print("📧 ENVIANDO EMAIL...")
        
        # Enviar email
        success = await notification_service._send_email(to_email, subject, message)
        
        if success:
            print("✅ Email enviado exitosamente desde la aplicación")
            return True
        else:
            print("❌ Error al enviar email desde la aplicación")
            return False
            
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = asyncio.run(test_email_from_app())
    
    print("=" * 60)
    if success:
        print("🎉 PRUEBA EXITOSA: El envío de email desde la aplicación funciona")
    else:
        print("💥 PRUEBA FALLIDA: Hay problemas con el envío de email desde la aplicación")
    print("=" * 60)
