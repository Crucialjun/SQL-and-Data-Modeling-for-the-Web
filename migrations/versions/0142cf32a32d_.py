"""empty message

Revision ID: 0142cf32a32d
Revises: 0f6ea6db6f72
Create Date: 2022-09-01 12:43:49.313415

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0142cf32a32d'
down_revision = '0f6ea6db6f72'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Show', sa.Column('start_time', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Show', 'start_time')
    # ### end Alembic commands ###
