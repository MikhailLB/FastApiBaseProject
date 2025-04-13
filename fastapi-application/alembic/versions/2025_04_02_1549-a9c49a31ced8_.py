"""empty message

Revision ID: a9c49a31ced8
Revises: d9a7358dd70e
Create Date: 2025-04-02 15:49:51.549082

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a9c49a31ced8"
down_revision: Union[str, None] = "d9a7358dd70e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "notes",
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.add_column(
        "notes",
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )



def downgrade() -> None:

    op.drop_column("notes", "updated_at")
    op.drop_column("notes", "created_at")

