"""Add profile_photo column to users table

Revision ID: 003
Revises: 002
Create Date: 2025-01-27 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Agregar columna profile_photo a la tabla users
    op.add_column('users', sa.Column('profile_photo', sa.String(length=500), nullable=True))

def downgrade() -> None:
    # Eliminar columna profile_photo de la tabla users
    op.drop_column('users', 'profile_photo')
