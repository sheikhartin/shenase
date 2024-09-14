import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    ForeignKey,
    Boolean,
    String,
    Enum,
    DateTime,
)
from sqlalchemy.orm import relationship

from shenase import enums
from shenase.database import Base
from shenase.config import DEFAULT_AVATAR


class User(Base):
    __tablename__ = 'users'

    id = Column(
        String(32),
        default=lambda: uuid.uuid4().hex,
        primary_key=True,
        index=True,
    )
    username = Column(String(35), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(65), nullable=True)
    role = Column(Enum(enums.UserRole), default=enums.UserRole.USER)
    is_verified = Column(Boolean, default=False)
    status = Column(Enum(enums.UserStatus), default=enums.UserStatus.ACTIVE)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    profile = relationship('Profile', back_populates='user', uselist=False)


class Profile(Base):
    __tablename__ = 'profiles'

    id = Column(
        String(32),
        default=lambda: uuid.uuid4().hex,
        primary_key=True,
        index=True,
    )
    user_id = Column(String(32), ForeignKey('users.id'), nullable=False)
    display_name = Column(String(50), nullable=False)
    avatar = Column(String(35), default=DEFAULT_AVATAR)
    bio = Column(String(300))
    location = Column(String(200))

    user = relationship('User', back_populates='profile')
