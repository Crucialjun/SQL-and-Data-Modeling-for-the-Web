"""empty message

Revision ID: 7b310081266e
Revises: c29ca85a1e66
Create Date: 2022-08-31 15:00:54.414627

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7b310081266e'
down_revision = 'c29ca85a1e66'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Show', sa.Column('venue_name', sa.String(length=120), nullable=True))
    op.add_column('Show', sa.Column('artist_name', sa.String(length=120), nullable=True))
    op.add_column('Show', sa.Column('artist_image_link', sa.String(length=500), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Show', 'artist_image_link')
    op.drop_column('Show', 'artist_name')
    op.drop_column('Show', 'venue_name')
    # ### end Alembic commands ###
