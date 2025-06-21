"""add unit_name and building_name to properties table

Revision ID: f038fad8e588
Revises: e88432ca6579
Create Date: 2025-06-21 01:33:48.278828

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f038fad8e588'
down_revision = 'e88432ca6579'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('properties', sa.Column('unit_name', sa.String(length=100), nullable=True))
    op.create_index(op.f('ix_properties_unit_name'), 'properties', ['unit_name'], unique=False)
    op.add_column('properties', sa.Column('building_name', sa.String(length=100), nullable=True))
    op.create_index(op.f('ix_properties_building_name'), 'properties', ['building_name'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_properties_building_name'), table_name='properties')
    op.drop_column('properties', 'building_name')
    op.drop_index(op.f('ix_properties_unit_name'), table_name='properties')
    op.drop_column('properties', 'unit_name')
