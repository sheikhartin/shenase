import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import (
    Column,
    ForeignKey,
    Boolean,
    Integer,
    String,
    Enum,
    DateTime,
)
from sqlalchemy.orm import relationship

from shenase import enums
from shenase.database import Base
from shenase.config import SESSION_EXPIRE_DAYS, DEFAULT_AVATAR


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(35), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(65))
    role = Column(Enum(enums.UserRole), default=enums.UserRole.USER)
    is_verified = Column(Boolean, default=False)
    status = Column(Enum(enums.UserStatus), default=enums.UserStatus.ACTIVE)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    profile = relationship('Profile', back_populates='user', uselist=False)
    sessions = relationship('Session', back_populates='user')


class Profile(Base):
    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True, index=True)
    display_name = Column(String(50), nullable=False)
    avatar = Column(String(35), default=DEFAULT_AVATAR)
    bio = Column(String(300))
    location = Column(String(200))
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship('User', back_populates='profile')


class Session(Base):
    __tablename__ = 'sessions'

    id = Column(Integer, primary_key=True, index=True)
    access_token = Column(
        String(32),
        default=lambda: uuid.uuid4().hex,
        unique=True,
        index=True,
    )
    client_fingerprint = Column(String(64), nullable=False)
    status = Column(
        Enum(enums.SessionStatus),
        default=enums.SessionStatus.ACTIVE,
    )
    expires_at = Column(
        DateTime,
        default=lambda: (
            datetime.now(timezone.utc) + timedelta(days=SESSION_EXPIRE_DAYS)
        ),
    )
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship('User', back_populates='sessions')
