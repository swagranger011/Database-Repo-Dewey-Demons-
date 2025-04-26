"""fix isbn

Revision ID: 861a1b2fb610
Revises: f2b5a2fa71a3
Create Date: 2025-04-25 20:16:55.623507

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa  # type: ignore # noqa: F401


# revision identifiers, used by Alembic.
revision: str = "861a1b2fb610"
down_revision: Union[str, None] = "f2b5a2fa71a3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
ALTER TABLE books ADD COLUMN isbn_temp VARCHAR(17);
UPDATE books SET isbn_temp = CAST(isbn AS VARCHAR);
ALTER TABLE books DROP COLUMN isbn;
ALTER TABLE books RENAME COLUMN isbn_temp TO isbn;  
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
DO $$
BEGIN
    -- Check for non-numeric ISBNs
    IF EXISTS (SELECT 1 FROM books WHERE isbn ~ '[^0-9]') THEN
    RAISE EXCEPTION 'Cannot downgrade - non-numeric ISBN values exist';
    END IF;
END $$;

ALTER TABLE books ALTER COLUMN isbn TYPE INTEGER USING (isbn::INTEGER);  
    """)
