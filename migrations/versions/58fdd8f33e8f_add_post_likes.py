"""add post likes

Revision ID: 58fdd8f33e8f
Revises: 14fa1bce64b4
Create Date: 2022-03-29 11:53:18.748967

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '58fdd8f33e8f'
down_revision = '14fa1bce64b4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post_likes',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.Column('post_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post_like')
    # ### end Alembic commands ###
