#!/usr/bin/env python3
"""
Script de prueba para verificar la configuración SMTP
"""

import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def test_smtp_connection():
    """Probar conexión SMTP"""
    
    # Configuración SMTP desde variables de entorno
    smtp_host = os.getenv('SMTP_HOST', 'taylor.mxrouting.net')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    smtp_user = os.getenv('SMTP_USER', 'guia@papyrus.com.co')
    smtp_password = os.getenv('SMTP_PASSWORD', '^Kxub2aoh@xC2LsK')
    smtp_from_name = os.getenv('SMTP_FROM_NAME', 'PAQUETES EL CLUB')
    smtp_from_email = os.getenv('SMTP_FROM_EMAIL', 'guia@papyrus.com.co')
    
    print("🔍 CONFIGURACIÓN SMTP:")
    print(f"   Host: {smtp_host}")
    print(f"   Puerto: {smtp_port}")
    print(f"   Usuario: {smtp_user}")
    print(f"   Contraseña: {'*' * len(smtp_password) if smtp_password else 'NO CONFIGURADA'}")
    print(f"   From Name: {smtp_from_name}")
    print(f"   From Email: {smtp_from_email}")
    print()
    
    try:
        # Crear mensaje de prueba
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"Prueba SMTP - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        msg['From'] = f"{smtp_from_name} <{smtp_from_email}>"
        msg['To'] = "jveyes@gmail.com"
        
        # Contenido del mensaje
        html_content = f"""
        <html>
        <body>
            <h2>Prueba de Configuración SMTP</h2>
            <p>Este es un email de prueba para verificar la configuración SMTP.</p>
            <p><strong>Fecha y hora:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p><strong>Servidor:</strong> {smtp_host}:{smtp_port}</p>
            <hr>
            <p><em>PAQUETES EL CLUB v3.1</em></p>
        </body>
        </html>
        """
        
        html_part = MIMEText(html_content, 'html', 'utf-8')
        msg.attach(html_part)
        
        print("🔧 CONECTANDO AL SERVIDOR SMTP...")
        
        # Configurar contexto SSL
        context = ssl.create_default_context()
        
        # Conectar al servidor SMTP
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            print("✅ Conexión SMTP establecida")
            
            # Habilitar TLS
            server.starttls(context=context)
            print("✅ TLS habilitado")
            
            # Autenticación
            print("🔐 AUTENTICANDO...")
            server.login(smtp_user, smtp_password)
            print("✅ Autenticación exitosa")
            
            # Enviar email
            print("📧 ENVIANDO EMAIL...")
            server.send_message(msg)
            print("✅ Email enviado exitosamente")
            
            return True
            
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Error de autenticación SMTP: {e}")
        return False
    except smtplib.SMTPRecipientsRefused as e:
        print(f"❌ Destinatario rechazado: {e}")
        return False
    except smtplib.SMTPServerDisconnected as e:
        print(f"❌ Servidor SMTP desconectado: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBA DE CONFIGURACIÓN SMTP")
    print("=" * 50)
    
    success = test_smtp_connection()
    
    print("=" * 50)
    if success:
        print("🎉 PRUEBA EXITOSA: La configuración SMTP funciona correctamente")
    else:
        print("💥 PRUEBA FALLIDA: Hay problemas con la configuración SMTP")
    
    print("=" * 50)
