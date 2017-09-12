"""empty message

Revision ID: 2a5a6640f7e2
Revises: 5c93568326e8
Create Date: 2017-08-25 07:31:35.127446

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a5a6640f7e2'
down_revision = '5c93568326e8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bucketlist', sa.Column('updated_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('bucketlist', 'updated_at')
    # ### end Alembic commands ###
