"""create rest

Revision ID: f2b5a2fa71a3
Revises: f1940bf435be
Create Date: 2025-04-25 18:32:43.829035

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa  # type: ignore # noqa: F401


# revision identifiers, used by Alembic.
revision: str = "f2b5a2fa71a3"
down_revision: Union[str, None] = "f1940bf435be"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
CREATE TABLE library_material (
    material_id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    publication_year INT NOT NULL,
    genre VARCHAR NOT NULL,
    availability_status VARCHAR NOT NULL,
    type VARCHAR NOT NULL
);

CREATE TABLE books (
    book_id SERIAL PRIMARY KEY,
    material_id INT REFERENCES library_material (material_id),
    author VARCHAR NOT NULL,
    isbn INT UNIQUE NOT NULL
);

CREATE TABLE digital_media (
    media_id SERIAL PRIMARY KEY,
    material_id INT REFERENCES library_material (material_id),
    creator VARCHAR NOT NULL,
    format VARCHAR NOT NULL
);

CREATE TABLE magazines (
    magazine_id SERIAL PRIMARY KEY,
    material_id INT REFERENCES library_material (material_id),
    issue_number VARCHAR NOT NULL,
    publish_date DATE NOT NULL
);

CREATE TABLE staff (
    staff_id INT PRIMARY KEY REFERENCES clients (client_id),
    dob DATE NOT NULL,
    work_phone_number VARCHAR NOT NULL,
    work_email VARCHAR NOT NULL
);

CREATE TABLE borrowing_transactions (
    transaction_id SERIAL PRIMARY KEY,
    client_id INT REFERENCES clients (client_id),
    material_id INT REFERENCES library_material (material_id),
    borrow_date DATE NOT NULL,
    due_date DATE NOT NULL,
    return_date DATE,
    fine_amount DECIMAL NOT NULL
);

CREATE TABLE reservations (
    reservation_id SERIAL PRIMARY KEY,
    client_id INT REFERENCES clients (client_id),
    material_id INT REFERENCES library_material (material_id),
    reservation_date DATE NOT NULL,
    status VARCHAR NOT NULL
);

CREATE TABLE notifications (
    notification_id SERIAL PRIMARY KEY,
    client_id INT REFERENCES clients (client_id),
    message TEXT NOT NULL,
    sent_date DATE NOT NULL
);
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
DROP TABLE IF EXISTS notifications;
DROP TABLE IF EXISTS reservations;
DROP TABLE IF EXISTS borrowing_transactions;
DROP TABLE IF EXISTS staff;
DROP TABLE IF EXISTS magazines;
DROP TABLE IF EXISTS digital_media;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS library_material;    
    """)
