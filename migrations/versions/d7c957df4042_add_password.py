"""add password

Revision ID: d7c957df4042
Revises: 0a4da45a92eb
Create Date: 2020-07-16 09:56:18.173089

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd7c957df4042'
down_revision = '0a4da45a92eb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('mahasiswa', sa.Column('password', sa.String(length=10), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('mahasiswa', 'password')
    # ### end Alembic commands ###