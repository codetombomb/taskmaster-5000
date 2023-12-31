"""create users and tasks

Revision ID: 4183c32e4588
Revises: 
Create Date: 2023-08-04 23:46:02.369287

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4183c32e4588'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('username', sa.String(length=30), nullable=True),
    sa.Column('birthday', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('task',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=150), nullable=False),
    sa.Column('complete', sa.Boolean(), nullable=True),
    sa.Column('due_date', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('task')
    op.drop_table('user')
    # ### end Alembic commands ###
