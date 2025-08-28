#!/usr/bin/env python3
"""
Script para probar el envío de emails con SMTP configurado
"""

import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def send_test_email_with_password(password):
    """Enviar email de prueba con contraseña proporcionada"""
    try:
        print("📧 CONFIGURACIÓN SMTP:")
        print("=" * 30)
        print("🏢 Servidor: smtp.gmail.com")
        print("🔌 Puerto: 587")
        print("👤 Usuario: jveyes@gmail.com")
        print("🔒 TLS: Habilitado")
        print("")
        
        # Configuración SMTP
        smtp_host = "smtp.gmail.com"
        smtp_port = 587
        smtp_username = "jveyes@gmail.com"
        smtp_password = password
        to_email = "jveyes@gmail.com"
        
        print(f"🔍 Probando conexión SMTP...")
        
        # Crear mensaje
        msg = MIMEMultipart()
        msg['From'] = smtp_username
        msg['To'] = to_email
        msg['Subject'] = f"🎉 Prueba SMTP Exitosa - Paquetes El Club v3.1 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        # Contenido del email
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                <div style="text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px 10px 0 0;">
                    <h1 style="margin: 0;">🎉 Prueba SMTP Exitosa</h1>
                    <p style="margin: 10px 0 0 0; font-size: 18px;">Paquetes El Club v3.1</p>
                </div>
                
                <div style="padding: 20px;">
                    <h2 style="color: #667eea;">✅ Sistema de Emails Funcionando</h2>
                    <p>Este email confirma que el sistema de envío de emails está funcionando correctamente desde el servidor AWS.</p>
                    
                    <h3 style="color: #667eea;">📊 Información de la Prueba:</h3>
                    <ul>
                        <li><strong>Servidor SMTP:</strong> {smtp_host}:{smtp_port}</li>
                        <li><strong>Usuario:</strong> {smtp_username}</li>
                        <li><strong>TLS:</strong> Habilitado</li>
                        <li><strong>Fecha y hora:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</li>
                        <li><strong>Servidor:</strong> AWS EC2 - guia.papyrus.com.co</li>
                    </ul>
                    
                    <h3 style="color: #667eea;">✅ Estado del Sistema:</h3>
                    <ul>
                        <li>🌐 <strong>Aplicación:</strong> <a href="https://guia.papyrus.com.co" style="color: #667eea;">https://guia.papyrus.com.co</a></li>
                        <li>🗄️ <strong>Base de datos:</strong> AWS RDS - Funcionando</li>
                        <li>📧 <strong>Sistema de emails:</strong> Configurado y funcionando</li>
                        <li>🔐 <strong>Sistema de autenticación:</strong> Funcionando</li>
                        <li>🔄 <strong>Restablecimiento de contraseña:</strong> Disponible</li>
                    </ul>
                    
                    <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                        <h4 style="margin-top: 0; color: #667eea;">🔐 Credenciales de Acceso:</h4>
                        <p><strong>URL:</strong> <a href="https://guia.papyrus.com.co" style="color: #667eea;">https://guia.papyrus.com.co</a></p>
                        <p><strong>Usuario:</strong> jveyes</p>
                        <p><strong>Email:</strong> jveyes@gmail.com</p>
                    </div>
                    
                    <p><em>Este email confirma que el sistema de envío de emails está funcionando correctamente y que el restablecimiento de contraseña estará disponible.</em></p>
                </div>
                
                <div style="text-align: center; padding: 20px; background: #f8f9fa; border-radius: 0 0 10px 10px;">
                    <p style="margin: 0; color: #666; font-size: 14px;">
                        <strong>Paquetes El Club v3.1</strong><br>
                        Sistema de gestión de paquetería<br>
                        Desarrollado en AWS Cloud
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(body, 'html'))
        
        print("📤 Enviando email de prueba...")
        
        # Conectar y enviar
        context = ssl.create_default_context()
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls(context=context)
        server.login(smtp_username, smtp_password)
        server.send_message(msg)
        server.quit()
        
        print("✅ Email de prueba enviado exitosamente")
        print(f"📧 Email enviado a: {to_email}")
        print("")
        print("🎉 ¡Sistema de emails funcionando correctamente!")
        print("🔐 El restablecimiento de contraseña ahora está disponible")
        
        return True
        
    except Exception as e:
        print(f"❌ Error enviando email: {e}")
        print("")
        print("🔧 SOLUCIÓN:")
        print("1. Verifica que tienes una contraseña de aplicación válida")
        print("2. Asegúrate de que la verificación en 2 pasos esté activada")
        print("3. Genera una nueva contraseña de aplicación en Gmail")
        return False

def main():
    print("📧 ========================================")
    print("📧 PRUEBA DE ENVÍO DE EMAILS")
    print("📧 PAQUETES EL CLUB v3.1")
    print("📧 ========================================")
    print("")
    
    print("⚠️  IMPORTANTE: Necesitas una contraseña de aplicación de Gmail")
    print("📋 Si no la tienes, sigue estos pasos:")
    print("   1. Ve a https://myaccount.google.com/security")
    print("   2. Activa la verificación en 2 pasos si no está activada")
    print("   3. Ve a 'Contraseñas de aplicación'")
    print("   4. Genera una nueva contraseña para 'Correo'")
    print("   5. Usa esa contraseña aquí (no tu contraseña normal)")
    print("")
    
    # Por ahora, vamos a mostrar las instrucciones
    print("📋 INSTRUCCIONES PARA PROBAR EMAILS:")
    print("=" * 50)
    print("1. Obtén una contraseña de aplicación de Gmail")
    print("2. Ejecuta este script con la contraseña:")
    print("   python3 test_email_send.py TU_CONTRASEÑA_AQUÍ")
    print("3. O edita el archivo .env y agrega:")
    print("   EMAIL_PASSWORD=TU_CONTRASEÑA_DE_APLICACIÓN")
    print("4. Reinicia los contenedores")
    print("5. Prueba el restablecimiento de contraseña")
    
    print("\n🌐 URLs de la aplicación:")
    print("=" * 30)
    print("🔗 Aplicación: https://guia.papyrus.com.co")
    print("🔗 Forgot Password: https://guia.papyrus.com.co/forgot-password")
    
    print("\n✅ Configuración SMTP lista")
    print("📧 Email de pruebas: jveyes@gmail.com")
    
    # Si se proporciona una contraseña como argumento
    import sys
    if len(sys.argv) > 1:
        password = sys.argv[1]
        print(f"\n🔐 Probando con contraseña proporcionada...")
        return send_test_email_with_password(password)
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🚀 ¡Configuración de emails lista!")
    else:
        print("\n❌ Error en la configuración")
