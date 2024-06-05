import enum
from datetime import datetime
from sqlalchemy import Boolean, Enum, MetaData, Table, Column, String, Integer, TIMESTAMP, ForeignKey, Date, CheckConstraint


metadata = MetaData()


class UserStatus(enum.Enum):
    CLIENT = "client"
    ADMIN = "admin"

class ProfileType(enum.Enum):
    INDIVIDUAL = "individual"
    COMPANY = "company"

class EventType(enum.Enum):
    CONFERENCE = "conference"
    EXHIBITION = "exhibition"

class RequestStatus(enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class RegistrationStatus(enum.Enum):
    REGISTERED = "registered"
    ATTENDED = "attended"
    CANCELLED = "cancelled"


users = Table(
    "users",
    metadata,
    Column("user_id", Integer, primary_key=True),
    Column("user_login", String, unique=True, nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("user_status", Enum(UserStatus), nullable=False, default=UserStatus.CLIENT),
    Column("registered_at", TIMESTAMP, default=datetime.utcnow()),
    Column("updated_at", TIMESTAMP, default=datetime.utcnow()),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("is_superuser", Boolean, default=False, nullable=False),
    Column("is_verified", Boolean, default=False, nullable=False)
)

profiles = Table(
    "profiles",
    metadata,
    Column("profile_id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.user_id"), unique=True, nullable=False),
    Column("registered_at", TIMESTAMP, default=datetime.utcnow()),
    Column("updated_at", TIMESTAMP, default=datetime.utcnow()),
    Column("profile_type", Enum(ProfileType), nullable=False, default=ProfileType.INDIVIDUAL),
    Column("surname", String),
    Column("firstname", String),
    Column("patronymic", String),
    Column("birthdate", Date),
    Column("phone", String)
)

requests = Table(
    "requests",
    metadata,
    Column("request_id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("profiles.profile_id"), nullable=False),
    Column("created_at", TIMESTAMP, default=datetime.utcnow()),
    Column("updated_at", TIMESTAMP, default=datetime.utcnow()),
    Column("request_title", String, nullable=False),
    Column("request_description", String, nullable=True),
    Column("event_id", Integer, ForeignKey("events.id"), nullable=False)
)

events = Table(
    "events",
    metadata,
    Column("event_id", Integer, primary_key=True),
    Column("request_id", Integer, ForeignKey("requests.request_id"), nullable=False),
    Column("title", String, nullable=False),
    Column("description", String, nullable=True),
    Column("event_type", Enum(EventType), nullable=False, default=EventType.CONFERENCE),
    Column("start_timestamp", TIMESTAMP, nullable=False),
    Column("end_timestamp", TIMESTAMP, nullable=False),
    Column("created_at", TIMESTAMP, default=datetime.utcnow()),
    Column("updated_at", TIMESTAMP, default=datetime.utcnow()),
)

registrations = Table(
    "registrations", 
    metadata,
    Column("registration_id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("profiles.profile_id"), nullable=False),
    Column("event_id", Integer, ForeignKey("events.event_id"), nullable=False),
    Column("status", Enum(RegistrationStatus), nullable=False, default=RegistrationStatus.REGISTERED),
    Column("registered_at", TIMESTAMP, default=datetime.utcnow()),
    Column("updated_at", TIMESTAMP, default=datetime.utcnow())
)