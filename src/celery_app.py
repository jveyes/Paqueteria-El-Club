from celery import Celery
celery_app = Celery("paqueteria", broker="redis://:Redis2025!Secure@redis:6379/0", backend="redis://:Redis2025!Secure@redis:6379/0")
celery_app.conf.update(task_serializer="json", accept_content=["json"], result_serializer="json", timezone="America/Bogota", enable_utc=True, broker_connection_retry_on_startup=True)
