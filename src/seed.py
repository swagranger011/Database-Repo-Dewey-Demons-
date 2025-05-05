from datetime import date
from sqlmodel import Session, create_engine, text
from src.models import (
    AccountStatusEnum,
    Books,
    BorrowingTransactions,
    Clients,
    DigitalMedia,
    DigitalMediaFormatEnum,
    LibraryMaterial,
    Magazines,
    MaterialTypeEnum,
    MembershipTypeEnum,
    MembershipTypes,
    Notifications,
    ReservationStatusEnum,
    Reservations,
    Staff,
)
from src.utils import get_url
from sqlalchemy.dialects.postgresql import insert as pg_insert


def seed_database(url: str = get_url()) -> None:
    engine = create_engine(url, echo=True)

    with Session(engine) as session:
        # Bulk insert MembershipTypes
        membership_types = [
            {
                "membership_type": MembershipTypeEnum.Regular.value,
                "borrowing_limit": 5,
                "reserving_limit": 3,
                "late_fee_rate": 0.25,
            },
            {
                "membership_type": MembershipTypeEnum.Student.value,
                "borrowing_limit": 3,
                "reserving_limit": 2,
                "late_fee_rate": 0.10,
            },
            {
                "membership_type": "Senior Citizen",
                "borrowing_limit": 7,
                "reserving_limit": 4,
                "late_fee_rate": 0.0,
            },
        ]
        stmt = (
            pg_insert(MembershipTypes)
            .values(membership_types)
            .on_conflict_do_update(
                index_elements=["membership_type"],
                set_={
                    k: getattr(MembershipTypes, k) for k in membership_types[0].keys()
                },
            )
        )
        session.execute(stmt)

        # Bulk insert Clients

        # there is something wrong here,, i couldn't fix lolz -@codyduong
        # clients = [
        #     {"client_id": 1, "name": "Alice Smith", "contact_info": "alice.smith@example.com",
        #      "membership_type": MembershipTypeEnum.Regular.value, "account_status": AccountStatusEnum.Active.value},
        #     {"client_id": 2, "name": "Bob Johnson", "contact_info": "bob.johnson@example.com",
        #      "membership_type": MembershipTypeEnum.Student.value, "account_status": AccountStatusEnum.Active.value},
        #     {"client_id": 3, "name": "Carol Williams", "contact_info": "carol.williams@example.com",
        #      "membership_type": MembershipTypeEnum.Senior_Citizen.value, "account_status": AccountStatusEnum.Suspended.value}
        # ]
        # stmt = pg_insert(Clients).values(clients).on_conflict_do_update(
        #     index_elements=["client_id"],
        #     set_={k: getattr(Clients, k) for k in clients[0].keys()}
        # )
        # session.execute(stmt)
        client_insert_sql = text("""
            INSERT INTO clients (client_id, name, contact_info, account_status, membership_type)
            VALUES 
                (1, 'Alice Smith', 'alice.smith@example.com', 'Active', 'Regular'),
                (2, 'Bob Johnson', 'bob.johnson@example.com', 'Active', 'Student'),
                (3, 'Carol Williams', 'carol.williams@example.com', 'Suspended', 'Senior Citizen'),
                (4, 'David Brown', 'david.brown@example.com', 'Active', 'Regular'),
                (5, 'Eve Green', 'eve.green@example.com', 'Active', 'Student')
            ON CONFLICT (client_id) DO UPDATE SET
                name = EXCLUDED.name,
                contact_info = EXCLUDED.contact_info,
                account_status = EXCLUDED.account_status,
                membership_type = EXCLUDED.membership_type
        """)

        session.execute(client_insert_sql)
        session.commit()

        # Bulk insert Staff
        staff = [
            {
                "staff_id": 1,
                "dob": "1990-05-15",
                "work_phone_number": "555-1234",
                "work_email": "alice.smith@library.org",
            },
            {
                "staff_id": 2,
                "dob": "1985-11-30",
                "work_phone_number": "555-5678",
                "work_email": "bob.johnson@library.org",
            },
            {
                "staff_id": 3,
                "dob": "1992-07-20",
                "work_phone_number": "555-8765",
                "work_email": "carol.williams@library.org",
            }
        ]
        stmt = (
            pg_insert(Staff)
            .values(staff)
            .on_conflict_do_update(
                index_elements=["staff_id"],
                set_={k: getattr(Staff, k) for k in staff[0].keys()},
            )
        )
        session.execute(stmt)

        # Bulk insert LibraryMaterial
        materials = [
            {
                "material_id": 1,
                "title": "The Great Novel",
                "publication_year": 2020,
                "genre": "Fiction",
                "availability_status": "Available",
                "type": MaterialTypeEnum.Book.value,
            },
            {
                "material_id": 2,
                "title": "History of Rome",
                "publication_year": 2015,
                "genre": "History",
                "availability_status": "Checked Out",
                "type": MaterialTypeEnum.Book.value,
            },
            {
                "material_id": 3,
                "title": "Digital Marketing",
                "publication_year": 2022,
                "genre": "Business",
                "availability_status": "Available",
                "type": MaterialTypeEnum.Digital_Media.value,
            },
            {
                "material_id": 4,
                "title": "Sci-Fi Movie",
                "publication_year": 2023,
                "genre": "Sci-Fi",
                "availability_status": "Available",
                "type": MaterialTypeEnum.Digital_Media.value,
            },
            {
                "material_id": 5,
                "title": "Tech Today",
                "publication_year": 2024,
                "genre": "Technology",
                "availability_status": "Available",
                "type": MaterialTypeEnum.Magazine.value,
            },
            {
                "material_id": 6,
                "title": "Mystery at Manor",
                "publication_year": 2018,
                "genre": "Mystery",
                "availability_status": "Available",
                "type": MaterialTypeEnum.Book.value,
            },
            {
                "material_id": 7,
                "title": "Science Today",
                "publication_year": 2025,
                "genre": "Science",
                "availability_status": "Available",
                "type": MaterialTypeEnum.Magazine.value,
            },
            {
                "material_id": 8,
                "title": "Learning SQL",
                "publication_year": 2021,
                "genre": "Technology",
                "availability_status": "Checked Out",
                "type": MaterialTypeEnum.Book.value,
            },
            {
                "material_id": 9,
                "title": "Nature Documentary",
                "publication_year": 2020,
                "genre": "Documentary",
                "availability_status": "Available",
                "type": MaterialTypeEnum.Digital_Media.value,
            },
            {
                "material_id": 10,
                "title": "Health & Wellness",
                "publication_year": 2023,
                "genre": "Health",
                "availability_status": "Available",
                "type": MaterialTypeEnum.Magazine.value,
            },
            {
                "material_id": 13,
                "title": "Adventures of Ruby",
                "publication_year": 2022,
                "genre": "Fiction",
                "availability_status": "Available",
                "type": MaterialTypeEnum.Book.value,
            },
            {
                "material_id": 14,
                "title": "The Art of Testing",
                "publication_year": 2020,
                "genre": "Technology",
                "availability_status": "Available",
                "type": MaterialTypeEnum.Book.value,
            },

        ]
        stmt = (
            pg_insert(LibraryMaterial)
            .values(materials)
            .on_conflict_do_update(
                index_elements=["material_id"],
                set_={k: getattr(LibraryMaterial, k) for k in materials[0].keys()},
            )
        )
        session.execute(stmt)

        # Bulk insert Books
        books = [
            {
                "book_id": 1,
                "material_id": 1,
                "author": "John Doe",
                "isbn": 9780123456789,
            },
            {
                "book_id": 2,
                "material_id": 2,
                "author": "Jane Smith",
                "isbn": 9789876543210,
            },
            {
                "book_id": 3,
                "material_id": 6,
                "author": "Agatha Christie",
                "isbn": 9780307588371,
            },
            {
                "book_id": 4,
                "material_id": 8,
                "author": "Daniele Moschella",
                "isbn": 9781492097611,
            },
            {
                "book_id": 5,
                "material_id": 13,
                "author": "Jane Smith",
                "isbn": 9781234567890,
            },
            {
                "book_id": 6,
                "material_id": 14,
                "author": "Test Author",
                "isbn": 9781111111111,
            },
        ]
        stmt = (
            pg_insert(Books)
            .values(books)
            .on_conflict_do_update(
                index_elements=["book_id"],
                set_={k: getattr(Books, k) for k in books[0].keys()},
            )
        )
        session.execute(stmt)

        # Bulk insert DigitalMedia
        digital_media = [
            {
                "media_id": 1,
                "material_id": 3,
                "creator": "Mark Lee",
                "format": DigitalMediaFormatEnum.eBook.value,
            },
            {
                "media_id": 2,
                "material_id": 4,
                "creator": "Director X",
                "format": DigitalMediaFormatEnum.DVD.value,
            },
            {
                "media_id": 3,
                "material_id": 9,
                "creator": "NAT Geo",
                "format": DigitalMediaFormatEnum.DVD.value,
            },
        ]
        stmt = (
            pg_insert(DigitalMedia)
            .values(digital_media)
 