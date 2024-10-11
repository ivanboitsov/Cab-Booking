"""002_migration

Revision ID: f44be09146ae
Revises: c32aca645a16
Create Date: 2024-10-11 05:06:24.757621

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'f44be09146ae'
down_revision: Union[str, None] = 'c32aca645a16'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
