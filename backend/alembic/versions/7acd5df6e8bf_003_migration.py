"""003_migration

Revision ID: 7acd5df6e8bf
Revises: f44be09146ae
Create Date: 2024-10-11 05:23:13.869308

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '7acd5df6e8bf'
down_revision: Union[str, None] = 'f44be09146ae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
