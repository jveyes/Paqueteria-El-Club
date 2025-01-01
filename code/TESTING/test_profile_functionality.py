#!/usr/bin/env python3
# ========================================
# PAQUETES EL CLUB v3.1 - Test de Funcionalidades de Perfil
# ========================================

import sys
import os
import asyncio
import json
from datetime import datetime

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.main import app
from src.database.database import get_db, Base
from src.models.user import User, UserRole
from src.models.user_activity_log import UserActivityLog, ActivityType
from src.services.user_service import UserService
from src.services.activity_log_service import ActivityLogService
from src.utils.auth import get_password_hash

# Configurar base de datos de prueba
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

def setup_test_database():
    """Configurar base de datos de prueba"""
    Base.metadata.create_all(bind=engine)
    
    # Crear usuario de prueba
    db = TestingSessionLocal()
    try:
        # Verificar si ya existe un usuario admin
        admin_user = db.query(User).filter(User.role == UserRole.ADMIN).first()
        if not admin_user:
            admin_user = User(
                username="admin_test",
                email="admin@test.com",
                full_name="Admin Test",
                hashed_password=get_password_hash("admin123"),
                role=UserRole.ADMIN,
                is_active=True
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
        
        # Crear usuario operador de prueba
        operator_user = db.query(User).filter(User.username == "operator_test").first()
        if not operator_user:
            operator_user = User(
                username="operator_test",
                email="operator@test.com",
                full_name="Operator Test",
                hashed_password=get_password_hash("operator123"),
                role=UserRole.OPERATOR,
                is_active=True
            )
            db.add(operator_user)
            db.commit()
            db.refresh(operator_user)
        
        return admin_user, operator_user
    finally:
        db.close()

def test_user_model():
    """Test del modelo de usuario"""
    print("🧪 Probando modelo de usuario...")
    
    db = TestingSessionLocal()
    try:
        # Crear usuario de prueba
        user = User(
            username="test_user",
            email="test@example.com",
            full_name="Test User",
            hashed_password=get_password_hash("password123"),
            role=UserRole.OPERATOR,
            is_active=True,
            phone="1234567890",
            profile_photo="https://example.com/photo.jpg"
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Verificar propiedades
        assert user.first_name == "Test"
        assert user.last_name == "User"
        assert user.is_operator == True
        assert user.is_admin == False
        assert user.can_manage_users() == False
        
        print("✅ Modelo de usuario funcionando correctamente")
        return user
    finally:
        db.close()

def test_activity_log_model():
    """Test del modelo de logs de actividad"""
    print("🧪 Probando modelo de logs de actividad...")
    
    db = TestingSessionLocal()
    try:
        # Crear usuario de prueba
        user = User(
            username="log_test_user",
            email="log@example.com",
            full_name="Log Test User",
            hashed_password=get_password_hash("password123"),
            role=UserRole.OPERATOR,
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Crear log de actividad
        activity_log = UserActivityLog(
            user_id=user.id,
            activity_type=ActivityType.PROFILE_UPDATE,
            description="Perfil actualizado",
            ip_address="127.0.0.1",
            user_agent="Test Browser",
            activity_metadata={"field": "email", "old_value": "old@example.com", "new_value": "new@example.com"}
        )
        
        db.add(activity_log)
        db.commit()
        db.refresh(activity_log)
        
        # Verificar propiedades
        assert activity_log.user_id == user.id
        assert activity_log.activity_type == ActivityType.PROFILE_UPDATE
        assert activity_log.description == "Perfil actualizado"
        assert activity_log.ip_address == "127.0.0.1"
        assert activity_log.activity_metadata["field"] == "email"
        
        print("✅ Modelo de logs de actividad funcionando correctamente")
        return activity_log
    finally:
        db.close()

def test_user_service():
    """Test del servicio de usuarios"""
    print("🧪 Probando servicio de usuarios...")
    
    db = TestingSessionLocal()
    try:
        user_service = UserService(db)
        
        # Crear usuario de prueba
        from src.schemas.user import UserCreate
        user_data = UserCreate(
            username="service_test",
            email="service@test.com",
            full_name="Service Test User",
            password="password123",
            role=UserRole.OPERATOR
        )
        
        user = user_service.create_user(user_data)
        assert user.username == "service_test"
        assert user.email == "service@test.com"
        assert user.first_name == "Service"
        assert user.last_name == "Test User"
        
        # Test de actualización de perfil
        from src.schemas.user import UserUpdate
        update_data = UserUpdate(
            first_name="Updated",
            last_name="Name",
            phone="9876543210"
        )
        
        updated_user = user_service.update_user_profile(
            user_id=user.id,
            user_data=update_data,
            ip_address="127.0.0.1",
            user_agent="Test Browser"
        )
        
        assert updated_user.first_name == "Updated"
        assert updated_user.last_name == "Name"
        assert updated_user.phone == "9876543210"
        
        # Verificar que se creó el log de actividad
        logs = user_service.get_user_activity_logs(user.id, limit=10)
        assert len(logs) > 0
        assert logs[0].activity_type == ActivityType.PROFILE_UPDATE
        
        print("✅ Servicio de usuarios funcionando correctamente")
        return user
    finally:
        db.close()

def test_activity_log_service():
    """Test del servicio de logs de actividad"""
    print("🧪 Probando servicio de logs de actividad...")
    
    db = TestingSessionLocal()
    try:
        activity_service = ActivityLogService(db)
        
        # Crear usuario de prueba
        user = User(
            username="activity_test",
            email="activity@test.com",
            full_name="Activity Test User",
            hashed_password=get_password_hash("password123"),
            role=UserRole.OPERATOR,
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Crear varios logs de actividad
        activities = [
            (ActivityType.LOGIN, "Inicio de sesión"),
            (ActivityType.PROFILE_UPDATE, "Actualización de perfil"),
            (ActivityType.PASSWORD_CHANGE, "Cambio de contraseña"),
            (ActivityType.LOGOUT, "Cierre de sesión")
        ]
        
        for activity_type, description in activities:
            activity_service.log_activity(
                user_id=user.id,
                activity_type=activity_type,
                description=description,
                ip_address="127.0.0.1",
                user_agent="Test Browser"
            )
        
        # Obtener logs del usuario
        logs = activity_service.get_user_activity_logs(user.id, limit=10)
        assert len(logs) == 4
        
        # Obtener estadísticas
        stats = activity_service.get_activity_stats(user.id, days=30)
        assert stats["total_activities"] == 4
        assert "login" in stats["activities_by_type"]
        assert "profile_update" in stats["activities_by_type"]
        assert "password_change" in stats["activities_by_type"]
        assert "logout" in stats["activities_by_type"]
        
        print("✅ Servicio de logs de actividad funcionando correctamente")
        return user
    finally:
        db.close()

def test_api_endpoints():
    """Test de los endpoints de la API"""
    print("🧪 Probando endpoints de la API...")
    
    client = TestClient(app)
    
    # Configurar base de datos de prueba
    setup_test_database()
    
    # Test de login
    login_response = client.post("/auth/login", data={
        "username": "admin_test",
        "password": "admin123"
    })
    
    assert login_response.status_code == 200
    token_data = login_response.json()
    assert "access_token" in token_data
    
    # Headers con token
    headers = {"Authorization": f"Bearer {token_data['access_token']}"}
    
    # Test de obtener perfil
    profile_response = client.get("/profile/api/profile", headers=headers)
    assert profile_response.status_code == 200
    profile_data = profile_response.json()
    assert profile_data["username"] == "admin_test"
    assert profile_data["role"] == "admin"
    
    # Test de actualizar perfil
    update_data = {
        "first_name": "Updated",
        "last_name": "Admin",
        "phone": "1234567890"
    }
    
    update_response = client.put("/profile/api/profile", 
                               json=update_data, 
                               headers=headers)
    assert update_response.status_code == 200
    update_result = update_response.json()
    assert update_result["message"] == "Perfil actualizado exitosamente"
    
    # Test de obtener logs de actividad
    logs_response = client.get("/profile/api/profile/activity-logs", headers=headers)
    assert logs_response.status_code == 200
    logs_data = logs_response.json()
    assert isinstance(logs_data, list)
    
    # Test de obtener estadísticas de actividad
    stats_response = client.get("/profile/api/profile/activity-stats", headers=headers)
    assert stats_response.status_code == 200
    stats_data = stats_response.json()
    assert "total_activities" in stats_data
    assert "activities_by_type" in stats_data
    
    print("✅ Endpoints de la API funcionando correctamente")

def test_admin_functionality():
    """Test de funcionalidades de administrador"""
    print("🧪 Probando funcionalidades de administrador...")
    
    client = TestClient(app)
    
    # Login como admin
    login_response = client.post("/auth/login", data={
        "username": "admin_test",
        "password": "admin123"
    })
    
    assert login_response.status_code == 200
    token_data = login_response.json()
    headers = {"Authorization": f"Bearer {token_data['access_token']}"}
    
    # Test de obtener lista de usuarios
    users_response = client.get("/api/admin/users", headers=headers)
    assert users_response.status_code == 200
    users_data = users_response.json()
    assert isinstance(users_data, list)
    assert len(users_data) > 0
    
    # Buscar usuario operador para las pruebas
    operator_user = None
    for user in users_data:
        if user["username"] == "operator_test":
            operator_user = user
            break
    
    if operator_user:
        user_id = operator_user["id"]
        
        # Test de cambiar rol de usuario
        role_data = {"role": "user"}
        role_response = client.put(f"/api/admin/users/{user_id}/role", 
                                 json=role_data, 
                                 headers=headers)
        assert role_response.status_code == 200
        role_result = role_response.json()
        assert "Rol actualizado exitosamente" in role_result["message"]
        
        # Test de cambiar estado de usuario
        status_data = {"is_active": False}
        status_response = client.put(f"/api/admin/users/{user_id}/status", 
                                   json=status_data, 
                                   headers=headers)
        assert status_response.status_code == 200
        status_result = status_response.json()
        assert "Estado actualizado exitosamente" in status_result["message"]
        
        # Test de obtener logs de actividad de usuario
        logs_response = client.get(f"/api/admin/users/{user_id}/activity-logs", headers=headers)
        assert logs_response.status_code == 200
        logs_data = logs_response.json()
        assert isinstance(logs_data, list)
    
    print("✅ Funcionalidades de administrador funcionando correctamente")

def main():
    """Función principal para ejecutar todos los tests"""
    print("🚀 PAQUETES EL CLUB v3.1 - Test de Funcionalidades de Perfil")
    print("=" * 60)
    
    try:
        # Configurar base de datos de prueba
        setup_test_database()
        
        # Ejecutar tests
        test_user_model()
        test_activity_log_model()
        test_user_service()
        test_activity_log_service()
        test_api_endpoints()
        test_admin_functionality()
        
        print("\n" + "=" * 60)
        print("🎉 ¡Todos los tests pasaron exitosamente!")
        print("✅ Funcionalidades del perfil de usuario implementadas correctamente")
        
    except Exception as e:
        print(f"\n❌ Error en los tests: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
