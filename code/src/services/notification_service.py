# ========================================
# PAQUETES EL CLUB v3.0 - Servicio de Notificaciones
# ========================================

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session

from ..models.notification import Notification, NotificationType, NotificationStatus
from ..models.package import Package
from ..models.user import User, PasswordResetToken
from ..utils.exceptions import NotificationException
from ..config import settings

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
                        background-color: #ffffff;
                    }}
                    .container {{ 
                        max-width: 600px; 
                        margin: 0 auto; 
                        background-color: #ffffff; 
                        padding: 20px;
                    }}
                    .header {{ 
                        text-align: center; 
                        padding: 20px 0; 
                        border-bottom: 1px solid #ccc;
                        margin-bottom: 20px;
                    }}
                    .service-name {{
                        font-size: 20px;
                        font-weight: bold;
                        margin: 0 0 5px 0;
                        color: #333;
                    }}
                    .service-subtitle {{
                        font-size: 14px;
                        margin: 0;
                        color: #666;
                    }}
                    .content {{ 
                        padding: 20px 0;
                    }}
                    .greeting {{
                        font-size: 16px;
                        color: #333;
                        margin-bottom: 15px;
                        font-weight: bold;
                    }}
                    .message {{
                        font-size: 14px;
                        color: #333;
                        margin-bottom: 15px;
                        line-height: 1.5;
                    }}
                    .button-container {{
                        text-align: center;
                        margin: 25px 0;
                    }}
                    .button {{ 
                        display: inline-block; 
                        background-color: #007bff; 
                        color: white; 
                        padding: 12px 25px; 
                        text-decoration: none; 
                        border-radius: 4px; 
                        font-weight: bold;
                        font-size: 14px;
                    }}
                    .warning {{
                        background-color: #f9f9f9;
                        border: 1px solid #ddd;
                        padding: 12px;
                        margin: 15px 0;
                        border-radius: 4px;
                        text-align: center;
                        color: #333;
                        font-size: 13px;
                    }}
                    .link-container {{
                        background-color: #f9f9f9;
                        border: 1px solid #ddd;
                        border-radius: 4px;
                        padding: 12px;
                        margin: 15px 0;
                        text-align: center;
                    }}
                    .link-text {{
                        word-break: break-all; 
                        color: #333; 
                        font-family: monospace;
                        font-size: 12px;
                        margin: 5px 0;
                    }}
                    .footer {{ 
                        text-align: center; 
                        padding: 20px 0; 
                        border-top: 1px solid #ccc;
                        margin-top: 20px;
                        color: #666;
                        font-size: 12px;
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
                            Has solicitado restablecer tu contraseña en PAQUETES EL CLUB, nuestro sistema de gestión de paquetería.
                        </div>
                        
                        <div class="message">
                            Haz clic en el siguiente botón para crear una nueva contraseña de forma segura:
                        </div>
                        
                        <div class="button-container">
                            <a href="{reset_url}" class="button">
                                Restablecer Contraseña
                            </a>
                        </div>
                        
                        <div class="warning">
                            <strong>IMPORTANTE:</strong> Este enlace expirará en 1 hora por seguridad.
                        </div>
                        
                        <div class="link-container">
                            <p>Si el botón no funciona, copia y pega este enlace en tu navegador:</p>
                            <p class="link-text">{reset_url}</p>
                        </div>
                    </div>
                    
                    <div class="footer">
                        <p>Si no solicitaste este cambio, puedes ignorar este email de forma segura.</p>
                        <p>Este es un email automático, por favor no respondas a este mensaje.</p>
                        <p>Desarrollado por JEMAVI para PAPYRUS</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            # Enviar email
            return await self._send_email_real(user.email, subject, html_content)
            
        except Exception as e:
            print(f"Error enviando email de reset: {e}")
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
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Conectar al servidor SMTP
            server = smtplib.SMTP(settings.smtp_host, settings.smtp_port)
            server.starttls()  # Habilitar TLS
            
            # Autenticación
            server.login(settings.smtp_user, settings.smtp_password)
            
            # Enviar email
            server.send_message(msg)
            server.quit()
            
            print(f"Email enviado exitosamente a {to_email}")
            return True
            
        except Exception as e:
            print(f"Error enviando email a {to_email}: {e}")
            return False
    
    async def _send_email(self, to_email: str, subject: str, message: str) -> bool:
        """Enviar email usando SMTP (simulado)"""
        # Aquí se implementaría el envío real de email
        # Por ahora solo simulamos
        print(f"Email simulado a {to_email}: {subject} - {message}")
        return True
    
    async def _send_sms(self, phone: str, message: str) -> bool:
        """Enviar SMS usando LIWA.co (simulado)"""
        # Aquí se implementaría la integración real con LIWA.co
        # Por ahora solo simulamos el envío
        if not settings.liwa_api_key:
            # En desarrollo, solo log
            print(f"SMS simulado a {phone}: {message}")
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
