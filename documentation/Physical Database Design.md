**Introduction**:

- Project Overview:
  - This database's purpose is to simplify the management of a modern library system's core operations. Core operations include resource cataloging, client interactions, and transaction workflows. The entities integrated into the database are books, digital media, clients, staff, and membership types to allow for actions such as borrowing, reservations, and notifications. This system will track these actions, calculate fines, and monitor the availability of physical and digital resources. Relationships between entities ensure seamless coordination, like linking clients to their transactions or reservations, staff to system management, and membership types to borrowing privileges. The database supports real- time updates for availability, automated overdue notifications, and dynamic fine calculations, which align with the library’s goals of accessibility, accuracy, and user satisfaction.
- Scope:
  - The scope of this database will cover resource management, client management, transaction workflows, notifications, and staff operations. Resource management will involve cataloging books and digital media with metadata and tracking availability. Client management will involve storing client details, membership types, and account statuses, with borrowing limits tied to membership tiers. Transactional workflows will involve managing checkouts, returns, reservations, and fines, with automated status updates. Notifications will be sent out for due dates, overdue items, and reservation availability. And lastly, staff operations will involve recording staff contact details for internal management. The information that is out of scope is integration with external e-book platforms, mobile app interfaces, payment processing for fine, advanced analytics or predictive modeling for inventory, and inter-library loan systems beyond the local branch network. The system serves as a foundational tool for daily operations, with scalability for future enhancements like API expansions.
- Glossary:
  - Book_ID/Media_ID/Magazine_ID: Unique numeric identifier for physical/digital resources.
  - Title: Title of a book/digital media.
  - Author/Creator: The person who made the book/digital media.
  - Issue_Number: Specific number assigned to a magazine issue.
  - Publish_Date: The publication date of a magazine issue.
  - Genre: Genre of a book/digital media.
  - Publication_Year: Year that a book/digital media waspublished.
  - Format: Type of digital media.
  - ISBN: Unique identifier used to identify a book or other publication.
  - ENUM: Enumerated data type.
  - VARCHAR: Variable-length character string.
  - Material_ID: Foreign key identifier used for identifying a book or digital media.
  - Client_ID: Unique identifier for library clients, linked to transactions and reservations.
  - Name: Name of each client.
  - DOB: Date of birth.
  - Contact_Info: Contact information of the clients.
  - Work_Phone_Number: Phone number of those on staff.
  - Work_Email: Email address of those on staff.
  - Membership_Type: Tier (Regular, Student, Senior) determining borrowing limits and fees.
  - Transaction_ID: Unique identifier for a checkout-return event/tied to fines.
  - Reservation_ID: Identifier for holds placed on unavailable
    items.
  - Reservation_Date: The date of the reservation.
  - Reserving_Limit: Maximum reservations that a client can
    book.
  - Availability_Status: Current state of a resource (Available/Checked Out/ Reserved).
  - Return_Date: The date that the book/digital media was their membership
  - Borrow_Date: The
    borrowed.
  - Fine_Amount: The either returning the book/digital media late or losing/destroying the book/digital media.
  - Due_Date: The date that the book/digital media HAS to be returned.
  - Borrowing_Limit: Maximum items a client can borrow based on date that the book/digital media is amount of any fine that is charged for
  - Late_Fee_Rate: The fee per day for overdue items is defined by membership type.
  - OPAC: Online catalog for clients to search resources (implied by
  - Title/Author attributes).
  - Hold: Synonym for reservations (active, fulfilled, or canceled).
  - Staff_ID: Unique identifier for library employees.
  - Notification_ID: A unique identifier is used to identify notifications.
  - Message: The message in the notification sent to the client.
  - Sent_Date: The date that the notification got sent on.
  - Account_Status: Shows whether a client’s account is active or not.
  - Status: Tracks the status of a reservation

**Platform**:

The database system will utilize PostgreSQL as the relational database management system, deployed within a Docker container.

This will allow platform agnostic and prevent affecting a local user's machines (ie. the database will be containerized).

