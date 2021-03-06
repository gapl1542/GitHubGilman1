"""cambio nombre coments2

Revision ID: 40de0defc0d6
Revises: d1eb2c836163
Create Date: 2020-10-15 20:59:37.171039

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '40de0defc0d6'
down_revision = 'd1eb2c836163'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('coments', sa.Column('title_pdf', sa.String(length=256), nullable=False))
    op.create_unique_constraint(None, 'coments', ['title_pdf'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'coments', type_='unique')
    op.drop_column('coments', 'title_pdf')
    # ### end Alembic commands ###
