"""Added phone to user table

Revision ID: 17007c1f3587
Revises: d8f86f2ed853
Create Date: 2025-04-07 22:58:32.687699
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "17007c1f3587"
down_revision: Union[str, None] = "d8f86f2ed853"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("phone", sa.String(), nullable=False, server_default="")
        )
        batch_op.create_unique_constraint("uq_users_phone", ["phone"])


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_constraint("uq_users_phone", type_="unique")
        batch_op.drop_column("phone")
