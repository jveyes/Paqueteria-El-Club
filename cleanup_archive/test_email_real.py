#!/usr/bin/env python3
# ========================================
# PAQUETES EL CLUB v3.1 - Test de Email Real
# ========================================

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys

def test_real_email(to_email=None):
    """Probar envío de email real"""
    
    print("🔧 PAQUETES EL CLUB v3.1 - Test de Email Real")
    print("=" * 50)
    
    # Configuración SMTP
    smtp_host = "taylor.mxrouting.net"
    smtp_port = 587
    smtp_user = "guia@papyrus.com.co"
    smtp_password = "^Kxub2aoh@xC2LsK"  # En producción, usar variable de entorno
    
    # Email de destino
    if not to_email:
        to_email = input("📧 Ingresa tu email para recibir la prueba: ").strip()
    
    if not to_email:
        print("❌ No se proporcionó un email válido")
        return False
    
    print(f"📧 Configuración:")
    print(f"   De: {smtp_user}")
    print(f"   Para: {to_email}")
    print(f"   Servidor: {smtp_host}:{smtp_port}")
    print()
    
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
            print("📤 Enviando email de prueba...")
            
            msg = MIMEMultipart('alternative')
            msg['Subject'] = "Test Email - PAQUETES EL CLUB v3.1"
            msg['From'] = f"PAQUETES EL CLUB <{smtp_user}>"
            msg['To'] = to_email
            
            # Contenido HTML
            html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Test Email - PAQUETES EL CLUB</title>
                <style>
                    body { 
                        font-family: Arial, sans-serif; 
                        line-height: 1.6; 
                        color: #333; 
                        margin: 0; 
                        padding: 20px; 
                        background-color: #f4f4f4;
                    }
                    .container { 
                        max-width: 600px; 
                        margin: 0 auto; 
                        background-color: #ffffff; 
                        padding: 30px;
                        border-radius: 10px;
                        box-shadow: 0 0 20px rgba(0,0,0,0.1);
                    }
                    .header { 
                        text-align: center; 
                        padding: 20px 0; 
                        border-bottom: 2px solid #3B82F6;
                        margin-bottom: 30px;
                    }
                    .service-name {
                        font-size: 24px;
                        font-weight: bold;
                        margin: 0 0 5px 0;
                        color: #3B82F6;
                    }
                    .content { 
                        padding: 20px 0;
                    }
                    .message {
                        font-size: 16px;
                        color: #333;
                        margin-bottom: 20px;
                        line-height: 1.6;
                    }
                    .success {
                        background-color: #D1FAE5;
                        border: 1px solid #10B981;
                        padding: 15px;
                        margin: 20px 0;
                        border-radius: 8px;
                        color: #065F46;
                    }
                    .footer { 
                        text-align: center; 
                        padding: 20px 0; 
                        border-top: 1px solid #E5E7EB;
                        margin-top: 30px;
                        color: #6B7280;
                        font-size: 14px;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <div class="service-name">PAQUETES EL CLUB</div>
                        <div style="color: #666;">Test de Sistema de Emails</div>
                    </div>
                    
                    <div class="content">
                        <div class="message">
                            <strong>¡Hola!</strong>
                        </div>
                        
                        <div class="message">
                            Este es un email de prueba del sistema <strong>PAQUETES EL CLUB v3.1</strong>.
                        </div>
                        
                        <div class="success">
                            <strong>✅ ¡Éxito!</strong><br>
                            Si recibes este email, significa que el sistema de emails está funcionando correctamente.
                        </div>
                        
                        <div class="message">
                            <strong>Detalles del sistema:</strong><br>
                            • Servidor SMTP: taylor.mxrouting.net:587<br>
                            • Autenticación: TLS<br>
                            • Remitente: guia@papyrus.com.co<br>
                            • Sistema: PAQUETES EL CLUB v3.1
                        </div>
                        
                        <div class="message">
                            El sistema de recuperación de contraseña ahora está completamente funcional.
                        </div>
                    </div>
                    
                    <div class="footer">
                        <p><strong>PAQUETES EL CLUB</strong></p>
                        <p>Cra. 91 #54-120, Local 12</p>
                        <p>Tel: 3334004007 | Email: guia@papyrus.com.co</p>
                        <p style="margin-top: 15px; font-size: 12px; color: #9CA3AF;">
                            Este es un email de prueba del sistema.<br>
                            Desarrollado por JEMAVI para PAPYRUS
                        </p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            # Agregar contenido HTML
            html_part = MIMEText(html_content, 'html', 'utf-8')
            msg.attach(html_part)
            
            # Enviar email
            server.send_message(msg)
            print("✅ Email enviado exitosamente")
            print(f"📧 Verifica tu bandeja de entrada: {to_email}")
            print("📧 También revisa la carpeta de spam si no lo encuentras")
            
            return True
            
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Error de autenticación SMTP: {e}")
        return False
        
    except smtplib.SMTPServerDisconnected as e:
        print(f"❌ Servidor SMTP desconectado: {e}")
        return False
        
    except Exception as e:
        print(f"❌ Error de conexión SMTP: {e}")
        return False

def main():
    """Ejecutar prueba de email real"""
    
    print("🚀 Probando envío de email real...")
    print()
    
    # Verificar si se proporcionó email como argumento
    to_email = None
    if len(sys.argv) > 1:
        to_email = sys.argv[1]
    
    success = test_real_email(to_email)
    
    print("\n" + "=" * 50)
    
    if success:
        print("🎉 ¡Sistema de emails funcionando correctamente!")
        print("📧 El sistema de recuperación de contraseña está listo")
    else:
        print("❌ Error en el sistema de emails")
        print("🔧 Revisa la configuración SMTP")
    
    print()
    print("📝 Próximos pasos:")
    print("   1. Verifica que recibiste el email de prueba")
    print("   2. Prueba la recuperación de contraseña desde la web")
    print("   3. El sistema está listo para producción")
    print()
    print("💡 Uso del script:")
    print("   python3 test_email_real.py")
    print("   python3 test_email_real.py tuemail@ejemplo.com")

if __name__ == "__main__":
    main()
