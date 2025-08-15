"""initial tables

Revision ID: 0001
Revises: 
Create Date: 2024-05-27
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'roles',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.Enum('world_builder', 'dungeon_master', 'player', name='roleenum'), nullable=False, unique=True),
    )
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('username', sa.String(), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('role_id', sa.Integer(), sa.ForeignKey('roles.id')),
    )
    op.create_table(
        'sessions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('token', sa.String(), nullable=False, unique=True),
    )
    op.create_table(
        'world_items',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String()),
    )
    op.create_table(
        'player_profiles',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('bio', sa.String()),
    )


def downgrade() -> None:
    op.drop_table('player_profiles')
    op.drop_table('world_items')
    op.drop_table('sessions')
    op.drop_table('users')
    op.drop_table('roles')
    sa.Enum('world_builder', 'dungeon_master', 'player', name='roleenum').drop(op.get_bind(), checkfirst=False)
