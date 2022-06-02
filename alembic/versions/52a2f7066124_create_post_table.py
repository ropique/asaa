"""create post table

Revision ID: 52a2f7066124
Revises: 
Create Date: 2022-06-01 17:49:26.796958

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '52a2f7066124'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False,
    primary_key=True), sa.Column('title', sa.String(), nullable=False), sa.Column('category', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
