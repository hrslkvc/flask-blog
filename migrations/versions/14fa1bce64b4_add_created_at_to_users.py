"""add created at to users

Revision ID: 14fa1bce64b4
Revises: bfdb502df5d4
Create Date: 2022-03-29 10:58:11.980702

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '14fa1bce64b4'
down_revision = 'bfdb502df5d4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('created_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'created_at')
    # ### end Alembic commands ###
