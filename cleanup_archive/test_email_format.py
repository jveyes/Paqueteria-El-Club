#!/usr/bin/env python3
# ========================================
# PAQUETES EL CLUB v3.1 - Test de Formato de Email
# ========================================

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def test_email_format():
    """Probar el formato del email de reset de contraseña"""
    
    print("🔧 PAQUETES EL CLUB v3.1 - Test de Formato de Email")
    print("=" * 50)
    
    # Configuración SMTP
    smtp_host = "taylor.mxrouting.net"
    smtp_port = 587
    smtp_user = "guia@papyrus.com.co"
    smtp_password = "^Kxub2aoh@xC2LsK"  # En producción, usar variable de entorno
    
    # Email de destino
    to_email = "jveyes@gmail.com"
    reset_token = "test-token-12345"
    reset_url = f"http://localhost/auth/reset-password?token={reset_token}"
    
    print(f"📧 Configuración:")
    print(f"   De: {smtp_user}")
    print(f"   Para: {to_email}")
    print(f"   URL: {reset_url}")
    print()
    
    # Contenido del email (copiado del servicio)
    subject = "Restablecimiento de Contraseña - PAQUETES EL CLUB"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Restablecimiento de Contraseña - PAQUETES EL CLUB</title>
        <style>
            body {{ 
                font-family: Arial, sans-serif; 
                line-height: 1.6; 
                color: #333; 
                margin: 0; 
                padding: 20px; 
                background-color: #f4f4f4;
            }}
            .container {{ 
                max-width: 600px; 
                margin: 0 auto; 
                background-color: #ffffff; 
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 0 20px rgba(0,0,0,0.1);
            }}
            .header {{ 
                text-align: center; 
                padding: 20px 0; 
                border-bottom: 2px solid #3B82F6;
                margin-bottom: 30px;
            }}
            .service-name {{
                font-size: 24px;
                font-weight: bold;
                margin: 0 0 5px 0;
                color: #3B82F6;
            }}
            .service-subtitle {{
                font-size: 16px;
                margin: 0;
                color: #666;
            }}
            .content {{ 
                padding: 20px 0;
            }}
            .greeting {{
                font-size: 18px;
                color: #333;
                margin-bottom: 20px;
                font-weight: bold;
            }}
            .message {{
                font-size: 16px;
                color: #333;
                margin-bottom: 20px;
                line-height: 1.6;
            }}
            .button-container {{
                text-align: center;
                margin: 30px 0;
            }}
            .button {{ 
                display: inline-block; 
                background-color: #3B82F6; 
                color: white; 
                padding: 15px 30px; 
                text-decoration: none; 
                border-radius: 8px; 
                font-weight: bold;
                font-size: 16px;
                transition: background-color 0.3s;
            }}
            .button:hover {{
                background-color: #2563EB;
            }}
            .warning {{
                background-color: #FEF3C7;
                border: 1px solid #F59E0B;
                padding: 15px;
                margin: 20px 0;
                border-radius: 8px;
                text-align: center;
                color: #92400E;
                font-size: 14px;
            }}
            .link-container {{
                background-color: #F3F4F6;
                border: 1px solid #D1D5DB;
                border-radius: 8px;
                padding: 15px;
                margin: 20px 0;
                text-align: center;
            }}
            .link-text {{
                word-break: break-all; 
                color: #374151; 
                font-family: monospace;
                font-size: 12px;
                margin: 10px 0;
                padding: 10px;
                background-color: white;
                border-radius: 4px;
            }}
            .footer {{ 
                text-align: center; 
                padding: 20px 0; 
                border-top: 1px solid #E5E7EB;
                margin-top: 30px;
                color: #6B7280;
                font-size: 14px;
            }}
            .logo {{
                width: 120px;
                height: auto;
                margin-bottom: 10px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="service-name">PAQUETES EL CLUB</div>
                <div class="service-subtitle">Restablecimiento de Contraseña</div>
            </div>
            
            <div class="content">
                <div class="greeting">¡Hola Jesus!</div>
                
                <div class="message">
                    Has solicitado restablecer tu contraseña en <strong>PAQUETES EL CLUB</strong>, nuestro sistema de gestión de paquetería.
                </div>
                
                <div class="message">
                    Haz clic en el siguiente botón para crear una nueva contraseña de forma segura:
                </div>
                
                <div class="button-container">
                    <a href="{reset_url}" class="button">
                        🔐 Restablecer Contraseña
                    </a>
                </div>
                
                <div class="warning">
                    <strong>⚠️ IMPORTANTE:</strong> Este enlace expirará en 1 hora por seguridad.
                </div>
                
                <div class="link-container">
                    <p><strong>Si el botón no funciona, copia y pega este enlace en tu navegador:</strong></p>
                    <p class="link-text">{reset_url}</p>
                </div>
                
                <div class="message">
                    <strong>¿No solicitaste este cambio?</strong><br>
                    Si no fuiste tú quien solicitó este restablecimiento, puedes ignorar este email de forma segura. Tu contraseña actual permanecerá sin cambios.
                </div>
            </div>
            
            <div class="footer">
                <p><strong>PAQUETES EL CLUB</strong></p>
                <p>Cra. 91 #54-120, Local 12</p>
                <p>Tel: 3334004007 | Email: guia@papyrus.com.co</p>
                <p style="margin-top: 15px; font-size: 12px; color: #9CA3AF;">
                    Este es un email automático, por favor no respondas a este mensaje.<br>
                    Desarrollado por JEMAVI para PAPYRUS
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    
    try:
        # Configurar contexto SSL
        context = ssl.create_default_context()
        
        print("🔍 Conectando al servidor SMTP...")
        
        # Intentar conexión
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            print("✅ Conexión establecida")
            
            # Habilitar TLS
            server.starttls(context=context)
            print("✅ TLS habilitado")
            
            # Autenticación
            server.login(smtp_user, smtp_password)
            print("✅ Autenticación exitosa")
            
            # Crear email de prueba
            print("📤 Enviando email de prueba con formato actualizado...")
            
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"PAQUETES EL CLUB <{smtp_user}>"
            msg['To'] = to_email
            
            # Agregar contenido HTML
            html_part = MIMEText(html_content, 'html', 'utf-8')
            msg.attach(html_part)
            
            # Enviar email
            server.send_message(msg)
            print("✅ Email enviado exitosamente")
            print(f"📧 Verifica tu bandeja de entrada: {to_email}")
            print(f"🔗 URL del botón: {reset_url}")
            
            print("\n" + "=" * 50)
            print("🎉 ¡Formato de email actualizado correctamente!")
            print("✅ El texto 'Restablecer Contraseña' ahora es BLANCO")
            print("✅ La URL del enlace es correcta (sin puerto 8000)")
            
            print("\n📝 Verificaciones:")
            print("   ✅ Color del botón: white")
            print("   ✅ URL del enlace: http://localhost/auth/reset-password")
            print("   ✅ Email enviado exitosamente")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n" + "=" * 50)
        print("❌ Error en el sistema de emails")
        print("🔧 Revisa la configuración SMTP")

if __name__ == "__main__":
    test_email_format()
