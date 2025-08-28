# ========================================
# PAQUETES EL CLUB v3.0 - Servicio de Notificaciones
# ========================================

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
import logging

from ..models.notification import Notification, NotificationType, NotificationStatus
from ..models.package import Package
from ..models.user import User, PasswordResetToken
from ..utils.exceptions import NotificationException
from ..config import settings

# Configurar logging
logger = logging.getLogger(__name__)

class NotificationService:
    """Servicio para manejo de notificaciones"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def send_package_announcement(self, package: Package) -> Notification:
        """Enviar notificación de anuncio de paquete"""
        message = f"Su paquete {package.tracking_number} ha sido anunciado. Costo total: ${package.total_cost:,.0f}"
        
        # Crear notificación en BD
        notification = Notification(
            package_id=package.id,
            notification_type=NotificationType.SMS,
            message=message,
            status=NotificationStatus.PENDING
        )
        
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        
        # Enviar SMS (simulado por ahora)
        try:
            await self._send_sms(package.customer_phone, message)
            notification.status = NotificationStatus.SENT
            notification.sent_at = datetime.now()
        except Exception as e:
            notification.status = NotificationStatus.FAILED
            raise NotificationException("SMS", str(e))
        finally:
            self.db.commit()
        
        return notification
    
    async def send_package_received(self, package: Package) -> Notification:
        """Enviar notificación de paquete recibido"""
        message = f"Su paquete {package.tracking_number} ha sido recibido en nuestras instalaciones."
        
        notification = Notification(
            package_id=package.id,
            notification_type=NotificationType.SMS,
            message=message,
            status=NotificationStatus.PENDING
        )
        
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        
        try:
            await self._send_sms(package.customer_phone, message)
            notification.status = NotificationStatus.SENT
            notification.sent_at = datetime.now()
        except Exception as e:
            notification.status = NotificationStatus.FAILED
            raise NotificationException("SMS", str(e))
        finally:
            self.db.commit()
        
        return notification
    
    async def send_package_delivered(self, package: Package) -> Notification:
        """Enviar notificación de paquete entregado"""
        message = f"Su paquete {package.tracking_number} ha sido entregado exitosamente."
        
        notification = Notification(
            package_id=package.id,
            notification_type=NotificationType.SMS,
            message=message,
            status=NotificationStatus.PENDING
        )
        
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        
        try:
            await self._send_sms(package.customer_phone, message)
            notification.status = NotificationStatus.SENT
            notification.sent_at = datetime.now()
        except Exception as e:
            notification.status = NotificationStatus.FAILED
            raise NotificationException("SMS", str(e))
        finally:
            self.db.commit()
        
        return notification
    
    async def send_package_cancelled(self, package: Package, reason: str) -> Notification:
        """Enviar notificación de paquete cancelado"""
        message = f"Su paquete {package.tracking_number} ha sido cancelado. Motivo: {reason}"
        
        notification = Notification(
            package_id=package.id,
            notification_type=NotificationType.SMS,
            message=message,
            status=NotificationStatus.PENDING
        )
        
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        
        try:
            await self._send_sms(package.customer_phone, message)
            notification.status = NotificationStatus.SENT
            notification.sent_at = datetime.now()
        except Exception as e:
            notification.status = NotificationStatus.FAILED
            raise NotificationException("SMS", str(e))
        finally:
            self.db.commit()
        
        return notification
    
    async def send_email_notification(
        self,
        to_email: str,
        subject: str,
        message: str,
        package_id: Optional[str] = None
    ) -> Notification:
        """Enviar notificación por email"""
        notification = Notification(
            package_id=package_id,
            notification_type=NotificationType.EMAIL,
            message=message,
            status=NotificationStatus.PENDING
        )
        
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        
        try:
            await self._send_email(to_email, subject, message)
            notification.status = NotificationStatus.SENT
            notification.sent_at = datetime.now()
        except Exception as e:
            notification.status = NotificationStatus.FAILED
            raise NotificationException("EMAIL", str(e))
        finally:
            self.db.commit()
        
        return notification
    
    async def send_password_reset_email(self, user: User, reset_token: str) -> bool:
        """Enviar email de restablecimiento de contraseña"""
        try:
            # Crear el enlace de reset
            reset_url = f"http://localhost/auth/reset-password?token={reset_token}"
            
            # Contenido del email
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
                        <div class="greeting">¡Hola {user.first_name}!</div>
                        
                        <div class="message">
                            Has solicitado restablecer tu contraseña en <strong>PAQUETES EL CLUB</strong>, nuestro sistema de gestión de paquetería.
                        </div>
                        
                        <div class="message">
                            Haz clic en el siguiente botón para crear una nueva contraseña de forma segura:
                        </div>
                        
                        <div class="button-container">
                            <a href="{reset_url}" class="button" style="display: inline-block; background-color: #3B82F6; color: white !important; padding: 15px 30px; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 16px;">
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
            
            # Intentar enviar email real
            email_sent = await self._send_email_real(user.email, subject, html_content)
            
            if email_sent:
                logger.info(f"Email de reset enviado exitosamente a {user.email}")
                return True
            else:
                # Si falla el envío real, simular en desarrollo
                if settings.environment == "development":
                    logger.warning(f"Fallback a modo desarrollo para {user.email}")
                    print(f"📧 Email de reset simulado para {user.email}")
                    print(f"   Enlace: {reset_url}")
                    return True
                else:
                    logger.error(f"Error enviando email de reset a {user.email}")
                    return False
            
        except Exception as e:
            logger.error(f"Error en send_password_reset_email: {e}")
            return False
    
    async def _send_email_real(self, to_email: str, subject: str, html_content: str) -> bool:
        """Enviar email usando SMTP real"""
        try:
            # Crear mensaje
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{settings.smtp_from_name} <{settings.smtp_from_email}>"
            msg['To'] = to_email
            
            # Agregar contenido HTML
            html_part = MIMEText(html_content, 'html', 'utf-8')
            msg.attach(html_part)
            
            # Configurar contexto SSL
            context = ssl.create_default_context()
            
            # Conectar al servidor SMTP
            logger.info(f"Conectando a SMTP: {settings.smtp_host}:{settings.smtp_port}")
            
            with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
                server.starttls(context=context)  # Habilitar TLS
                
                # Autenticación
                logger.info(f"Autenticando con usuario: {settings.smtp_user}")
                server.login(settings.smtp_user, settings.smtp_password)
                
                # Enviar email
                server.send_message(msg)
                logger.info(f"Email enviado exitosamente a {to_email}")
                return True
                
        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"Error de autenticación SMTP: {e}")
            return False
        except smtplib.SMTPRecipientsRefused as e:
            logger.error(f"Destinatario rechazado: {e}")
            return False
        except smtplib.SMTPServerDisconnected as e:
            logger.error(f"Servidor SMTP desconectado: {e}")
            return False
        except Exception as e:
            logger.error(f"Error enviando email a {to_email}: {e}")
            return False
    
    async def _send_email(self, to_email: str, subject: str, message: str) -> bool:
        """Enviar email usando SMTP"""
        return await self._send_email_real(to_email, subject, message)
    
    async def _send_sms(self, phone: str, message: str) -> bool:
        """Enviar SMS usando LIWA.co (simulado)"""
        # Aquí se implementaría la integración real con LIWA.co
        # Por ahora solo simulamos el envío
        if not settings.liwa_api_key:
            # En desarrollo, solo log
            logger.info(f"SMS simulado a {phone}: {message}")
            return True
        
        # Implementación real con LIWA.co
        # import httpx
        # async with httpx.AsyncClient() as client:
        #     response = await client.post(
        #         "https://api.liwa.co/send-sms",
        #         headers={"Authorization": f"Bearer {settings.liwa_api_key}"},
        #         json={
        #             "to": phone,
        #             "message": message,
        #             "from": settings.liwa_from_name
        #         }
        #     )
        #     return response.status_code == 200
        
        return True
    
    def get_notification_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas de notificaciones"""
        total_notifications = self.db.query(Notification).count()
        
        # Notificaciones por estado
        status_counts = self.db.query(
            Notification.status,
            self.db.func.count(Notification.id)
        ).group_by(Notification.status).all()
        
        status_stats = {status.value: count for status, count in status_counts}
        
        # Notificaciones por tipo
        type_counts = self.db.query(
            Notification.notification_type,
            self.db.func.count(Notification.id)
        ).group_by(Notification.notification_type).all()
        
        type_stats = {ntype.value: count for ntype, count in type_counts}
        
        return {
            "total_notifications": total_notifications,
            "status_distribution": status_stats,
            "type_distribution": type_stats
        }
