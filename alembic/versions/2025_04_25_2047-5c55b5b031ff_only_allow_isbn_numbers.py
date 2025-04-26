"""only allow isbn numbers

Revision ID: 5c55b5b031ff
Revises: 861a1b2fb610
Create Date: 2025-04-25 20:47:49.896420

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa  # type: ignore # noqa: F401


# revision identifiers, used by Alembic.
revision: str = "5c55b5b031ff"
down_revision: Union[str, None] = "861a1b2fb610"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
ALTER TABLE books
ADD CONSTRAINT books_isbn_numeric_check 
CHECK (isbn ~ '^[0-9]+$');
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
ALTER TABLE books
DROP CONSTRAINT IF EXISTS books_isbn_numeric_check;
    """)
