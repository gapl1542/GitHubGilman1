"""data1.7

Revision ID: 8b1fc8e63da9
Revises: 53e52dacfae6
Create Date: 2020-10-15 05:13:57.567086

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b1fc8e63da9'
down_revision = '53e52dacfae6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Coments', sa.Column('username', sa.String(length=80), nullable=False))
    op.add_column('Coments', sa.Column('username_pdf', sa.String(length=80), nullable=False))
    op.drop_column('Coments', 'id_user_pdf')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Coments', sa.Column('id_user_pdf', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('Coments', 'username_pdf')
    op.drop_column('Coments', 'username')
    # ### end Alembic commands ###