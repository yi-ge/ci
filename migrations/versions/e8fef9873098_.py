"""empty message

Revision ID: e8fef9873098
Revises: 5ee0af64d5f1
Create Date: 2017-09-16 15:45:45.106105

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e8fef9873098'
down_revision = '5ee0af64d5f1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('phone', sa.String(length=15), nullable=False))
    op.create_unique_constraint(None, 'users', ['phone'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'phone')
    # ### end Alembic commands ###
