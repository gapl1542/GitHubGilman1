"""padrehijo

Revision ID: 6a4eab0617ab
Revises: 3934a1f03422
Create Date: 2020-10-15 01:58:50.790932

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6a4eab0617ab'
down_revision = '3934a1f03422'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('account', sa.Column('is_teacher', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('account', 'is_teacher')
    # ### end Alembic commands ###
