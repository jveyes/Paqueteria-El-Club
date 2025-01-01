#!/usr/bin/env python3
# ========================================
# PAQUETES EL CLUB v3.1 - Crear Datos de Muestra
# ========================================

import sys
import os
import asyncio
import logging
from datetime import datetime, timedelta
import uuid

# Agregar el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.database.database import get_db
from src.models.user import User, UserRole
from src.models.customer import Customer
from src.models.package import Package, PackageStatus
from src.models.announcement import PackageAnnouncement
from src.services.user_service import UserService
from src.utils.datetime_utils import get_colombia_now

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_sample_data():
    """Crear datos de muestra para el dashboard"""
    print("🎯 CREANDO DATOS DE MUESTRA PARA EL DASHBOARD")
    print("=" * 50)
    
    # Crear sesión de base de datos
    db = next(get_db())
    
    try:
        # 1. Crear clientes de muestra
        print("\n👥 1. CREANDO CLIENTES DE MUESTRA")
        print("-" * 30)
        
        customers_data = [
            {
                "name": "María González",
                "phone": "3001234567",
                "tracking_number": "CUST001"
            },
            {
                "name": "Carlos Rodríguez",
                "phone": "3109876543",
                "tracking_number": "CUST002"
            },
            {
                "name": "Ana Martínez",
                "phone": "3155551234",
                "tracking_number": "CUST003"
            },
            {
                "name": "Luis Pérez",
                "phone": "3207778888",
                "tracking_number": "CUST004"
            },
            {
                "name": "Sofia Herrera",
                "phone": "3114445555",
                "tracking_number": "CUST005"
            }
        ]
        
        customers = []
        for customer_data in customers_data:
            customer = Customer(
                name=customer_data["name"],
                phone=customer_data["phone"],
                tracking_number=customer_data["tracking_number"]
            )
            db.add(customer)
            customers.append(customer)
            print(f"   ✅ Cliente creado: {customer.name}")
        
        db.commit()
        print(f"   📊 Total clientes creados: {len(customers)}")
        
        # 2. Crear paquetes de muestra
        print("\n📦 2. CREANDO PAQUETES DE MUESTRA")
        print("-" * 30)
        
        packages_data = [
            {
                "tracking_number": "PKG001",
                "customer": customers[0],
                "status": PackageStatus.ANUNCIADO,
                "weight": 2.5,
                "dimensions": "30x20x15",
                "description": "Ropa y accesorios",
                "created_at": get_colombia_now() - timedelta(days=5)
            },
            {
                "tracking_number": "PKG002",
                "customer": customers[1],
                "status": PackageStatus.ENTREGADO,
                "weight": 1.8,
                "dimensions": "25x18x12",
                "description": "Electrónicos",
                "created_at": get_colombia_now() - timedelta(days=3),
                "delivered_at": get_colombia_now() - timedelta(days=1)
            },
            {
                "tracking_number": "PKG003",
                "customer": customers[2],
                "status": PackageStatus.ANUNCIADO,
                "weight": 3.2,
                "dimensions": "35x25x20",
                "description": "Libros y documentos",
                "created_at": get_colombia_now() - timedelta(days=2)
            },
            {
                "tracking_number": "PKG004",
                "customer": customers[3],
                "status": PackageStatus.ENTREGADO,
                "weight": 0.8,
                "dimensions": "20x15x10",
                "description": "Medicamentos",
                "created_at": get_colombia_now() - timedelta(days=7),
                "delivered_at": get_colombia_now() - timedelta(days=4)
            },
            {
                "tracking_number": "PKG005",
                "customer": customers[4],
                "status": PackageStatus.ANUNCIADO,
                "weight": 4.1,
                "dimensions": "40x30x25",
                "description": "Herramientas",
                "created_at": get_colombia_now() - timedelta(hours=6)
            },
            {
                "tracking_number": "PKG006",
                "customer": customers[0],
                "status": PackageStatus.ENTREGADO,
                "weight": 1.5,
                "dimensions": "22x16x12",
                "description": "Cosméticos",
                "created_at": get_colombia_now() - timedelta(days=10),
                "delivered_at": get_colombia_now() - timedelta(days=8)
            }
        ]
        
        packages = []
        for package_data in packages_data:
            package = Package(
                tracking_number=package_data["tracking_number"],
                customer_id=package_data["customer"].id,
                status=package_data["status"],
                weight=package_data["weight"],
                dimensions=package_data["dimensions"],
                description=package_data["description"],
                created_at=package_data["created_at"]
            )
            
            if package_data["status"] == PackageStatus.ENTREGADO:
                package.delivered_at = package_data["delivered_at"]
            
            db.add(package)
            packages.append(package)
            print(f"   ✅ Paquete creado: {package.tracking_number} - {package.status.value}")
        
        db.commit()
        print(f"   📊 Total paquetes creados: {len(packages)}")
        
        # 3. Crear anuncios de muestra
        print("\n📢 3. CREANDO ANUNCIOS DE MUESTRA")
        print("-" * 30)
        
        announcements_data = [
            {
                "guide_number": "GUIDE001",
                "customer_name": "Pedro López",
                "phone_number": "3001112222",
                "is_processed": False,
                "announced_at": get_colombia_now() - timedelta(hours=2)
            },
            {
                "guide_number": "GUIDE002",
                "customer_name": "Carmen Silva",
                "phone_number": "3103334444",
                "is_processed": True,
                "announced_at": get_colombia_now() - timedelta(days=1)
            },
            {
                "guide_number": "GUIDE003",
                "customer_name": "Roberto Díaz",
                "phone_number": "3155556666",
                "is_processed": False,
                "announced_at": get_colombia_now() - timedelta(hours=4)
            },
            {
                "guide_number": "GUIDE004",
                "customer_name": "Patricia Ruiz",
                "phone_number": "3207778888",
                "is_processed": True,
                "announced_at": get_colombia_now() - timedelta(days=2)
            },
            {
                "guide_number": "GUIDE005",
                "customer_name": "Fernando Morales",
                "phone_number": "3119990000",
                "is_processed": False,
                "announced_at": get_colombia_now() - timedelta(hours=1)
            }
        ]
        
        announcements = []
        for announcement_data in announcements_data:
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
        
        db.commit()
        print(f"   📊 Total anuncios creados: {len(announcements)}")
        
        # 4. Mostrar resumen final
        print("\n📊 RESUMEN DE DATOS CREADOS")
        print("=" * 50)
        
        total_customers = db.query(Customer).count()
        total_packages = db.query(Package).count()
        pending_packages = db.query(Package).filter(Package.status == PackageStatus.ANUNCIADO).count()
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
        print(f"   ⏳ Paquetes pendientes: {pending_packages}")
        print(f"   ✅ Paquetes entregados: {delivered_packages}")
        print(f"   📢 Anuncios totales: {total_announcements}")
        print(f"   ⏳ Anuncios pendientes: {pending_announcements}")
        print(f"   ✅ Anuncios procesados: {processed_announcements}")
        
        print("\n🎉 DATOS DE MUESTRA CREADOS EXITOSAMENTE")
        print("💡 Ahora puedes ver el dashboard con datos reales en:")
        print("   http://localhost:8001/dashboard")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR CREANDO DATOS: {e}")
        logger.error(f"Error creando datos de muestra: {e}", exc_info=True)
        return False
        
    finally:
        db.close()

def main():
    """Función principal"""
    print("🚀 INICIANDO CREACIÓN DE DATOS DE MUESTRA")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    success = create_sample_data()
    
    if success:
        print("\n✅ Proceso completado exitosamente")
    else:
        print("\n❌ Error en el proceso")

if __name__ == "__main__":
    main()
