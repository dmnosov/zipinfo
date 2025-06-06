"""nullable upload_id

Revision ID: 0398963c180e
Revises: 0704dc744990
Create Date: 2025-04-15 19:58:02.274324

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0398963c180e"
down_revision: Union[str, None] = "0704dc744990"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column("reports", "upload_id", existing_type=sa.UUID(), nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("reports", "upload_id", existing_type=sa.UUID(), nullable=False)
    # ### end Alembic commands ###
