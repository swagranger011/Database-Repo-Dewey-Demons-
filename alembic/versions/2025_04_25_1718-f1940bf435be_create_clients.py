"""Creates clients table (and membership_types since we have membership_type FK)

Revision ID: f1940bf435be
Revises: 
Create Date: 2025-04-25 17:18:20.169011

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa # type: ignore # noqa: F401


# revision identifiers, used by Alembic.
revision: str = 'f1940bf435be'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
        CREATE TYPE membership_types_enum AS ENUM ('Regular', 'Student', 'Senior Citizen');
        CREATE TYPE account_status_enum AS ENUM ('Active', 'Suspended');

        CREATE TABLE membership_types (
            membership_type membership_types_enum PRIMARY KEY,
            borrowing_limit INT,
            reserving_limit INT,
            late_fee_rate DECIMAL
        );

        CREATE TABLE clients (
            client_id SERIAL PRIMARY KEY, -- Use SERIAL for auto-increment
            name VARCHAR NOT NULL,
            contact_info VARCHAR NOT NULL,
            membership_type membership_types_enum NOT NULL,
            account_status account_status_enum NOT NULL,
            FOREIGN KEY (membership_type) REFERENCES membership_types (membership_type)
        );
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
        DROP TABLE IF EXISTS clients;
        DROP TABLE IF EXISTS membership_types;
        DROP TYPE IF EXISTS membership_types_enum;
        DROP TYPE IF EXISTS account_status_enum;
    """)
