"""empty message

Revision ID: 23aa591d3215
Revises: 79c2a4857bad
Create Date: 2024-06-04 13:48:35.079873

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "23aa591d3215"
down_revision: Union[str, None] = "79c2a4857bad"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
