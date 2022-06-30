"""Initial migration.

Revision ID: 566994cec6bf
Revises: 
Create Date: 2022-06-30 10:04:07.928987

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '566994cec6bf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('poll_question')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('poll_question',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('poll_id', sa.INTEGER(), nullable=False),
    sa.Column('text', sa.VARCHAR(length=64), nullable=False),
    sa.ForeignKeyConstraint(['poll_id'], ['poll.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
