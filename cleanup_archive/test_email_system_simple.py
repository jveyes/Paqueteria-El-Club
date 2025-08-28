#!/usr/bin/env python3
# ========================================
# PAQUETES EL CLUB v3.1 - Test Simple del Sistema de Emails
# ========================================

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def test_smtp_connection():
    """Probar conexión SMTP con las credenciales actualizadas"""
    
    print("🔧 PAQUETES EL CLUB v3.1 - Test SMTP")
    print("=" * 50)
    
    # Configuración SMTP
    smtp_host = "taylor.mxrouting.net"
    smtp_port = 587
    smtp_user = "guia@papyrus.com.co"
    smtp_password = "^Kxub2aoh@xC2LsK"
    
    print(f"📧 Configuración SMTP:")
    print(f"   Servidor: {smtp_host}:{smtp_port}")
    print(f"   Usuario: {smtp_user}")
    print(f"   Contraseña: {'*' * len(smtp_password)}")
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
            
            # Intentar autenticación
            print("🔐 Intentando autenticación...")
            server.login(smtp_user, smtp_password)
            print("✅ Autenticación exitosa")
            
            # Probar envío de email simple
            print("📤 Enviando email de prueba...")
            
            msg = MIMEMultipart()
            msg['Subject'] = "Test Email - PAQUETES EL CLUB"
            msg['From'] = f"PAQUETES EL CLUB <{smtp_user}>"
            msg['To'] = "test@example.com"
            
            text = """
            Este es un email de prueba del sistema PAQUETES EL CLUB.
            
            Si recibes este email, significa que la configuración SMTP está funcionando correctamente.
            
            Saludos,
            Sistema PAQUETES EL CLUB
            """
            
            msg.attach(MIMEText(text, 'plain', 'utf-8'))
            
            server.send_message(msg)
            print("✅ Email de prueba enviado exitosamente")
            
            return True
            
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Error de autenticación SMTP: {e}")
        print("💡 Posibles soluciones:")
        print("   - Verifica que la contraseña sea correcta")
        print("   - Asegúrate de que la cuenta esté habilitada")
        print("   - Verifica que el servidor permita autenticación")
        return False
        
    except smtplib.SMTPServerDisconnected as e:
        print(f"❌ Servidor SMTP desconectado: {e}")
        return False
        
    except Exception as e:
        print(f"❌ Error de conexión SMTP: {e}")
        return False

def test_email_with_different_ports():
    """Probar diferentes puertos SMTP"""
    
    print("\n🔍 Probando diferentes configuraciones SMTP...")
    print("=" * 50)
    
    configs = [
        {"host": "taylor.mxrouting.net", "port": 587, "name": "TLS 587"},
        {"host": "taylor.mxrouting.net", "port": 465, "name": "SSL 465"},
        {"host": "taylor.mxrouting.net", "port": 25, "name": "SMTP 25"},
    ]
    
    smtp_user = "guia@papyrus.com.co"
    smtp_password = "^Kxub2aoh@xC2LsK"
    
    for config in configs:
        print(f"\n🔍 Probando {config['name']}...")
        
        try:
            context = ssl.create_default_context()
            
            if config['port'] == 465:
                # SSL
                with smtplib.SMTP_SSL(config['host'], config['port'], context=context) as server:
                    server.login(smtp_user, smtp_password)
                    print(f"✅ {config['name']} - Conexión exitosa")
            else:
                # TLS o SMTP normal
                with smtplib.SMTP(config['host'], config['port']) as server:
                    if config['port'] == 587:
                        server.starttls(context=context)
                    server.login(smtp_user, smtp_password)
                    print(f"✅ {config['name']} - Conexión exitosa")
                    
        except Exception as e:
            print(f"❌ {config['name']} - Error: {e}")

def main():
    """Ejecutar todas las pruebas"""
    
    print("🚀 Iniciando pruebas del sistema de emails...")
    print()
    
    # Probar configuración principal
    success = test_smtp_connection()
    
    if not success:
        print("\n🔄 Probando configuraciones alternativas...")
        test_email_with_different_ports()
    
    print("\n" + "=" * 50)
    print("✅ Pruebas completadas")
    print()
    print("📝 Notas:")
    print("   - Si las pruebas fallan, verifica las credenciales")
    print("   - Algunos servidores requieren configuración específica")
    print("   - Contacta al proveedor de email si persisten los problemas")

if __name__ == "__main__":
    main()
