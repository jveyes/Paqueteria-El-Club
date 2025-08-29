"""add user relations to models

Revision ID: 005
Revises: 004_add_tracking_code_to_announcements
Create Date: 2025-08-29 05:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '005'
down_revision = '004_add_tracking_code'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Agregar columna created_by_id a package_announcements
    op.add_column('package_announcements', sa.Column('created_by_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.create_foreign_key(None, 'package_announcements', 'users', ['created_by_id'], ['id'])
    
    # Agregar columna created_by_id a packages
    op.add_column('packages', sa.Column('created_by_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.create_foreign_key(None, 'packages', 'users', ['created_by_id'], ['id'])


def downgrade() -> None:
    # Eliminar foreign keys
    op.drop_constraint(None, 'packages', type_='foreignkey')
    op.drop_constraint(None, 'package_announcements', type_='foreignkey')
    
    # Eliminar columnas
    op.drop_column('packages', 'created_by_id')
    op.drop_column('package_announcements', 'created_by_id')
