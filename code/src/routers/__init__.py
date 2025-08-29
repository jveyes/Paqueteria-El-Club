# ========================================
# PAQUETES EL CLUB v3.1 - Routers
# ========================================

# Importar routers principales
from . import auth, packages, customers, rates, notifications, messages, files, admin, announcements

__all__ = [
    "auth",
    "packages", 
    "customers",
    "rates",
    "notifications",
    "messages",
    "files",
    "admin",
    "announcements"
]
