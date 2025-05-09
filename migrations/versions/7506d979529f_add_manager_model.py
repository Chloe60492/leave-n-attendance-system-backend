"""add manager model

Revision ID: 7506d979529f
Revises: 9014b07421e1
Create Date: 2025-05-04 13:22:47.855703

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7506d979529f'
down_revision: Union[str, None] = '9014b07421e1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('users_manager_id_fkey', 'users', type_='foreignkey')
    op.drop_column('users', 'manager_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('manager_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('users_manager_id_fkey', 'users', 'users', ['manager_id'], ['id'])
    # ### end Alembic commands ###
