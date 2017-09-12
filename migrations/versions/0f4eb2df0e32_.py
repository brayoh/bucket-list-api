"""empty message

Revision ID: 0f4eb2df0e32
Revises: 2a5a6640f7e2
Create Date: 2017-08-25 07:40:20.626848

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0f4eb2df0e32'
down_revision = '2a5a6640f7e2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bucketlist_items', sa.Column('updated_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('bucketlist_items', 'updated_at')
    # ### end Alembic commands ###
