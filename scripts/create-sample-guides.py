#!/usr/bin/env python3
"""
Script para Crear Guías de Muestra - PAQUETES EL CLUB v3.1
==========================================================

Crea guías de muestra con diferentes estados y tiempos para visualizar:
- Flujos completos (ANUNCIADO -> RECIBIDO -> ENTREGADO)
- Flujos parciales (ANUNCIADO -> RECIBIDO)
- Cancelaciones tempranas y tardías
- Diferentes tiempos de procesamiento
- Estados en tiempo real
"""

import requests
import json
import random
from datetime import datetime, timedelta
import time

def create_sample_guides():
    """Crea guías de muestra con diferentes estados"""
    print("🚀 CREANDO GUÍAS DE MUESTRA CON DIFERENTES ESTADOS")
    print("=" * 70)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    base_url = "http://localhost"
    api_url = f"{base_url}/api/announcements"
    
    # Datos de clientes de muestra
    sample_customers = [
        {"name": "María González", "phone": "3001234567"},
        {"name": "Carlos Rodríguez", "phone": "3002345678"},
        {"name": "Ana Martínez", "phone": "3003456789"},
        {"name": "Luis Pérez", "phone": "3004567890"},
        {"name": "Sofia López", "phone": "3005678901"},
        {"name": "Diego Ramírez", "phone": "3006789012"},
        {"name": "Valentina Torres", "phone": "3007890123"},
        {"name": "Andrés Silva", "phone": "3008901234"},
        {"name": "Camila Vargas", "phone": "3009012345"},
        {"name": "Juan Morales", "phone": "3000123456"},
        {"name": "Isabella Castro", "phone": "3001234568"},
        {"name": "Mateo Herrera", "phone": "3002345679"},
        {"name": "Valeria Jiménez", "phone": "3003456780"},
        {"name": "Nicolás Ruiz", "phone": "3004567891"},
        {"name": "Daniela Moreno", "phone": "3005678902"},
        {"name": "Sebastián Ortiz", "phone": "3006789013"},
        {"name": "Gabriela Rojas", "phone": "3007890124"},
        {"name": "Felipe Mendoza", "phone": "3008901235"},
        {"name": "Laura Vega", "phone": "3009012346"},
        {"name": "Alejandro Guzmán", "phone": "3000123457"}
    ]
    
    # Definir diferentes flujos de estados
    flow_patterns = [
        # Flujos completos (ANUNCIADO -> RECIBIDO -> ENTREGADO)
        {"name": "Flujo Completo Rápido", "states": ["RECIBIDO", "ENTREGADO"], "time_range": (1, 3)},
        {"name": "Flujo Completo Normal", "states": ["RECIBIDO", "ENTREGADO"], "time_range": (3, 7)},
        {"name": "Flujo Completo Lento", "states": ["RECIBIDO", "ENTREGADO"], "time_range": (7, 15)},
        
        # Flujos parciales (ANUNCIADO -> RECIBIDO)
        {"name": "Solo Recibido Rápido", "states": ["RECIBIDO"], "time_range": (1, 2)},
        {"name": "Solo Recibido Normal", "states": ["RECIBIDO"], "time_range": (2, 5)},
        {"name": "Solo Recibido Lento", "states": ["RECIBIDO"], "time_range": (5, 10)},
        
        # Cancelaciones
        {"name": "Cancelación Temprana", "states": ["CANCELADO"], "time_range": (1, 2)},
        {"name": "Cancelación Tardía", "states": ["RECIBIDO", "CANCELADO"], "time_range": (3, 7)},
        
        # Estados especiales
        {"name": "En Proceso", "states": ["RECIBIDO"], "time_range": (1, 3)},
        {"name": "Pendiente de Entrega", "states": ["RECIBIDO"], "time_range": (5, 10)},
        {"name": "Retrasado", "states": ["RECIBIDO"], "time_range": (10, 15)},
        {"name": "Cancelado por Cliente", "states": ["CANCELADO"], "time_range": (2, 5)},
        {"name": "Cancelado por Sistema", "states": ["CANCELADO"], "time_range": (1, 3)},
        {"name": "Entregado con Retraso", "states": ["RECIBIDO", "ENTREGADO"], "time_range": (8, 12)},
        {"name": "Entregado Anticipado", "states": ["RECIBIDO", "ENTREGADO"], "time_range": (1, 2)},
        {"name": "Procesamiento Normal", "states": ["RECIBIDO", "ENTREGADO"], "time_range": (4, 6)},
        {"name": "Procesamiento Rápido", "states": ["RECIBIDO", "ENTREGADO"], "time_range": (2, 4)},
        {"name": "Procesamiento Lento", "states": ["RECIBIDO", "ENTREGADO"], "time_range": (6, 10)},
        {"name": "Recepción Inmediata", "states": ["RECIBIDO"], "time_range": (1, 1)},
        {"name": "Recepción Programada", "states": ["RECIBIDO"], "time_range": (3, 5)},
        {"name": "Entrega Express", "states": ["RECIBIDO", "ENTREGADO"], "time_range": (1, 2)},
        {"name": "Entrega Estándar", "states": ["RECIBIDO", "ENTREGADO"], "time_range": (5, 8)}
    ]
    
    created_guides = []
    successful_creations = 0
    
    print(f"\n📝 Creando {len(flow_patterns)} guías con diferentes flujos...")
    print("-" * 70)
    
    for i, pattern in enumerate(flow_patterns, 1):
        # Seleccionar cliente aleatorio
        customer = random.choice(sample_customers)
        
        # Crear datos del anuncio
        guide_data = {
            "customer_name": customer["name"],
            "guide_number": f"SAMPLE{i:03d}",
            "phone_number": customer["phone"]
        }
        
        print(f"\n🔍 Creando guía {i}/{len(flow_patterns)}: {pattern['name']}")
        print(f"   Cliente: {customer['name']}")
        print(f"   Guía: {guide_data['guide_number']}")
        print(f"   Estados: {' -> '.join(['ANUNCIADO'] + pattern['states'])}")
        print(f"   Tiempo: {pattern['time_range'][0]}-{pattern['time_range'][1]} días")
        
        try:
            # Crear anuncio
            response = requests.post(api_url, json=guide_data)
            
            if response.status_code == 200:
                announcement = response.json()
                tracking_code = announcement["tracking_code"]
                
                print(f"   ✅ Creado exitosamente - Código: {tracking_code}")
                
                # Agregar a la lista de guías creadas
                created_guides.append({
                    "guide_number": guide_data["guide_number"],
                    "tracking_code": tracking_code,
                    "customer_name": customer["name"],
                    "pattern": pattern["name"],
                    "states": pattern["states"],
                    "time_range": pattern["time_range"]
                })
                
                successful_creations += 1
                
            elif response.status_code == 429:
                print(f"   ⏳ Rate limit alcanzado, esperando...")
                time.sleep(60)  # Esperar 1 minuto
                # Reintentar
                response = requests.post(api_url, json=guide_data)
                if response.status_code == 200:
                    announcement = response.json()
                    tracking_code = announcement["tracking_code"]
                    print(f"   ✅ Creado exitosamente después de espera - Código: {tracking_code}")
                    created_guides.append({
                        "guide_number": guide_data["guide_number"],
                        "tracking_code": tracking_code,
                        "customer_name": customer["name"],
                        "pattern": pattern["name"],
                        "states": pattern["states"],
                        "time_range": pattern["time_range"]
                    })
                    successful_creations += 1
                else:
                    print(f"   ❌ Error después de espera: {response.status_code}")
            else:
                print(f"   ❌ Error: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"   ❌ Excepción: {e}")
        
        # Pequeña pausa entre creaciones
        time.sleep(1)
    
    # Resumen de creación
    print("\n" + "=" * 70)
    print("📊 RESUMEN DE GUÍAS CREADAS")
    print("=" * 70)
    print(f"Total de patrones: {len(flow_patterns)}")
    print(f"Guías creadas exitosamente: {successful_creations}")
    print(f"Tasa de éxito: {(successful_creations/len(flow_patterns))*100:.1f}%")
    
    # Mostrar guías creadas
    print(f"\n📋 GUÍAS CREADAS:")
    print("-" * 70)
    for guide in created_guides:
        print(f"📦 {guide['guide_number']} | {guide['tracking_code']} | {guide['customer_name']}")
        print(f"   Patrón: {guide['pattern']}")
        print(f"   Estados: {' -> '.join(['ANUNCIADO'] + guide['states'])}")
        print(f"   Tiempo: {guide['time_range'][0]}-{guide['time_range'][1]} días")
        print()
    
    # Guardar en archivo para referencia
    with open("sample_guides_created.json", "w", encoding="utf-8") as f:
        json.dump(created_guides, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"💾 Información guardada en: sample_guides_created.json")
    
    # Instrucciones para visualizar
    print(f"\n🎯 INSTRUCCIONES PARA VISUALIZAR:")
    print("-" * 70)
    print("1. Ve a http://localhost/")
    print("2. Usa cualquiera de los códigos de tracking mostrados arriba")
    print("3. Observa los diferentes flujos y tiempos")
    print("4. Compara los estados y tiempos entre guías")
    
    print(f"\n🔍 EJEMPLOS DE CÓDIGOS PARA PROBAR:")
    print("-" * 70)
    for i, guide in enumerate(created_guides[:10], 1):  # Mostrar primeros 10
        print(f"{i:2d}. {guide['tracking_code']} - {guide['pattern']}")
    
    if len(created_guides) > 10:
        print(f"    ... y {len(created_guides) - 10} más")
    
    print(f"\n✅ ¡Guías de muestra creadas exitosamente!")
    print(f"🎨 Ahora puedes visualizar diferentes flujos y tiempos en el sistema")

if __name__ == "__main__":
    create_sample_guides()
