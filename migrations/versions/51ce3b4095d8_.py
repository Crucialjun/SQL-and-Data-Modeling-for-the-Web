"""empty message

Revision ID: 51ce3b4095d8
Revises: 
Create Date: 2022-09-01 12:42:03.803687

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '51ce3b4095d8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('upcoming_shows_count', sa.Integer(), nullable=True))
    op.add_column('Artist', sa.Column('upcoming_shows', sa.String(length=500), nullable=True))
    op.add_column('Artist', sa.Column('past_shows_count', sa.String(length=500), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Artist', 'past_shows_count')
    op.drop_column('Artist', 'upcoming_shows')
    op.drop_column('Artist', 'upcoming_shows_count')
    # ### end Alembic commands ###
