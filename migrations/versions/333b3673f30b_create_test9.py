"""create test9

Revision ID: 333b3673f30b
Revises: 895eb61b2b62
Create Date: 2023-10-22 10:49:27.822000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '333b3673f30b'
down_revision: Union[str, None] = '895eb61b2b62'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('ProductUser', 'test')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ProductUser', sa.Column('test', sa.VARCHAR(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
