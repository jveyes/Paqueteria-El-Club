"""add password reset tokens

Revision ID: 002
Revises: 001
Create Date: 2025-01-25 06:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '002_add_password_reset_tokens'
down_revision = '001_initial_migration'
branch_labels = None
depends_on = None

def upgrade():
    """Crear tabla de tokens de restablecimiento de contraseña"""
    op.create_table('password_reset_tokens',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('token', sa.String(length=255), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('used', sa.Boolean(), nullable=False, default=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, default=sa.func.now()),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Crear índices
    op.create_index(op.f('ix_password_reset_tokens_token'), 'password_reset_tokens', ['token'], unique=True)
    op.create_index(op.f('ix_password_reset_tokens_user_id'), 'password_reset_tokens', ['user_id'], unique=False)
    op.create_index(op.f('ix_password_reset_tokens_expires_at'), 'password_reset_tokens', ['expires_at'], unique=False)

def downgrade():
    """Eliminar tabla de tokens de restablecimiento de contraseña"""
    op.drop_index(op.f('ix_password_reset_tokens_expires_at'), table_name='password_reset_tokens')
    op.drop_index(op.f('ix_password_reset_tokens_user_id'), table_name='password_reset_tokens')
    op.drop_index(op.f('ix_password_reset_tokens_token'), table_name='password_reset_tokens')
    op.drop_table('password_reset_tokens')
