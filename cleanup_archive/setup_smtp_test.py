#!/usr/bin/env python3
"""
Script para configurar y probar SMTP con Gmail
"""

import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def test_smtp_connection(host, port, username, password, use_tls=True):
    """Probar conexión SMTP"""
    try:
        print(f"🔍 Probando conexión SMTP a {host}:{port}...")
        
        if use_tls:
            context = ssl.create_default_context()
            server = smtplib.SMTP(host, port)
            server.starttls(context=context)
        else:
            server = smtplib.SMTP(host, port)
        
        server.login(username, password)
        print("✅ Conexión SMTP exitosa")
        server.quit()
        return True
    except Exception as e:
        print(f"❌ Error de conexión SMTP: {e}")
        return False

def send_test_email(host, port, username, password, to_email, use_tls=True):
    """Enviar email de prueba"""
    try:
        print(f"📧 Enviando email de prueba a {to_email}...")
        
        # Crear mensaje
        msg = MIMEMultipart()
        msg['From'] = username
        msg['To'] = to_email
        msg['Subject'] = f"Prueba SMTP - Paquetes El Club v3.1 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        # Contenido del email
        body = f"""
        <html>
        <body>
            <h2>🎉 Prueba SMTP Exitosa</h2>
            <p>Este es un email de prueba del sistema <strong>Paquetes El Club v3.1</strong>.</p>
            
            <h3>📊 Información de la prueba:</h3>
            <ul>
                <li><strong>Servidor SMTP:</strong> {host}:{port}</li>
                <li><strong>Usuario:</strong> {username}</li>
                <li><strong>TLS:</strong> {'Habilitado' if use_tls else 'Deshabilitado'}</li>
                <li><strong>Fecha y hora:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</li>
                <li><strong>Servidor:</strong> AWS EC2 - guia.papyrus.com.co</li>
            </ul>
            
            <h3>✅ Estado del sistema:</h3>
            <ul>
                <li>🌐 Aplicación: https://guia.papyrus.com.co</li>
                <li>🗄️ Base de datos: AWS RDS</li>
                <li>📧 Sistema de emails: Configurado</li>
                <li>🔐 Sistema de autenticación: Funcionando</li>
            </ul>
            
            <p><em>Este email confirma que el sistema de envío de emails está funcionando correctamente.</em></p>
            
            <hr>
            <p><small>Paquetes El Club v3.1 - Sistema de gestión de paquetería</small></p>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(body, 'html'))
        
        # Conectar y enviar
        if use_tls:
            context = ssl.create_default_context()
            server = smtplib.SMTP(host, port)
            server.starttls(context=context)
        else:
            server = smtplib.SMTP(host, port)
        
        server.login(username, password)
        server.send_message(msg)
        server.quit()
        
        print("✅ Email de prueba enviado exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error enviando email: {e}")
        return False

def main():
    print("🔧 ========================================")
    print("🔧 CONFIGURACIÓN Y PRUEBA DE SMTP")
    print("🔧 PAQUETES EL CLUB v3.1")
    print("🔧 ========================================")
    print("")
    
    # Configuración SMTP para Gmail
    smtp_config = {
        'host': 'smtp.gmail.com',
        'port': 587,
        'username': 'jveyes@gmail.com',  # Email de pruebas
        'password': '',  # Se pedirá al usuario
        'use_tls': True
    }
    
    print("📧 CONFIGURACIÓN SMTP PARA PRUEBAS:")
    print("=" * 40)
    print(f"🏢 Servidor: {smtp_config['host']}")
    print(f"🔌 Puerto: {smtp_config['port']}")
    print(f"👤 Usuario: {smtp_config['username']}")
    print(f"🔒 TLS: {'Habilitado' if smtp_config['use_tls'] else 'Deshabilitado'}")
    print("")
    
    # Solicitar contraseña de aplicación
    print("⚠️  IMPORTANTE: Para Gmail necesitas una 'Contraseña de aplicación'")
    print("📋 Pasos para obtenerla:")
    print("   1. Ve a https://myaccount.google.com/security")
    print("   2. Activa la verificación en 2 pasos si no está activada")
    print("   3. Ve a 'Contraseñas de aplicación'")
    print("   4. Genera una nueva contraseña para 'Correo'")
    print("   5. Usa esa contraseña aquí (no tu contraseña normal)")
    print("")
    
    # Por ahora, vamos a probar con configuración básica
    print("🧪 PRUEBA CON CONFIGURACIÓN BÁSICA:")
    print("=" * 40)
    
    # Probar conexión SMTP (sin autenticación)
    print("1️⃣ Probando conexión SMTP básica...")
    try:
        server = smtplib.SMTP(smtp_config['host'], smtp_config['port'])
        server.starttls()
        print("✅ Conexión SMTP básica exitosa")
        server.quit()
    except Exception as e:
        print(f"❌ Error en conexión básica: {e}")
    
    # Crear archivo de configuración SMTP
    print("\n2️⃣ Creando archivo de configuración SMTP...")
    smtp_config_content = f"""
# ========================================
# CONFIGURACIÓN SMTP PARA PAQUETES EL CLUB v3.1
# ========================================

# Configuración SMTP Gmail
EMAIL_HOST={smtp_config['host']}
EMAIL_PORT={smtp_config['port']}
EMAIL_USERNAME={smtp_config['username']}
EMAIL_PASSWORD=TU_CONTRASEÑA_DE_APLICACIÓN_AQUÍ
EMAIL_USE_TLS={str(smtp_config['use_tls']).lower()}

# Configuración adicional
EMAIL_FROM_NAME=Paquetes El Club
EMAIL_FROM_ADDRESS={smtp_config['username']}

# Notas importantes:
# - Para Gmail, usa una 'Contraseña de aplicación'
# - No uses tu contraseña normal de Gmail
# - Activa la verificación en 2 pasos primero
"""
    
    with open('smtp_config.txt', 'w') as f:
        f.write(smtp_config_content)
    
    print("✅ Archivo smtp_config.txt creado")
    
    # Mostrar instrucciones
    print("\n📋 INSTRUCCIONES PARA CONFIGURAR SMTP:")
    print("=" * 50)
    print("1. Obtén una contraseña de aplicación de Gmail")
    print("2. Edita el archivo .env y agrega:")
    print(f"   EMAIL_HOST={smtp_config['host']}")
    print(f"   EMAIL_PORT={smtp_config['port']}")
    print(f"   EMAIL_USERNAME={smtp_config['username']}")
    print(f"   EMAIL_PASSWORD=TU_CONTRASEÑA_DE_APLICACIÓN")
    print(f"   EMAIL_USE_TLS=true")
    print("3. Reinicia los contenedores")
    print("4. Ejecuta el script de prueba de email")
    
    print("\n🌐 URLs de la aplicación:")
    print("=" * 30)
    print("🔗 Aplicación: https://guia.papyrus.com.co")
    print("🔗 Forgot Password: https://guia.papyrus.com.co/forgot-password")
    
    print("\n✅ Configuración SMTP preparada")
    print("📧 Email de pruebas: jveyes@gmail.com")
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🚀 ¡Configuración SMTP lista!")
    else:
        print("\n❌ Error en la configuración")
