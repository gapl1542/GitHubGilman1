"""data1.6

Revision ID: 53e52dacfae6
Revises: 139ead4278c6
Create Date: 2020-10-15 04:06:02.666996

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '53e52dacfae6'
down_revision = '139ead4278c6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('files', sa.Column('username', sa.String(length=80), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('files', 'username')
    # ### end Alembic commands ###
