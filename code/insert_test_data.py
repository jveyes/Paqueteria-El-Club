#!/usr/bin/env python3
# ========================================
# PAQUETES EL CLUB v3.1 - Insertar Datos de Prueba
# ========================================

import sys
import os
import logging
from datetime import datetime, timedelta
import uuid

# Agregar el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.database.database import get_db, init_db
from src.models.package import Package, PackageStatus, PackageType, PackageCondition
from src.utils.datetime_utils import get_colombia_now

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def insert_test_packages():
    """Insertar paquetes de prueba para el dashboard"""
    print("🎯 INSERTANDO PAQUETES DE PRUEBA")
    print("=" * 50)
    
    # Inicializar base de datos
    init_db()
    
    # Crear sesión de base de datos
    db = next(get_db())
    
    try:
        # Crear paquetes de prueba
        packages_data = [
            {
                "tracking_number": "PKG001",
                "customer_name": "María González",
                "customer_phone": "+573001234567",
                "status": PackageStatus.ANUNCIADO,
                "package_type": PackageType.NORMAL,
                "package_condition": PackageCondition.BUENO,
                "observations": "Ropa y accesorios",
                "created_at": get_colombia_now() - timedelta(days=5)
            },
            {
                "tracking_number": "PKG002",
                "customer_name": "Carlos Rodríguez",
                "customer_phone": "+573109876543", 
                "status": PackageStatus.ENTREGADO,
                "package_type": PackageType.NORMAL,
                "package_condition": PackageCondition.BUENO,
                "observations": "Electrónicos",
                "created_at": get_colombia_now() - timedelta(days=3),
                "delivered_at": get_colombia_now() - timedelta(days=1)
            },
            {
                "tracking_number": "PKG003",
                "customer_name": "Ana Martínez",
                "customer_phone": "+573155551234",
                "status": PackageStatus.ANUNCIADO,
                "package_type": PackageType.NORMAL,
                "package_condition": PackageCondition.BUENO,
                "observations": "Libros y documentos",
                "created_at": get_colombia_now() - timedelta(days=2)
            },
            {
                "tracking_number": "PKG004",
                "customer_name": "Luis Pérez",
                "customer_phone": "+573207778888",
                "status": PackageStatus.RECIBIDO,
                "package_type": PackageType.NORMAL,
                "package_condition": PackageCondition.BUENO,
                "observations": "Medicamentos",
                "created_at": get_colombia_now() - timedelta(days=1),
                "received_at": get_colombia_now() - timedelta(hours=6)
            },
            {
                "tracking_number": "PKG005",
                "customer_name": "Sofia Herrera",
                "customer_phone": "+573114445555",
                "status": PackageStatus.ANUNCIADO,
                "package_type": PackageType.NORMAL,
                "package_condition": PackageCondition.BUENO,
                "observations": "Herramientas",
                "created_at": get_colombia_now() - timedelta(hours=6)
            },
            {
                "tracking_number": "PKG006",
                "customer_name": "María González",
                "customer_phone": "+573001234567",
                "status": PackageStatus.ENTREGADO,
                "package_type": PackageType.NORMAL,
                "package_condition": PackageCondition.BUENO,
                "observations": "Cosméticos",
                "created_at": get_colombia_now() - timedelta(days=10),
                "delivered_at": get_colombia_now() - timedelta(days=8)
            }
        ]
        
        packages = []
        for package_data in packages_data:
            # Verificar si ya existe
            existing = db.query(Package).filter(
                Package.tracking_number == package_data["tracking_number"]
            ).first()
            
            if not existing:
                package = Package(
                    tracking_number=package_data["tracking_number"],
                    customer_name=package_data["customer_name"],
                    customer_phone=package_data["customer_phone"],
                    status=package_data["status"],
                    package_type=package_data["package_type"],
                    package_condition=package_data["package_condition"],
                    observations=package_data["observations"],
                    storage_cost=25000.0,
                    delivery_cost=5000.0,
                    total_cost=30000.0,
                    announced_at=package_data["created_at"]
                )
                
                if package_data["status"] == PackageStatus.ENTREGADO:
                    package.delivered_at = package_data["delivered_at"]
                elif package_data["status"] == PackageStatus.RECIBIDO:
                    package.received_at = package_data["received_at"]
                
                db.add(package)
                packages.append(package)
                print(f"   ✅ Paquete creado: {package.tracking_number} - {package.status.value}")
            else:
                packages.append(existing)
                print(f"   ⚠️  Paquete ya existe: {existing.tracking_number}")
        
        db.commit()
        print(f"   📊 Total paquetes: {len(packages)}")
        
        # Mostrar resumen final
        print("\n📊 RESUMEN DE PAQUETES")
        print("=" * 50)
        
        total_packages = db.query(Package).count()
        announced_packages = db.query(Package).filter(Package.status == PackageStatus.ANUNCIADO).count()
        received_packages = db.query(Package).filter(Package.status == PackageStatus.RECIBIDO).count()
        delivered_packages = db.query(Package).filter(Package.status == PackageStatus.ENTREGADO).count()
        
        print(f"   📦 Paquetes totales: {total_packages}")
        print(f"   📢 Paquetes anunciados: {announced_packages}")
        print(f"   📥 Paquetes recibidos: {received_packages}")
        print(f"   ✅ Paquetes entregados: {delivered_packages}")
        
        print("\n🎉 PAQUETES DE PRUEBA INSERTADOS EXITOSAMENTE")
        print("💡 Ahora puedes ver el dashboard con datos reales en:")
        print("   http://localhost/dashboard")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR INSERTANDO DATOS: {e}")
        logger.error(f"Error insertando datos de prueba: {e}", exc_info=True)
        return False
        
    finally:
        db.close()

def main():
    """Función principal"""
    print("🚀 INICIANDO INSERCIÓN DE PAQUETES DE PRUEBA")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    success = insert_test_packages()
    
    if success:
        print("\n✅ Proceso completado exitosamente")
    else:
        print("\n❌ Error en el proceso")

if __name__ == "__main__":
    main()

