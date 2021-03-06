"""creando files

Revision ID: 3934a1f03422
Revises: 405f3e5972ef
Create Date: 2020-10-09 07:41:13.325797

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3934a1f03422'
down_revision = '405f3e5972ef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('files',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('routes_files', sa.String(length=256), nullable=False),
    sa.Column('title', sa.String(length=256), nullable=False),
    sa.Column('uptime', sa.DateTime(), nullable=True),
    sa.Column('id_user', sa.Integer(), nullable=True),
    sa.Column('category', sa.String(length=256), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('files')
    # ### end Alembic commands ###
