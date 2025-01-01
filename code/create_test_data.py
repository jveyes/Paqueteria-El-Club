#!/usr/bin/env python3
# ========================================
# PAQUETES EL CLUB v3.1 - Crear Datos de Prueba
# ========================================

import sys
import os
import logging
from datetime import datetime, timedelta
import uuid

# Agregar el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.database.database import get_db, init_db
from src.models.user import User, UserRole
from src.models.customer import Customer
from src.models.package import Package, PackageStatus, PackageType, PackageCondition
from src.models.announcement import PackageAnnouncement
from src.utils.datetime_utils import get_colombia_now

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_test_data():
    """Crear datos de prueba para el dashboard"""
    print("🎯 CREANDO DATOS DE PRUEBA PARA EL DASHBOARD")
    print("=" * 50)
    
    # Inicializar base de datos
    init_db()
    
    # Crear sesión de base de datos
    db = next(get_db())
    
    try:
        # 1. Crear clientes de prueba
        print("\n👥 1. CREANDO CLIENTES DE PRUEBA")
        print("-" * 30)
        
        customers_data = [
            {
                "name": "María González",
                "phone": "+573001234567",
                "tracking_number": "CUST001"
            },
            {
                "name": "Carlos Rodríguez", 
                "phone": "+573109876543",
                "tracking_number": "CUST002"
            },
            {
                "name": "Ana Martínez",
                "phone": "+573155551234",
                "tracking_number": "CUST003"
            },
            {
                "name": "Luis Pérez",
                "phone": "+573207778888",
                "tracking_number": "CUST004"
            },
            {
                "name": "Sofia Herrera",
                "phone": "+573114445555",
                "tracking_number": "CUST005"
            }
        ]
        
        customers = []
        for customer_data in customers_data:
            # Verificar si ya existe
            existing = db.query(Customer).filter(
                Customer.tracking_number == customer_data["tracking_number"]
            ).first()
            
            if not existing:
                customer = Customer(
                    name=customer_data["name"],
                    phone=customer_data["phone"],
                    tracking_number=customer_data["tracking_number"]
                )
                db.add(customer)
                customers.append(customer)
                print(f"   ✅ Cliente creado: {customer.name}")
            else:
                customers.append(existing)
                print(f"   ⚠️  Cliente ya existe: {existing.name}")
        
        db.commit()
        print(f"   📊 Total clientes: {len(customers)}")
        
        # 2. Crear paquetes de prueba
        print("\n📦 2. CREANDO PAQUETES DE PRUEBA")
        print("-" * 30)
        
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
        
        # 3. Crear anuncios de prueba
        print("\n📢 3. CREANDO ANUNCIOS DE PRUEBA")
        print("-" * 30)
        
        announcements_data = [
            {
                "guide_number": "GUIDE001",
                "customer_name": "Pedro López",
                "phone_number": "+573001112222",
                "is_processed": False,
                "announced_at": get_colombia_now() - timedelta(hours=2)
            },
            {
                "guide_number": "GUIDE002",
                "customer_name": "Carmen Silva",
                "phone_number": "+573103334444",
                "is_processed": True,
                "announced_at": get_colombia_now() - timedelta(days=1)
            },
            {
                "guide_number": "GUIDE003",
                "customer_name": "Roberto Díaz",
                "phone_number": "+573155556666",
                "is_processed": False,
                "announced_at": get_colombia_now() - timedelta(hours=4)
            },
            {
                "guide_number": "GUIDE004",
                "customer_name": "Patricia Ruiz",
                "phone_number": "+573207778888",
                "is_processed": True,
                "announced_at": get_colombia_now() - timedelta(days=2)
            },
            {
                "guide_number": "GUIDE005",
                "customer_name": "Fernando Morales",
                "phone_number": "+573119990000",
                "is_processed": False,
                "announced_at": get_colombia_now() - timedelta(hours=1)
            }
        ]
        
        announcements = []
        for announcement_data in announcements_data:
            # Verificar si ya existe
            existing = db.query(PackageAnnouncement).filter(
                PackageAnnouncement.guide_number == announcement_data["guide_number"]
            ).first()
            
            if not existing:
                announcement = PackageAnnouncement(
                    guide_number=announcement_data["guide_number"],
                    customer_name=announcement_data["customer_name"],
                    phone_number=announcement_data["phone_number"],
                    is_processed=announcement_data["is_processed"],
                    is_active=True,
                    announced_at=announcement_data["announced_at"]
                )
                db.add(announcement)
                announcements.append(announcement)
                print(f"   ✅ Anuncio creado: {announcement.guide_number} - {'Procesado' if announcement.is_processed else 'Pendiente'}")
            else:
                announcements.append(existing)
                print(f"   ⚠️  Anuncio ya existe: {existing.guide_number}")
        
        db.commit()
        print(f"   📊 Total anuncios: {len(announcements)}")
        
        # 4. Mostrar resumen final
        print("\n📊 RESUMEN DE DATOS CREADOS")
        print("=" * 50)
        
        total_customers = db.query(Customer).count()
        total_packages = db.query(Package).count()
        announced_packages = db.query(Package).filter(Package.status == PackageStatus.ANUNCIADO).count()
        received_packages = db.query(Package).filter(Package.status == PackageStatus.RECIBIDO).count()
        delivered_packages = db.query(Package).filter(Package.status == PackageStatus.ENTREGADO).count()
        total_announcements = db.query(PackageAnnouncement).count()
        pending_announcements = db.query(PackageAnnouncement).filter(
            PackageAnnouncement.is_processed == False
        ).count()
        processed_announcements = db.query(PackageAnnouncement).filter(
            PackageAnnouncement.is_processed == True
        ).count()
        
        print(f"   👥 Clientes: {total_customers}")
        print(f"   📦 Paquetes totales: {total_packages}")
        print(f"   📢 Paquetes anunciados: {announced_packages}")
        print(f"   📥 Paquetes recibidos: {received_packages}")
        print(f"   ✅ Paquetes entregados: {delivered_packages}")
        print(f"   📢 Anuncios totales: {total_announcements}")
        print(f"   ⏳ Anuncios pendientes: {pending_announcements}")
        print(f"   ✅ Anuncios procesados: {processed_announcements}")
        
        print("\n🎉 DATOS DE PRUEBA CREADOS EXITOSAMENTE")
        print("💡 Ahora puedes ver el dashboard con datos reales en:")
        print("   http://localhost:8001/dashboard")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR CREANDO DATOS: {e}")
        logger.error(f"Error creando datos de prueba: {e}", exc_info=True)
        return False
        
    finally:
        db.close()

def main():
    """Función principal"""
    print("🚀 INICIANDO CREACIÓN DE DATOS DE PRUEBA")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    success = create_test_data()
    
    if success:
        print("\n✅ Proceso completado exitosamente")
    else:
        print("\n❌ Error en el proceso")

if __name__ == "__main__":
    main()
