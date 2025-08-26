# ========================================
# PAQUETES EL CLUB v3.1 - Configuración Celery Optimizada
# ========================================

from celery import Celery

celery_app = Celery(
    "paqueteria", 
    broker="redis://redis:6379/0", 
    backend="redis://redis:6379/0"
)

# Configuración optimizada para 50 usuarios
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="America/Bogota",
    enable_utc=True,
    broker_connection_retry_on_startup=True,
    # Optimizaciones para poca RAM
    worker_concurrency=2,  # 2 workers para 50 usuarios
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    worker_max_tasks_per_child=500,  # Reiniciar worker cada 500 tareas
    task_soft_time_limit=300,  # 5 minutos máximo por tarea
    task_time_limit=600,  # 10 minutos máximo por tarea
    # Configuración de Redis
    broker_transport_options={
        'visibility_timeout': 3600,
        'fanout_prefix': True,
        'fanout_patterns': True
    }
)
