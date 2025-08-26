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
                <title>Restablecimiento de Contraseña</title>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background-color: #3B82F6; color: white; padding: 20px; text-align: center; }}
                    .content {{ padding: 20px; background-color: #f9f9f9; }}
                    .button {{ display: inline-block; background-color: #3B82F6; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                    .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>PAQUETES EL CLUB</h1>
                        <p>Restablecimiento de Contraseña</p>
                    </div>
                    <div class="content">
                        <h2>Hola {user.first_name},</h2>
                        <p>Has solicitado restablecer tu contraseña en PAQUETES EL CLUB.</p>
                        <p>Haz clic en el siguiente botón para crear una nueva contraseña:</p>
                        <div style="text-align: center;">
                            <a href="{reset_url}" class="button">Restablecer Contraseña</a>
                        </div>
                        <p><strong>Este enlace expirará en 1 hora por seguridad.</strong></p>
                        <p>Si no solicitaste este cambio, puedes ignorar este email.</p>
                        <p>Si tienes problemas con el botón, copia y pega este enlace en tu navegador:</p>
                        <p style="word-break: break-all; color: #666;">{reset_url}</p>
                    </div>
                    <div class="footer">
                        <p>Este es un email automático, no respondas a este mensaje.</p>
                        <p>PAQUETES EL CLUB - Sistema de Gestión de Paquetería</p>
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
