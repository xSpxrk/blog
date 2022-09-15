"""Added table user

Revision ID: 041de896a4aa
Revises: 
Create Date: 2022-09-14 15:54:00.808665

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '041de896a4aa'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('hashed_password', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('user')
