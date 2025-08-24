# ========================================
# PAQUETES EL CLUB v3.0 - Servicio de Notificaciones
# ========================================

from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
from datetime import datetime

from ..models.notification import Notification, NotificationType, NotificationStatus
from ..models.package import Package
from ..utils.exceptions import NotificationException
from ..config import settings

class NotificationService:
    """Servicio para la lógica de negocio de notificaciones"""
    
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
    
    async def _send_email(self, to_email: str, subject: str, message: str) -> bool:
        """Enviar email usando SMTP (simulado)"""
        # Aquí se implementaría el envío real de email
        # Por ahora solo simulamos
        print(f"Email simulado a {to_email}: {subject} - {message}")
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
