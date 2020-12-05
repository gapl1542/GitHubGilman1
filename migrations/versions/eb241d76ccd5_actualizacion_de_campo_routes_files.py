"""Actualizacion de campo routes_files

Revision ID: eb241d76ccd5
Revises: 569bcfbd0971
Create Date: 2020-09-21 21:42:31.404015

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb241d76ccd5'
down_revision = '569bcfbd0971'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('files', sa.Column('routes_files', sa.String(length=256), nullable=False))
    op.drop_column('files', 'routes_file')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('files', sa.Column('routes_file', sa.VARCHAR(length=80), autoincrement=False, nullable=False))
    op.drop_column('files', 'routes_files')
    # ### end Alembic commands ###
