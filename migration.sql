BEGIN;

CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> f1940bf435be

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
        );;

INSERT INTO alembic_version (version_num) VALUES ('f1940bf435be') RETURNING alembic_version.version_num;

-- Running upgrade f1940bf435be -> f2b5a2fa71a3

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
);;

UPDATE alembic_version SET version_num='f2b5a2fa71a3' WHERE alembic_version.version_num = 'f1940bf435be';

-- Running upgrade f2b5a2fa71a3 -> 861a1b2fb610

ALTER TABLE books ADD COLUMN isbn_temp VARCHAR(17);
UPDATE books SET isbn_temp = CAST(isbn AS VARCHAR);
ALTER TABLE books DROP COLUMN isbn;
ALTER TABLE books RENAME COLUMN isbn_temp TO isbn;;

UPDATE alembic_version SET version_num='861a1b2fb610' WHERE alembic_version.version_num = 'f2b5a2fa71a3';

COMMIT;

