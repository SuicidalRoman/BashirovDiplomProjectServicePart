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


users = Table(
    "users",
    metadata,
    Column("user_id", Integer, primary_key=True),
    Column("user_login", String, unique=True, nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("user_status", Enum(UserStatus), nullable=False, default=UserStatus.CLIENT),
    Column("registered_at", TIMESTAMP, default=datetime.utcnow),
    Column("updated_at", TIMESTAMP, default=datetime.utcnow),
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
    Column("created_at", TIMESTAMP, default=datetime.utcnow),
    Column("updated_at", TIMESTAMP, default=datetime.utcnow),
    Column("request_title", String, nullable=False),
    Column("event_title", String, nullable=False),
    Column("event_type", Enum(EventType), nullable=False, default=EventType.CONFERENCE)
)
