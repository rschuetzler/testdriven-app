"""empty message

Revision ID: f06a8effdcf6
Revises: 7cd16dff4316
Create Date: 2018-06-13 20:10:09.019341

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f06a8effdcf6'
down_revision = '7cd16dff4316'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password', sa.String(length=255), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'password')
    # ### end Alembic commands ###