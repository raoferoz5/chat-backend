"""create_initial_tables

Revision ID: f82c925dc213
Revises: 
Create Date: 2026-06-02 18:42:14.639681

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f82c925dc213'
down_revision: Union[str, Sequence[str], None] = '223f7594497f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
