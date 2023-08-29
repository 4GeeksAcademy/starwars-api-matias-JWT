"""empty message

Revision ID: d2afbe942246
Revises: eee6dd1f48a7
Create Date: 2023-08-29 18:58:05.946193

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd2afbe942246'
down_revision = 'eee6dd1f48a7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('vehicle',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('model', sa.String(length=250), nullable=False),
    sa.Column('manufacturer', sa.String(length=250), nullable=False),
    sa.Column('cost_in_credits', sa.Integer(), nullable=False),
    sa.Column('length', sa.Float(precision=50), nullable=False),
    sa.Column('speed', sa.Integer(), nullable=False),
    sa.Column('crew', sa.Integer(), nullable=False),
    sa.Column('cargo_capacity', sa.Integer(), nullable=False),
    sa.Column('consumables', sa.String(length=250), nullable=False),
    sa.Column('vehicle_class', sa.String(length=250), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('vehicle')
    # ### end Alembic commands ###