It uses python and [`alembic`](https://github.com/sqlalchemy/alembic) as tooling for running migrations.

The reasons are as follows:

- Postgressql was used due to it's increasingly popularity among developers (ranked #1 in 2024 stackoverflow survey as a RDMS),
  so it seemed a smart choice to learn
- Dockerized Containers were used to allow developers to be able to run code platform agnostic and ensure running
  code does not affect user's local development environment (ie. all artifacts are within containers/volumes)
- Migrations (ie. sql scripts) written in multiple parts is common-place in industry. It is also common
  due to limited database access, where DDL scripts have to be passed to database admins.
  - Using a tool to handle migrations likewise is easier than handling DDLs ourselves. Ensures
    consistency within the evolving database.
-

**Physical Schema**:

```sql
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

-- Running upgrade 861a1b2fb610 -> 5c55b5b031ff

ALTER TABLE books
ADD CONSTRAINT books_isbn_numeric_check
CHECK (isbn ~ '^[0-9]+$');;

UPDATE alembic_version SET version_num='5c55b5b031ff' WHERE alembic_version.version_num = '861a1b2fb610';

COMMIT;
```

**Table Contents**:

```sql
eecs447=# SELECT * from books;
 book_id | material_id |      author       |     isbn
---------+-------------+-------------------+---------------
       1 |           1 | John Doe          | 9780123456789
       2 |           2 | Jane Smith        | 9789876543210
       3 |           6 | Agatha Christie   | 9780307588371
       4 |           8 | Daniele Moschella | 9781492097611
       5 |          13 | Jane Smith        | 9781234567890
       6 |          14 | Test Author       | 9781111111111
(6 rows)


eecs447=# SELECT * from borrowing_transactions;
 transaction_id | client_id | material_id | borrow_date |  due_date  | return_date | fine_amount
----------------+-----------+-------------+-------------+------------+-------------+-------------
              1 |         1 |           1 | 2024-01-01  | 2024-01-15 | 2024-01-10  |         0.0
              2 |         2 |           2 | 2024-01-05  | 2024-01-20 |             |         0.0
              3 |         4 |           6 | 2025-03-15  | 2025-03-29 | 2025-03-28  |         0.0
              4 |         5 |           8 | 2025-04-01  | 2025-04-15 |             |         0.0
              5 |         2 |           9 | 2025-02-10  | 2025-02-24 | 2025-02-25  |         0.0
              6 |         3 |           6 | 2025-04-01  | 2025-04-15 | 2025-04-20  |         0.0
              7 |         1 |           2 | 2025-03-01  | 2025-03-15 | 2025-03-20  |         0.0
              8 |         2 |           2 | 2025-04-05  | 2025-04-19 | 2025-04-10  |         0.0
              9 |         3 |           1 | 2025-05-01  | 2025-05-08 |             |         0.0
             10 |         2 |           2 | 2025-04-01  | 2025-04-15 |             |         0.0
             11 |         2 |           1 | 2025-03-10  | 2025-03-20 | 2025-03-25  |         0.0
             12 |         1 |           1 | 2025-04-10  | 2025-04-24 |             |         0.0
             13 |         2 |           1 | 2025-04-15  | 2025-04-29 |             |         0.0
             14 |         3 |           1 | 2025-04-20  | 2025-05-04 |             |         0.0
(14 rows)


eecs447=# SELECT * from clients;
 client_id |      name      |        contact_info        | membership_type | account_status
-----------+----------------+----------------------------+-----------------+----------------
         1 | Alice Smith    | alice.smith@example.com    | Regular         | Active
         2 | Bob Johnson    | bob.johnson@example.com    | Student         | Active
         3 | Carol Williams | carol.williams@example.com | Senior Citizen  | Suspended
         4 | David Brown    | david.brown@example.com    | Regular         | Active
         5 | Eve Green      | eve.green@example.com      | Student         | Active
(5 rows)


eecs447=# SELECT * from digital_media;
 media_id | material_id |  creator   | format
----------+-------------+------------+--------
        1 |           3 | Mark Lee   | eBook
        2 |           4 | Director X | DVD
        3 |           9 | NAT Geo    | DVD
(3 rows)


eecs447=# SELECT * from library_material;
 material_id |       title        | publication_year |    genre    | availability_status |     type
-------------+--------------------+------------------+-------------+---------------------+---------------
           1 | The Great Novel    |             2020 | Fiction     | Available           | Book
           2 | History of Rome    |             2015 | History     | Checked Out         | Book
           3 | Digital Marketing  |             2022 | Business    | Available           | Digital Media
           4 | Sci-Fi Movie       |             2023 | Sci-Fi      | Available           | Digital Media
           5 | Tech Today         |             2024 | Technology  | Avai