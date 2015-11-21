"""empty message

Revision ID: 1ef87e10f6c0
Revises: 563acb57641f
Create Date: 2015-11-21 14:30:47.591401

"""

# revision identifiers, used by Alembic.
revision = '1ef87e10f6c0'
down_revision = '563acb57641f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('book_can', sa.Column('modify_permission', sa.Boolean(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('book_can', 'modify_permission')
    ### end Alembic commands ###
