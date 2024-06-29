"""create users table

Revision ID: f83352319389
Revises: 
Create Date: 2024-06-29 04:26:51.488873

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f83352319389'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('user_id', sa.UUID, primary_key=True),
        sa.Column('username', sa.String(50), nullable=True),
        sa.Column('email', sa.String(250), nullable=True),
        sa.Column('phone', sa.String(20), nullable=True),
        sa.Column('password', sa.TEXT, nullable=True),
        sa.Column('created_at', sa.TIMESTAMP, nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP, nullable=True),
        sa.Column('deleted_at', sa.TIMESTAMP, nullable=True)
    )


def downgrade() -> None:
    op.drop_table('users')
