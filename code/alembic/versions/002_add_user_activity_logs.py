"""Add user activity logs table

Revision ID: 002
Revises: 001
Create Date: 2025-01-27 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Crear tipo ENUM para ActivityType
    op.execute("CREATE TYPE activitytype AS ENUM ('login', 'logout', 'profile_update', 'password_change', 'package_create', 'package_update', 'package_delete', 'file_upload', 'file_delete', 'user_create', 'user_update', 'user_delete', 'role_change', 'status_change')")
    
    # Crear tabla user_activity_logs
    op.create_table('user_activity_logs',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('activity_type', sa.Enum('login', 'logout', 'profile_update', 'password_change', 'package_create', 'package_update', 'package_delete', 'file_upload', 'file_delete', 'user_create', 'user_update', 'user_delete', 'role_change', 'status_change', name='activitytype'), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('ip_address', sa.String(length=45), nullable=True),
        sa.Column('user_agent', sa.String(length=500), nullable=True),
        sa.Column('activity_metadata', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Crear índices
    op.create_index('idx_user_activity_logs_user_id', 'user_activity_logs', ['user_id'])
    op.create_index('idx_user_activity_logs_activity_type', 'user_activity_logs', ['activity_type'])
    op.create_index('idx_user_activity_logs_created_at', 'user_activity_logs', ['created_at'])
    
    # Crear foreign key
    op.create_foreign_key(None, 'user_activity_logs', 'users', ['user_id'], ['id'])

def downgrade() -> None:
    # Eliminar foreign key
    op.drop_constraint(None, 'user_activity_logs', type_='foreignkey')
    
    # Eliminar índices
    op.drop_index('idx_user_activity_logs_created_at', table_name='user_activity_logs')
    op.drop_index('idx_user_activity_logs_activity_type', table_name='user_activity_logs')
    op.drop_index('idx_user_activity_logs_user_id', table_name='user_activity_logs')
    
    # Eliminar tabla
    op.drop_table('user_activity_logs')
    
    # Eliminar tipo ENUM
    op.execute("DROP TYPE activitytype")
