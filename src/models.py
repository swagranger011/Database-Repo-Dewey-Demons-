# this was generated entirely with generative ai -@codyduong

from datetime import date
import enum
from typing import Optional, List
from sqlmodel import Field, Relationship, SQLModel


class MembershipTypeEnum(str, enum.Enum):
    Regular = "Regular"
    Student = "Student"
    Senior_Citizen = "Senior Citizen"


class AccountStatusEnum(str, enum.Enum):
    Active = "Active"
    Suspended = "Suspended"


class MaterialTypeEnum(str, enum.Enum):
    Book = "Book"
    Digital_Media = "Digital Media"
    Magazine = "Magazine"


class DigitalMediaFormatEnum(str, enum.Enum):
    eBook = "eBook"
    Audiobook = "Audiobook"
    DVD = "DVD"


class ReservationStatusEnum(str, enum.Enum):
    Active = "Active"
    Fulfilled = "Fulfilled"
    Cancelled = "Cancelled"


class MembershipTypes(SQLModel, table=True):
    __tablename__ = "membership_types"
    membership_type: str = Field(
        primary_key=True,  # sa_column_kwargs={"enum": MembershipTypeEnum}
    )
    borrowing_limit: int
    reserving_limit: int
    late_fee_rate: float

    clients: List["Clients"] = Relationship(back_populates="membership_type")


class Clients(SQLModel, table=True):
    client_id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    contact_info: str
    account_status: AccountStatusEnum
    membership_type: MembershipTypeEnum = Field(foreign_key="membership_types.membership_type")

    membership_type_rel: MembershipTypes = Relationship(back_populates="clients")
    staff: Optional["Staff"] = Relationship(back_populates="client")
    borrowing_transactions: List["BorrowingTransactions"] = Relationship(
        back_populates="client"
    )
    reservations: List["Reservations"] = Relationship(back_populates="client")
    notifications: List["Notifications"] = Relationship(back_populates="client")


class Staff(SQLModel, table=True):
    staff_id: int = Field(primary_key=True, foreign_key="clients.client_id")
    dob: Optional[str]
    work_phone_number: str
    work_email: str

    client: Clients = Relationship(back_populates="staff")


class LibraryMaterial(SQLModel, table=True):
    __tablename__ = "library_material"
    material_id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    publication_year: int
    genre: str
    availability_status: str
    type: str  # = Field(sa_column_kwargs={"enum": MaterialTypeEnum})

    books: Optional["Books"] = Relationship(back_populates="material")
    digital_media: Optional["DigitalMedia"] = Relationship(back_populates="material")
    magazines: Optional["Magazines"] = Relationship(back_populates="material")
    borrowing_transactions: List["BorrowingTransactions"] = Relationship(
        back_populates="material"
    )
    reservations: List["Reservations"] = Relationship(back_populates="material")


class Books(SQLModel, table=True):
    book_id: Optional[int] = Field(default=None, primary_key=True)
    material_id: int = Field(foreign_key="library_material.material_id")
    author: str
    isbn: str = Field(max_length=17, unique=True)

    material: LibraryMaterial = Relationship(back_populates="books")


class DigitalMedia(SQLModel, table=True):
    __tablename__ = "digital_media"
    media_id: Optional[int] = Field(default=None, primary_key=True)
    material_id: int = Field(foreign_key="library_material.material_id")
    creator: str
    format: str  # = Field(sa_column_kwargs={"enum": DigitalMediaFormatEnum})

    material: LibraryMaterial = Relationship(back_populates="digital_media")


class Magazines(SQLModel, table=True):
    magazine_id: Optional[int] = Field(default=None, primary_key=True)
    material_id: int = Field(foreign_key="library_material.material_id")
    issue_number: str
    publish_date: Optional[str]

    material: LibraryMaterial = Relationship(back_populates="magazines")


class BorrowingTransactions(SQLModel, table=True):
    __tablename__ = "borrowing_transactions"
    transaction_id: Optional[int] = Field(default=None, primary_key=True)
    client_id: int = Field(foreign_key="clients.client_id")
    material_id: int = Field(foreign_key="library_material.material_id")
    borrow_date: date
    due_date: date
    return_date: Optional[date] = None
    fine_amount: float

    client: Clients = Relationship(back_populates="borrowing_transactions")
    material: LibraryMaterial = Relationship(back_populates="borrowing_transactions")


class Reservations(SQLModel, table=True):
    reservation_id: Optional[int] = Field(default=None, primary_key=True)
    client_id: int = Field(foreign_key="clients.client_id")
    material_id: int = Field(foreign_key="library_material.material_id")
    reservation_date: date
    status: str  # = Field(sa_column_kwargs={"enum": ReservationStatusEnum})

    client: Clients = Relationship(back_populates="reservations")
    material: LibraryMaterial = Relationship(back_populates="reservations")


class Notifications(SQLModel, table=True):
    notification_id: Optional[int] = Field(default=None, primary_key=True)
    client_id: int = Field(foreign_key="clients.client_id")
    message: str
    sent_date: date

    client: Clients = Relationship(back_populates="notifications")
