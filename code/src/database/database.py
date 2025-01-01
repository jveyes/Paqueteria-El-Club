# ========================================
# PAQUETES EL CLUB v3.1 - Configuración de Base de Datos
# ========================================

from sqlalchemy import create_engine, event, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..config import settings
import logging

logger = logging.getLogger(__name__)

# Crear URL de conexión con configuración de timezone
database_url = settings.database_url

# Crear engine con configuración específica para PostgreSQL AWS RDS
engine = create_engine(
    database_url,
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args={
        "options": "-c timezone=America/Bogota"  # Configurar timezone de Colombia
    }
)

# Configurar timezone en cada conexión para PostgreSQL AWS RDS
@event.listens_for(engine, "connect")
def set_timezone(dbapi_connection, connection_record):
    """Configurar timezone de Colombia en cada conexión"""
    cursor = dbapi_connection.cursor()
    cursor.execute("SET timezone = 'America/Bogota';")
    cursor.close()

# Crear sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos
Base = declarative_base()

def get_db():
    """Obtener sesión de base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Inicializar base de datos"""
    try:
        # Crear todas las tablas
        Base.metadata.create_all(bind=engine)
        logger.info("Base de datos AWS RDS inicializada correctamente")
        
        # Verificar timezone para PostgreSQL AWS RDS
        db = SessionLocal()
        result = db.execute(text("SHOW timezone;")).fetchone()
        logger.info(f"Timezone configurado: {result[0]}")
        db.close()
        
    except Exception as e:
        logger.error(f"Error inicializando base de datos AWS RDS: {e}")
        raise
