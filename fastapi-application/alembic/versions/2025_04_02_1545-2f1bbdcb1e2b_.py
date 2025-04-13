"""empty message

Revision ID: 2f1bbdcb1e2b
Revises: 4037583d157d
Create Date: 2025-04-02 15:45:51.656830

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2f1bbdcb1e2b"
down_revision: Union[str, None] = "4037583d157d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("password", sa.String(), nullable=False))



def downgrade() -> None:
    op.drop_column("users", "password")

