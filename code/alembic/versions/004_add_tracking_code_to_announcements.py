"""add tracking code to announcements

Revision ID: 004_add_tracking_code
Revises: 003_add_package_announcements
Create Date: 2024-01-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '004_add_tracking_code'
down_revision = '003'
branch_labels = None
depends_on = None


def upgrade():
    # Agregar columna tracking_code a package_announcements
    op.add_column('package_announcements', sa.Column('tracking_code', sa.String(length=4), nullable=True))
    
    # Crear índice único para tracking_code
    op.create_index(op.f('ix_package_announcements_tracking_code'), 'package_announcements', ['tracking_code'], unique=True)
    
    # Hacer la columna NOT NULL después de crear el índice
    op.alter_column('package_announcements', 'tracking_code', nullable=False)


def downgrade():
    # Eliminar índice
    op.drop_index(op.f('ix_package_announcements_tracking_code'), table_name='package_announcements')
    
    # Eliminar columna
    op.drop_column('package_announcements', 'tracking_code')
